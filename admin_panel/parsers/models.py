from jsonfield import JSONField
from django.db import models


class Parser(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    configuration = JSONField()

    def __str__(self):
        return self.name

class ScheduledTimePoint(models.Model):
    time = models.TimeField()
    parser = models.ForeignKey('Parser', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time}"