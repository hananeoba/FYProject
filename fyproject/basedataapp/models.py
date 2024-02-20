from django.db import models
from django.utils import timezone


# Create your models here.
class AbstrctBaseModel(models.Model):
    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        "userapp.User",
        on_delete=models.PROTECT,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "userapp.User",
        on_delete=models.PROTECT,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True,)
    updated_at = models.DateTimeField(null = True, blank = True,)

    class Meta:
        abstract = True


class ActivityNature(AbstrctBaseModel):
    def __str__(self):
        return str(self.label)


class StructureType(AbstrctBaseModel):
    def __str__(self):
        return str(self.label)


class Company(AbstrctBaseModel):

    def __str__(self):
        return str(self.label)


class WorkType(AbstrctBaseModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.label)


class Structure(AbstrctBaseModel):
    structures = models.ForeignKey("self", on_delete=models.PROTECT)
    structure_type = models.ForeignKey(StructureType, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.label)


class Installation(AbstrctBaseModel):
    structure = models.ForeignKey("Structure", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.label)


class Work(AbstrctBaseModel):
    worktype = models.ForeignKey(WorkType, on_delete=models.PROTECT)
    work_s = models.ForeignKey("self", on_delete=models.PROTECT)
    installation_id = models.ForeignKey(Installation, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.label)


# end of models.py
