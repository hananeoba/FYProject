from django.db import models

class AbstrctBaseModel(models.Model):
    # audit fields
    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        "userapp.AdminUser",
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "userapp.AdminUser",
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Activity_Nature(AbstrctBaseModel):
    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"activitynature'

    def __str__(self):
        return str(self.label)


class State(AbstrctBaseModel):
    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"state'

    def __str__(self):
        return self.label


class Province(AbstrctBaseModel):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"province'

    def __str__(self):
        return self.label


class Event_Type(AbstrctBaseModel):
    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"eventtype'

    def __str__(self):
        return self.label


class Causes(AbstrctBaseModel):

    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"causes'

    def __str__(self):
        return self.label


class Structure_Type(AbstrctBaseModel):
    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"structuretype'

    def __str__(self):
        return str(self.label)


class Company(AbstrctBaseModel):
    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"company'

    def __str__(self):
        return str(self.label)


class Structure(AbstrctBaseModel):
    parent_structure = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    structure_type = models.ForeignKey(
        Structure_Type, on_delete=models.SET_NULL, null=True, blank=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    province = models.ManyToManyField(
        Province, related_name="province"
    )

    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"structure'

    def __str__(self):
        return str(self.label)


class Installation(AbstrctBaseModel):
    structure = models.ForeignKey(
        Structure, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"installation'

    def __str__(self):
        return str(self.label)


class Work_Type(AbstrctBaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        # managed = True
        db_table = 'basedata_schema\".\"worktype'

    def __str__(self):
        return str(self.label)


class Work(AbstrctBaseModel):
    work_type = models.ForeignKey(
        Work_Type, on_delete=models.SET_NULL, null=True, blank=True
    )
    parent_work = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    installation = models.ForeignKey(
        Installation, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        unique_together = ("code", "installation", "parent_work", "work_type")
        # managed = True
        db_table = 'basedata_schema\".\"work'

    def __str__(self):
        return str(self.label)


# end of models.py
