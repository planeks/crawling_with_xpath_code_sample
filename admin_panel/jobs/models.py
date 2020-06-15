from django.db import models

# Create your models here.
sources = (
    ('angel', 'AngelList'), ('indeed', 'Indeed'), ('remoteok', 'RemoteOK')
)


class Job(models.Model):
    company_name = models.CharField(max_length=256)
    title = models.CharField(max_length=100)
    url = models.URLField()
    remote = models.BooleanField(default=True)
    source = models.CharField(choices=sources, max_length=100)
    description = models.TextField()
    job_type = models.CharField(max_length=25, blank=True)
    salary = models.CharField(max_length=50, blank=True)
    locations = models.TextField(blank=True)
    experience = models.FloatField(null=True)
    skills = models.TextField(blank=True)
    posted_at = models.DateField()
    slug = models.SlugField(unique=True)
    is_old = models.BooleanField(default=False)

    def __str__(self):
        return self.title
