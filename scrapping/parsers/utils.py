"""Spiders Utils"""


def generate_slug(source, job_id, company_slug, job_slug):
    return f'{source}-{job_id}-{company_slug}-{job_slug}'
