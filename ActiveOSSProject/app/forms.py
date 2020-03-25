from django import forms
from django.forms import ModelForm
from .models import TestModel
from .models import CrimeRecord


class PersonForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = TestModel
        fields = ['name','nrc','occupation','father_name','father_nrc','dob','spouse_name','spouse_nrc','labour_id','marital_status','race','religion','city','street','home_no','ward','township','gender']

class UpdatePerson(ModelForm):
  required_css_class = 'required'
  class Meta:
        fields = ['nrc','attribute','value']

class CrimeRecordForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = CrimeRecord
        fields = ['crime_id','criminal_nrc','criminal_name','tayalo_name','tayalo_nrc','court','potema','penalty','city','street','number','ward','township','time']

# model = TestModel
       
