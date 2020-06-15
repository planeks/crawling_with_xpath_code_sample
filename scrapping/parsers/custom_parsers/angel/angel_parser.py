import requests
import json
import sys
import time
import argparse
import os
import datetime as dt
from math import ceil as math_ceil
import django
from queries import *

# Django settings
django_path = '/'.join(os.getcwd().split('/')[:-4]) + '/admin_panel'
sys.path.append(django_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'jobagregator.settings'
django.setup()

# Graphql settings
GRAPHQL_URL = 'https://angel.co/graphql?fallbackAOR=talent'
headers = {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': '*/*',
    'Host': 'angel.co'
}


def response_to_json(response):
    if response.status_code < 300:
        return response.json()
    else:
        print(response.reason)


def get_page_with_startups(page, variables):
    query = companies_query
    # Convert json to string
    variables['filterConfigurationInput']['page'] = page
    variables = json.dumps(variables)
    data = {
        'variables': variables,
        'query': query
    }
    response = requests.post(GRAPHQL_URL, json=data, headers=headers)
    return response_to_json(response)


def get_job_details(job_id):
    query = jobs_query
    variables = {
        'id': job_id
    }
    data = {
        'query': query,
        'variables': variables
    }
    response = requests.post(GRAPHQL_URL, json=data, headers=headers)
    return response_to_json(response)


def generate_slug(source, job_id, company_slug, job_slug):
    return f'{source}-{job_id}-{company_slug}-{job_slug}'


def parse(startups_variables):
    from jobs.models import Job
    page = 1
    current_page = get_page_with_startups(page, startups_variables)
    startups_count = current_page['data']['talent']['jobSearchResults']['totalStartupCount']
    page_count = math_ceil(startups_count / 10.0)
    while page <= page_count:
        current_page = get_page_with_startups(page, startups_variables)
        startups = current_page['data']['talent']['jobSearchResults']['startups']['edges']
        for startup in startups:
            jobs = startup['node']['highlightedJobListings']
            startup_slug = startup['node']['slug']
            startup_name = startup['node']['name']
            for job in jobs:
                job_posted_at = dt.date.fromtimestamp(
                    job['liveStartAt'])
                job = get_job_details(
                    job['id'])['data']['jobListing']

                job_skills = ','.join(
                    list(map(lambda el: el['displayName'], job['skills'])))

                job_url = f"https://angel.co/company/{startup_slug}/jobs/{job['id']}-{job['slug']}"
                job_slug = generate_slug(
                    "angel", job['id'], startup_slug, job['slug'])
                new_job, created = Job.objects.get_or_create(
                    company_name=startup_name,
                    title=job['title'],
                    source='angel',
                    description=job['description'],
                    url=job_url,
                    remote=job['remote'],
                    posted_at=job_posted_at,
                    job_type=job['jobType'],
                    salary=job['compensation'],
                    locations=','.join(job['locationNames']),
                    experience=job['yearsExperienceMin'] if job['yearsExperienceMin'] else 0,
                    skills=job_skills,
                    slug=job_slug
                )
        page += 1


parser = argparse.ArgumentParser()
# Salary
parser.add_argument('--min_salary', default=None)
parser.add_argument('--max_salary', default=None)
# Equity
parser.add_argument('--min_equity', default=None)
parser.add_argument('--max_equity', default=None)
# Years in development
parser.add_argument('--min_years', default=None)
parser.add_argument('--max_years', default=None)
parser.add_argument('--remote', default="REMOTE_ONLY")
# Search Keyword
parser.add_argument('--search', default='python')
# Parse args
args = parser.parse_args()

# Search settings
filters = {
    'filterConfigurationInput': {
        'customJobTitles': args.search.split(','),
        'equity': {
            'min': float(args.min_equity) if args.min_equity is not None else None,
            'max': float(args.max_equity) if args.max_equity is not None else None
        },
        'remotePreference': 'REMOTE_ONLY',
        'salary': {
            'min': float(args.min_salary) if args.min_salary is not None else None,
            'max': float(args.max_salary) if args.max_salary is not None else None
        },
        'yearsExperience': {
            'min': float(args.min_years) if args.min_years is not None else args.min_years,
            'max': float(args.max_years) if args.max_years is not None else args.max_years,
        }
    }
}

try:
    print("Parsing...")
    parse(filters)
    print("Successfully parsed!!")
except KeyboardInterrupt:
    print("\nFinished by user interrupt")
