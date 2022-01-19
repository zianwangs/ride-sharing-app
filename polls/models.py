import datetime
from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    is_driver = models.BooleanField()

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    car_type = models.CharField(max_length = 20)
    car_capacity = models.IntegerField()
    real_name = models.CharField(max_length = 50)
    licence_number = models.CharField(max_length = 50)
    special_info = models.CharField(max_length = 200)
    number_of_incomplete_orders = models.IntegerField(default = 0)

class Ride(models.Model):
    status = models.IntegerField(default = 1)
    passenger_num = models.IntegerField(default = 0)
    driver = models.ForeignKey(Driver, null = True, on_delete = models.CASCADE)
    car_type = models.CharField(max_length = 20, default="Unspecified")
    destination = models.CharField(max_length = 100)
    arrival_time = models.DateTimeField()
    is_exclusive = models.BooleanField()
    sharer_num = models.IntegerField()
    special_info = models.CharField(max_length = 200, null = True)
    confirm_time = models.DateTimeField(null = True)
    complete_time = models.DateTimeField(null = True)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete = models.CASCADE)
    role = models.BooleanField()
    request_time = models.DateTimeField()
    passenger_num = models.IntegerField(default = 0)

'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
'''
# Create your models here.
