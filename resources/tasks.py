import json
import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from tablib import Dataset
from .models import Resources

from celery import shared_task


@shared_task
def import_excel(imported_data):
    "background task to upload resource excel to db asynchronously"
    # print("anju")
    # dataset = Dataset()
    # imported_data = dataset.load(myfile.read(), format='xlsx')
    # print(imported_data)
    print(type(imported_data), "anju1")
    print(json.loads(imported_data))
    json_data = json.loads(imported_data)
    for data in json_data:

        value = Resources(
            title=data['title'],
            description=data['description'],
            link=data['link'],
            resource_file=data['resource_file'],
            category_id=data['category'],
        )
        value.save()
