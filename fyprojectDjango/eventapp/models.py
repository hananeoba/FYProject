from django.db import models
from basedataapp.models import AbstrctBaseModel, Work

# Create your models here.


class Event(AbstrctBaseModel):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    start_date = models.DateTimeField(auto_now=True)
    event_description = models.TextField()
    event_location = models.CharField(max_length=255)
    event_type = models.ForeignKey("basedataapp.Event_Type", on_delete=models.PROTECT)
    event_status = models.CharField(max_length=25)
    event_duration = models.DurationField()
    event_causes = models.ManyToManyField(
        "basedataapp.Causes",
        related_name="event_causes",
    )

    class Meta:
        db_table = 'event_schema\".\"event'

    def __str__(self):
        return self.label


