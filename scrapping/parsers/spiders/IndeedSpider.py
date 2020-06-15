import scrapy
from scrapy.http import Request
import datetime as dt
import time
import sys
import os
import math
import django
from ..utils import generate_slug

# Django settings
django_path = '/'.join(os.getcwd().split('/')[:-2]) + '/admin_panel'
print(django_path)
sys.path.append(django_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'jobagregator.settings'
django.setup()


class IndeedSpider(scrapy.Spider):
    name = "indeed"

    def __init__(self, q="python", location="remote", job_type="all", **kwargs):
        self.start_urls = [
            f'https://www.indeed.co.uk/jobs?q={q}&l={location}&jt={job_type}']

    

    def start_requests(self):
        
        urls = self.start_urls
        
        for url in urls:
            # print("PAGE_COUNT",page_count)
            # for start in range(0, page_count, 10):
            #     url+= f"&start={start}"
            #     print(url)
                yield scrapy.Request(url=url, callback=self.parse_page_count)

    def parse_page_count(self, response):
        jobs_count = int(response.xpath('//div[@id="searchCountPages"]/text()').get().split('Page')[1].split()[-2])
        print('jobs_count', jobs_count)
        jobs_per_page = 15.0
        page_count = math.ceil(jobs_count / 15)
        print('PAGE_COUNT', page_count)
        
        for start in range(0, page_count):
            print("START", start)
            link = response.url + f"&start={start*10}"
            yield scrapy.Request(url=link, callback=self.parse_page)

        

    def parse_page(self, response):
        time.sleep(1)
        titles = response.css('h2.title')
        
        for title in titles:
            a = title.css('a::attr(href)').get()
            url = "https://www.indeed.co.uk" + a
            get_params = a.split('&')
            job_id = get_params[0].split('=')[-1]
            job_url = f"https://www.indeed.co.uk/viewjob?jk={job_id}"
            yield scrapy.Request(url=job_url, callback=self.parse_job)

    def parse_job(self, response):
        from jobs.models import Job
        # Extract title
        title = response.css('h3.jobsearch-JobInfoHeader-title::text').get()
        # Extract description
        paragraphs = response.xpath(
            "//div[@id='jobDescriptionText']//p/text()")
        description = "\n".join(map(lambda v: v.get(), paragraphs))
        # Extract company_name
        company_name = response.xpath(
            '//div[contains(@class, "jobsearch-JobInfoHeader-subtitle")]/div/div')
        company_name_link = company_name.xpath(
            './/a/text()').extract_first(default='not-found')
        if company_name_link != 'not-found':
            company_name = company_name_link
        else:
            company_name = company_name.xpath('./text()').get()

        # Extract posted_at data
        days_ago = response.xpath(
            '//div[contains(@class, "jobsearch-JobMetadataFooter")]/text()').get().split()[1]
        is_old = False
        if "+" in days_ago:
            days_ago = 30
            is_old = True
        elif "Today" in days_ago:
            days_ago = 0
        else:
            days_ago = int(days_ago)
        posted_at = dt.date.today() - dt.timedelta(days=days_ago)

        # Extract location, job_type, salary data
        data = {}
        header_block = response.xpath(
            '//div[contains(@class, "jobsearch-JobMetadataHeader")]//div')
        for header in header_block:
            self.preprocess_data(header, data)

        remote = False
        if 'remote' in description.lower() or 'remote' in title.lower() or ('location' in data and data['location'].lower() == 'home based'):
            remote = True
        # Move data to db
        job = Job.objects.get_or_create(
            slug=generate_slug("indeed", response.url.split(
                'jk=')[1], company_name.replace(' ', '-'), title.replace(' ', '-')),
            title=title,
            description=description,
            locations=data['location'] if 'location' in data else "",
            url=response.url,
            company_name=company_name,
            posted_at=posted_at,
            is_old=is_old,
            job_type=data['job_type'] if 'job_type' in data else "",
            salary=data['salary'] if 'salary' in data else "",
            source='indeed',
            remote=remote
        )


    def preprocess_data(self, header, data):
        location = False
        salary = False
        job_type = False
        if not 'location' in data:
            location = header.css(
                'div.icl-IconFunctional--location').extract_first(default='not-found')
        if not 'job_type' in data:
            job_type = header.css(
                'div.icl-IconFunctional--jobs').extract_first(default='not-found')
        if not 'salary' in data:
            salary = header.css(
                'div.icl-IconFunctional--salary').extract_first(default='not-found')

        header_data = header.xpath('./span/text()').get()
        if location and location != 'not-found':
            data['location'] = header_data
        elif job_type and job_type != 'not-found':
            data['job_type'] = header_data
        elif salary and salary != 'not-found':
            data['salary'] = header_data
