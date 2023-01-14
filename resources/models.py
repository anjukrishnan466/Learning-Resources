from django.db import models
from django.contrib.auth.models import User, auth

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=1250)

    def __str__(self):
        return self.name


class Resources(models.Model):

    title = models.CharField(max_length=1250)
    description = models.CharField(max_length=225)
    duration = models.CharField(max_length=225)
    link = models.CharField(max_length=225)
    resource_file = models.FileField(
        upload_to="resources/", max_length=250, null=True, default=None)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    User = models.ManyToManyField(User, through='Status', null=True)


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resources = models.ForeignKey(Resources, on_delete=models.CASCADE)
    status = models.IntegerField(null=True, default=0)
    total_time_spend = models.IntegerField(default=0)


class TimeSpendUser(models.Model):

    date_user = models.DateTimeField()
    time_spend_by_user = models.IntegerField(default=0)
    status = models.ForeignKey(Status, null=True, on_delete=models.CASCADE)
