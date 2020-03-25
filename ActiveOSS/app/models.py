#  myapp/models.py
from __future__ import unicode_literals # future between underscores, 2 on each side
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from django.db import connection
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db import models
from django.contrib.auth.models import User

'''
    cursor = connection.cursor()
    result = cursor.execute("SELECT COUNT(*) FROM test")
    print (result[0]['count'])
    '''

class TestModel(DjangoCassandraModel):

    __table_name = "test_model"
    __keyspace__= "dis_test"
    nrc   = columns.Text(primary_key=True,required=False)
    name  = columns.Text(required=False)
    occupation  = columns.Text(required=False)
    labour_id = columns.Text(index=True)
    race  = columns.Text(required=False)
    religion  = columns.Text(required=False)
    father_name  = columns.Text(required=False)
    father_nrc  = columns.Text(required=False)
    marital_status   = columns.Boolean(required=False)
    dob=columns.Date(required=False)
    spouse_name  = columns.Text(required=False)
    spouse_nrc  = columns.Text(required=False)
    street  = columns.Text(required=False)
    city  = columns.Text(required=False)
    home_no=columns.Text(required=False)
    ward=columns.Text(required=False)
    township=columns.Text(required=False)
    gender=columns.Text(required=False)


    def __str__(self):
       return '%s %s %s'%(self.nrc, self.name, self.race)
       class Meta:
         db_table = "test_model"

    def address_approval(self):
        return '%s %s %s'%(self.nrc, self.name, self.father_name,self.street,self.ward,self.home_no,self.township)

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return self.user.username

class CrimeRecord(DjangoCassandraModel):

    __table_name = "crime_record"
    __keyspace__= "dis_test1"
    crime_id   = columns.Text(primary_key=True,required=False)
    court  = columns.Text(required=False)
    potema  = columns.Text(required=False)
    penalty  = columns.Text(required=False)
    criminal_name  = columns.Text(required=False)
    criminal_nrc  = columns.Text(required=False)
    time=columns.Date(required=False)
    tayalo_name  = columns.Text(required=False)
    tayalo_nrc  = columns.Text(required=False)
    street  = columns.Text(required=False)
    city  = columns.Text(required=False)
    number=columns.Text(required=False)
    ward=columns.Text(required=False)
    township=columns.Text(required=False)

    def __str__(self):
       return '%s %s %s'%(self.criminal_nrc, self.criminal_name, self.potema)
       class Meta:
         db_table = "crime_record"

    def address_approval(self):
        return '%s %s %s'%(self.nrc, self.name, self.father_name)


