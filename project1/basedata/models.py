from django.db import models


# Create your models here.
class AbstrctBaseModel(models.Model):
    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActivityNature(models.Model):
    activity_nature = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.activity_nature)


class StructureType(AbstrctBaseModel):
    structure_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.structure_type)


class Company(AbstrctBaseModel):
    company_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.company_name)


class WorkType(models.Model):
    worktype = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.worktype)


class Structure(AbstrctBaseModel):
    structure_id = models.CharField(max_length=100, unique=True)
    structures = models.ForeignKey("self", on_delete=models.PROTECT)
    structure_type = models.ForeignKey(StructureType, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.structure_id)


class Installation(AbstrctBaseModel):
    installation_id = models.CharField(max_length=100, unique=True)
    structure = models.ForeignKey("Structure", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.installation_id)


class Work(AbstrctBaseModel):
    work_id = models.CharField(max_length=100, unique=True)
    worktype = models.ForeignKey(WorkType, on_delete=models.PROTECT)
    work_s = models.ForeignKey("self", on_delete=models.PROTECT)
    installation_id = models.ForeignKey(Installation, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.work_id)


# end of models.py
