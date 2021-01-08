from django.db import models


class RawData(models.Model):
    data = models.TextField(max_length=2000)
    is_valid = models.BooleanField(default=True)
    key = models.AutoField(primary_key=True)


class ExcelData(models.Model):
    lecture_data = models.TextField(max_length=750)
    use_link = models.BooleanField(default=True)
    links = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)
    key = models.AutoField(primary_key=True)
