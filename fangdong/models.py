# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Landlord(models.Model):
    # host_about	host_verifications
    # Responsible, mid-late thirties, American writer and Academic. 	['email', 'phone', 'facebook', 'reviews', 'kba']
    listing_id = models.IntegerField()
    host_id = models.IntegerField()
    superhost = models.BooleanField()
    response_time = models.CharField(max_length=50, null=True)
    response_rate = models.CharField(max_length=10, null=True)
    number_of_reviews = models.IntegerField()
    review_scores_rating = models.IntegerField(null=True)
    host_about = models.TextField(max_length=500, null=True)
    host_verifications = models.CharField(max_length=100)

    class Meta:
        unique_together = ('listing_id', 'host_id',)
        db_table = 'landlord'


class Visitors(models.Model):
    visitor_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=5, null=True)
    phone = models.CharField(max_length=11, null=True)
    english_level = models.CharField(max_length=10, null=True)
    degree = models.CharField(max_length=10, null=True)
    age = models.CharField(max_length=10, null=True)
    # visitor_Landlord = models.ManyToManyField(Landlord)

    class Meta:
        unique_together = ('name', 'gender', 'phone',)
        db_table = 'visitors'


class VisitRecords(models.Model):
    visitor_id = models.IntegerField()
    landlord_id = models.IntegerField()
    question1_score = models.IntegerField(default=0)
    question2_score = models.IntegerField(default=0)
    question3_score = models.IntegerField(default=0)
    question4_score = models.IntegerField(default=0)
    question5_score = models.IntegerField(default=0)
    question6_score = models.IntegerField(default=0)

    class Meta:
        db_table = 'visitor_landlord_relation'

