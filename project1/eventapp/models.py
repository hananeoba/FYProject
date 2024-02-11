from django.db import models
from basedata.models import AbstrctBaseModel, Work, Company

# Create your models here.


class Event(AbstrctBaseModel):
    event_name = models.CharField(primary_key=True, unique=True, max_length=255)
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    company_id = models.ForeignKey(Company, on_delete=models.PROTECT)
    start_date = models.DateTimeField(auto_now=True)
    event_description = models.TextField()
    event_location = models.CharField(max_length=255)
    event_type = models.ForeignKey("EventType", on_delete=models.PROTECT)
    event_status = models.CharField(max_length=25)
    event_duration = models.DurationField()
    event_causes = models.ManyToManyField(
        "Causes",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.event_name


class EventType(AbstrctBaseModel):
    event_type_name = models.CharField(unique=True, max_length=25)
    event_type_description = models.TextField()

    def __str__(self):
        return self.event_type_name


class Causes(AbstrctBaseModel):
    cause_id = models.AutoField(primary_key=True)
    cause_name = models.CharField(max_length=255, unique=True)
    cause_description = models.TextField()

    def __str__(self):
        return self.cause_name
