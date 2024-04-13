
from django.db import models
from basedataapp.models import AbstrctBaseModel, Work
from django.utils import timezone

# Create your models here.


class Event(AbstrctBaseModel):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    start_date = models.DateTimeField( default=timezone.now)
    event_description = models.TextField(default="No Description")
    event_location = models.CharField(max_length=255, blank=True, null=True)
    event_type = models.ForeignKey("basedataapp.Event_Type", on_delete=models.PROTECT)
    event_status = models.CharField(max_length=25, default="pending")
    event_duration = models.DurationField(null=True, blank=True)
    event_causes = models.ManyToManyField(
        "basedataapp.Causes",
        related_name="event_causes",
    )

    class Meta:
        ordering = ["start_date"]
        db_table = 'event_schema\".\"event'

    def __str__(self):
        return self.label


