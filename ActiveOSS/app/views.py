'''
    from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from app.models import TestModel
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import TestModel,CrimeRecord
from .forms import PersonForm,CrimeRecordForm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.fonts import addMapping
from .fusioncharts import FusionCharts
import datetime
import json

'''
def index(request):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('ndb')
    insert = TestModel(nrc="12/mgdn(naing)123456",labour_id="Hello",marital_status=1,name="ei nghon",race="burmese",religion="muslim")
    insert.save()
    cluster.shutdown()
    return HttpResponse("Hello world")
'''

#def index(request):
    #return render(request, 'index.html')

def index(request):
    return render(request, 'form_component.html')

#return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request,'home.html')

def indexform(request2):
    return render(request2, 'indexform.html')

def indexnewform(request2):
    return render(request2, 'indexnewform.html')

def add_person(request):
    submitted = False
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            print("save")
            return HttpResponseRedirect('/add_person/?submitted=True')
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_person.html', {'form': form, 'submitted': submitted})
#return HttpResponse("DONE")


def show_data(request):
    
    return render( request, 'show_data.html',{'street_name':'ရွာလယ်လမ်း','TestModel':list(TestModel.objects.filter(street='ရွာလယ်လမ်း')),'t1':list(TestModel.objects.filter(street='မာဃလမ်းသွယ်'))})


def table_test(request):
   
    #return render( request, 'table.html')
    return render(request,'show_data.html')

def delete_a_person(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))
        c.delete();
        return HttpResponseRedirect('/delete_a_person/?submitted=True')

    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'delete_person.html', {'form': form, 'submitted': submitted})

def request_approval(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))

        #font_file = 'C:\\Users\\user\\Desktop\\Active_OSS_master\\sun_test\\polls\\Pyidaungsu.ttf'
        #pdfmetrics.registerFont(TTFont('Pyidaungsu', font_file))
        pdfmetrics.registerFont(TTFont('Pyidaungsu', 'Pyidaungsu.ttf'))
        
        
        addMapping('Pyidaungsu', 0, 0, 'Pyidaungsu')
        addMapping('Pyidaungsu', 0, 1, 'Pyidaungsu')

        
        
        response = HttpResponse(content_type='application/pdf;charset=utf-8')
        response['Content-Disposition'] = 'inline; filename="desktop/mypdf1.pdf"'
        
        width, height = defaultPageSize

#actual content
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        next_line='\n'
        pdf_content=u"မင်္ဂလာဒုံမြို့နယ်----------------"+next_line+"စာအမှတ်၊     1/သဃအ-ရကအ/၂၀ -------------\nရက်စွဲ၊"+timestampStr+'\n------------------အကြောင်းအရာ။    ထောက်ခံချက်--------------------------------------------------- \n\n'+c.township+'..မြို့နယ်၊..'+c.ward+'..ကျေးရွာ..'+c.street+'လမ်း၊'+'  '+c.home_no+'အမှတ် ..'+'  '+'တွင်နေထိုင်သော (အဘ)ဦး'+c.father_name+'၏ ...သား/သမီးဖြစ်သူ မောင်/မ'+c.name +' ... နိုင်ငံသားစိစစ်ရေးကဒ်ပြားအမှတ်'+c.nrc + '...ကိုင်သောသူသည် ကျေးရွာအုပ်စုအတွင်း...အမှန်တကယ်နေထိုင်ကြောင်းကို...အပိုင်ဆယ်အိမ်မှူး/ရာအိမ်မှူး ၏ထောက်ခံချက်အရ ...မှန်ကန်ကြောင်း ထပ်ဆင့်ထောက်ခံအပ်ပါသည်။'
        print(pdf_content)
        pdf_content.replace("\n", "<br />")
        #a = pdf_content.decode("utf-8", "strict")  
        styles = getSampleStyleSheet()
        styles["Title"].fontName = 'Pyidaungsu'
        para = Paragraph(pdf_content, styles["Title"])
        #para = Paragraph(para, styles["Title"])
        
        #canvas.setFont('Pyidaungsu', 32)
        canv = canvas.Canvas('approval.pdf')

        para.wrap(width, height)
        para.drawOn(canv, 0, height/2)

        canv.showPage()
        canv.save()
    
        return response
    
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'request_approval.html', {'form': form, 'submitted': submitted})


def update_person(request):
    submitted = False
    if request.method == 'POST':
        form = PersonForm(request.POST)
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))
    #    c.labour_id=aa.get('attribute')

        attribute=aa.get('attribute')
        setattr(c, attribute, aa.get('value'))
        c.save();
        return HttpResponseRedirect('/update_person/?submitted=True')

    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'update_person.html', {'form': form, 'submitted': submitted})


#pdf generation testing
def request_crime_record(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST

        #totalcrime=CrimeRecord.objects.get(criminal_nrc=aa.get('nrc')).count()

        response = HttpResponse(content_type='application/pdf;charset=utf-8')
        response['Content-Disposition'] = 'inline; filename="desktop/mypdf1.pdf"'
        font_file = 'Pyidaungsu.ttf'
        pdfmetrics.registerFont(TTFont('Pyidaungsu', font_file))
        addMapping('Pyidaungsu', 0, 0, 'Pyidaungsu')
        width, height = defaultPageSize

    #actual content
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        
        try:
            totalcount=CrimeRecord.objects.filter(criminal_nrc=aa.get('nrc')).count()
            print("totalcount",totalcount)
            c = CrimeRecord.objects.get(criminal_nrc=aa.get('nrc'))
            #print(c)

        except:
            totalcount=0

        if (totalcount>=1):
            print("Criminal")
            next_line='\n'
           # totalcount_str=str(totalcount)
            pdf_content=u"မင်္ဂလာဒုံမြို့နယ်--------------------------------"+next_line+"စာအမှတ်၊     1/သဃအ-ရကအ/၂၀ -------------\nရက်စွဲ၊"+timestampStr+'\n---------------------အကြောင်းအရာ။    ထောက်ခံချက်--------------------------------------------------- \n\n'+c.township+'..မြို့နယ်၊..'+c.ward+'..ကျေးရွာ..'+c.street+'လမ်း၊'+'  '+c.number+'အမှတ် ..'+'  '+'တွင်နေထိုင်သော (အဘ)ဦး၏ ...သား/သမီးဖြစ်သူ မောင်/မ'+c.criminal_name +' ... နိုင်ငံသားစိစစ်ရေးကဒ်ပြားအမှတ်'+c.criminal_nrc + '...ကိုင်သောသူသည် ကျေးရွာအုပ်စုအတွင်း...ကျေးရွာအုပ်စုအတွင်း ၌'+'      ပြစ်မှု၊ဥပဒေပုဒ်မ('+ c.potema+'  ) ဖြင့် အမှန်တကယ်ပြစ်မှုကျူးလွန်ထားသူဖြစ်ကြောင်းကို...အပိုင်ဆယ်အိမ်မှူး/ရာအိမ်မှူး ၏ထောက်ခံချက်အရ ...မှန်ကန်ကြောင်း ထပ်ဆင့်ထောက်ခံအပ်ပါသည်။'
            pdf_content.replace("\n", "<br />")

            styles = getSampleStyleSheet()
            styles["Title"].fontName = 'Pyidaungsu'
            para = Paragraph(pdf_content, styles["Title"])
            canv = canvas.Canvas('crime_record1.pdf')

            para.wrap(width, height)
            para.drawOn(canv, 0, height/2)

            canv.showPage()
            canv.save() 

        elif(totalcount==0):
            print("No crime_record")
            
            next_line='\n'
            pdf_content=u"မင်္ဂလာဒုံမြို့နယ်--------------------------------"+next_line+"စာအမှတ်၊     1/သဃအ-ရကအ/၂၀ -------------\nရက်စွဲ၊"+timestampStr+'\n---------------------အကြောင်းအရာ။    ထောက်ခံချက်--------------------------------------------------- \n\n'+aa.get('nrc')+'သည် ပြစ်မှုကင်းစင်ကြောင် ကျေးကျေးရွာအုပ်စုအတွင်း...ကျေးရွာအုပ်စုအတွင်း...အပိုင်ဆယ်အိမ်မှူး/ရာအိမ်မှူး ၏ထောက်ခံချက်အရ ...မှန်ကန်ကြောင်း ထပ်ဆင့်ထောက်ခံအပ်ပါသည်။'
            pdf_content.replace("\n", "<br />")

            styles = getSampleStyleSheet()
            styles["Title"].fontName = 'Pyidaungsu'
            para = Paragraph(pdf_content, styles["Title"])
            canv = canvas.Canvas('crime_record2.pdf')

            para.wrap(width, height)
            para.drawOn(canv, 0, height/2)

            canv.showPage()
            canv.save()    
           

        return response
    
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'request_crime_record.html', {'form': form, 'submitted': submitted})

  
    
    
def data_visualization(request):

  #  totalcount=list(TestModel.objects.get(ward='စမ်းကြီးဝ'))

    totalcount_gent=TestModel.objects.filter(gender='ကျား').count()
    totalcount_lady=TestModel.objects.filter(gender='မ').count()

    total_teacher=TestModel.objects.filter(occupation='ျောင်းဆရာမ').count()
    total_merchant=TestModel.objects.filter(occupation='ကုန်သည်').count()
    total_engineer=TestModel.objects.filter(occupation='အင်ဂျင်နီယာ').count()
    total_unpaid=TestModel.objects.filter(occupation='မှီခို').count()
    total_doctor=TestModel.objects.filter(occupation='ဆရာဝန်').count()

    total_buddhist=TestModel.objects.filter(religion='ဗုဒ္ဓ').count()
    total_christian=TestModel.objects.filter(religion='ခရစ်ယာန်').count()
    total_islam=TestModel.objects.filter(religion='အစ္စလာမ်').count()


    b=5000
    religion_json_string=json.dumps({'chart':{ "caption": "Data chart based on religion","subCaption" : "for all population in database", "showValues":"1","showPercentInTooltip" : "0","numberPrefix" : "","enableMultiSlicing":"1","theme": "fusion"},'data':[{ "label": "buddist","value": total_buddhist},{"label": "Hindu","value": 50},{"label": "christian","value":total_christian },{"label": "Islam","value": total_islam}]})
    occupation_json_string=json.dumps({'chart':{ "caption": "Data chart based on occupation","subCaption" : "for all population in database", "showValues":"1","showPercentInTooltip" : "0","numberPrefix" : "","enableMultiSlicing":"1","theme": "fusion"},'data':[{ "label": "teacher","value": total_teacher},{"label": "marchant","value": total_merchant},{"label": "engineer","value": total_engineer},{"label": "unpaid job","value": total_unpaid}]})
    gender_json_string=json.dumps({'chart':{ "caption": "Data chart based on gender","subCaption" : "for all population in database", "showValues":"1","showPercentInTooltip" : "0","numberPrefix" : "","enableMultiSlicing":"1","theme": "fusion"},'data':[{ "label": "Male","value": totalcount_gent},{"label": "Female","value": totalcount_lady}]})
    # Create an object for the column2d chart using the FusionCharts class constructor
    gender_pie3d = FusionCharts("pie3d", "ex1" , "100%", "400", "chart-1", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                        gender_json_string)
    occupation_chart=FusionCharts("column2D", "ex2" , "100%", "400", "chart-2", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                        occupation_json_string)
    religion_chart=FusionCharts("pie3d", "ex3" , "100%", "400", "chart-3", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                        religion_json_string)
    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return render(request, 'data_visualization.html', {'output' : gender_pie3d.render(),'output2':occupation_chart.render(),'output3':religion_chart.render()})



def register_crime_record(request):
    submitted = False
    if request.method == 'POST':
        form = CrimeRecordForm(request.POST)
        if form.is_valid():
            form.save()
            print("save")
            return HttpResponseRedirect('/register_crime_record/?submitted=True')
    else:
        form = CrimeRecord()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'crime_record.html', {'form': form, 'submitted': submitted})


'''
def select_person(request):
   if request.method == 'POST':
        form = PersonForm(request.POST)
        aa = request.POST
    #    c.labour_id=aa.get('attribute')

        attribute=aa.get('attribute')
        return HttpResponseRedirect('/get_a_person/?submitted=True')

    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True

    return render( request, 'retrieve_person.html',{'TestModel':list(TestModel.objects.get(nrc="12/mgdn(naing)170361"))})

 
'''
def login(request):


    submitted = False
    if request.method == 'POST':
        #form=AdminForm(request.POST)
        inputdata = request.POST.copy()
        name = inputdata.get('username')
        pwd = inputdata.get('password')
        db_name="admin"
        db_pwd="admin"
        
        if name==db_name and pwd==db_pwd:
           # request.session['username'] = name
            return HttpResponseRedirect('/data_visualization/')
            #return render(request,"/admin/")
            #return HttpResponse(request.session['username'])
            #return HttpResponse("session created!")
        else:
            return HttpResponseRedirect('/login/?submitted=False')
    else:
        #form = Admin()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,"login.html")
   