# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login.models import Users
from datetime import date, datetime, timedelta


# Create your models here.
class TripManager(models.Manager):
    def trip_validation(self, post_data):
        errors=[]
        today = datetime.today()
        if len(post_data['destination']) < 3 :
            errors.append("Destination needs to be more than 3 characters")
        if len(post_data['plan']) < 3 :
            errors.append("Plan needs to be longer than 3 characters")
        try:
            travelfrom = datetime.strptime(post_data['start_date'], '%Y-%m-%d')
            if travelfrom < today - timedelta(1):
                errors.append("Starting travel date is in the past")
            if post_data['end_date'] < post_data['start_date']:
                errors.append("End Date cannot be before Start Date")
        except ValueError:
            errors.append('Must fill out dates')       
        return errors

    def addtrip(self, cleanData, request):
        return self.create(
            destination = cleanData['destination'],
            start_date = cleanData['start_date'],
            end_date = cleanData['end_date'],
            plan = cleanData['plan'],
            planner = Users.objects.get(id=request.session['id'])
        )

    def joiner(self, id, user):
        trip = self.get(id = id)
        trip.tourist.add(user)
        return self
    
class Trip(models.Model):
    destination=models.CharField(max_length=255)
    plan=models.TextField(max_length=1000)
    start_date=models.DateField()
    end_date=models.DateField()
    tourist=models.ManyToManyField(Users, related_name="tourist")
    planner=models.ForeignKey(Users, related_name="planner")
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = TripManager()

