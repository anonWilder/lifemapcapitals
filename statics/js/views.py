from django.shortcuts import render, redirect
# from weasyprint import HTML, CSS
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
# from wkhtmltopdf.views import PDFTemplateView,PDFTemplateResponse
from functools import wraps
import psycopg2
# import qrcode
import base64
import random
import json
from PIL import  Image
from io import BytesIO
from . import myclasss
import requests
import uuid
import os
import inspect
from django.views.decorators.csrf import csrf_exempt
import datetime

from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.views.generic import View


password = "EedcOsita@123"
host = "74.208.168.47"
port = "5432"
database = "EEDCLIVE"
user = "postgres"

def pdf_generation(request):
    # html_template = get_template('report/print.html')
    # pdf_file = HTML('http://74.208.145.137:8072/print/').write_pdf(stylesheets=[CSS(settings.STATICFILES_DIRS[0]+'/bootstrap.css'),CSS(settings.STATICFILES_DIRS[0]+'/print.css'),"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])
    # response = HttpResponse(pdf_file, content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="home_page.pdf"'
                name = "bill_report.pdf"
                cr = connection = myclasss.Connect().postgresConnect()
                if request.GET.get('type') == 'marketer':
                    cr.execute("SELECT bill.id,bill.create_date as create_date,c.id as customer_id,c.name,c.meter_no,class.name as tariff,class.tariff as tariff_rate,c.acc_no as account_no,c.credit as credit,c.old_acc_no,c.phone,c.street as address,d.name as district,bill.e_year as year,bill.e_month as month_num, bill.e_consumed,c.credit as arrears,(bill.e_consumed  * class.tariff) + bill.adjustment as rate, ((bill.e_consumed  * class.tariff) + (bill.e_consumed * class.tariff * case when bill.create_date > '2019-31-01' then 0.075 else 0.05)) as amount,bill.previous_read,bill.current_read,c.multiplicity,f.name as feeder,t.name as transformer,m.name as marketer_name,m.marketer_phone as marketer_phone from res_partner c LEFT JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN marketer m on m.id = c.marketer LEFT JOIN res_district d on d.id = c.district LEFT JOIN customer_class class on class.id = c.customer_class LEFT JOIN feeder_customer_details bill on bill.e_month = %s and bill.e_year = %s and bill.customer_ids = c.id where c.marketer = %s and c.customer_category = '%s' and e_consumed > 0 and bill.id is not null" % (request.GET.get('month'),request.GET.get('year'),request.GET.get('id'),request.GET.get('category')))
                elif request.GET.get('type') == 'books':
                    cr.execute("SELECT bill.id,bill.create_date as create_date,c.id as customer_id,c.name,c.meter_no,class.name as tariff,class.tariff as tariff_rate,c.acc_no as account_no,c.credit as credit,c.old_acc_no,c.phone,c.street as address,d.name as district,bill.e_year as year,bill.e_month as month_num, bill.e_consumed,c.credit as arrears,(bill.e_consumed  * class.tariff) + bill.adjustment as rate, ((bill.e_consumed  * class.tariff) + (bill.e_consumed * class.tariff * case when bill.create_date > '2019-31-01' then 0.075 else 0.05)) as amount,bill.previous_read,bill.current_read,c.multiplicity,f.name as feeder,t.name as transformer,m.name as marketer_name,m.marketer_phone as marketer_phone from res_partner c LEFT JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN marketer m on m.id = c.marketer LEFT JOIN res_district d on d.id = c.district LEFT JOIN customer_class class on class.id = c.customer_class LEFT JOIN feeder_customer_details bill on bill.e_month = %s and bill.e_year = %s and bill.customer_ids = c.id where c.book_id = %s and c.customer_category = '%s' and e_consumed > 0 and bill.id is not null" % (request.GET.get('month'),request.GET.get('year'),request.GET.get('id'),request.GET.get('category')))
                records = cr.fetchall() 
                month = ['January','February','March','April','May','June','July','August','September','October','November','December']
                for i in range(len(records)):
                        if records[i]['month_num'] == 2 and records[i]['year'] == 2020:
                            records[i]['vat'] = '{:,.2f}'.format(round(records[i]['rate'] * 0.05,2))
                        else:
                            records[i]['vat'] = '{:,.2f}'.format(round(records[i]['rate'] * 0.075,2))
                        prev_month = int(records[i]['month_num']) - 1
                        prev_year = records[i]['year']
                        records[i]['month'] = month[int(records[i]['month_num']) - 1]
                        records[i]['bill_month'] = month[int(records[i]['month_num']) - 2]
                        if prev_month == 0:
                                prev_month = 12
                                prev_year = int(records[i]['year']) - 1
                        # cr = self._cr
                        # bill_prev = self.env['feeder.customer.details'].search([('customer_ids','=',records[i]['customer_id']),('e_month','=',prev_month),('e_year','=',prev_year)],order='id desc')
                        cr.execute("SELECT e_consumed,bill.create_date,(e_consumed * cl.tariff) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and e_month = %s  and e_year = %s" % (records[i]['customer_id'],prev_month,prev_year))     
                        bill_prev = cr.fetchall()
                        b_rate = 0
                        arrears = 0
                        
                        bill_prev_create_date = False
                        if len(bill_prev) == 0:
                                bill_prev_create_date = '%s-%s-06' % (prev_year,prev_month)
                        else:
                                bill_prev_create_date = bill_prev[0]['create_date']
                                b_rate = bill_prev[0]['rate']

                        cr.execute("SELECT payment_date,amount from account_payment where partner_id = '%s' and payment_date Between '2019-07-01' and  '%s' and payment_date != '%s' and bill_description = 'bill' order by payment_date desc" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))     
                        july_payment = cr.fetchall()
                        

                        cr.execute("SELECT sum((e_consumed * cl.tariff) + (e_consumed * cl.tariff * 0.05)) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and bill.create_date Between '2019-07-01' and '%s' and bill.create_date != '%s'" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))      
                        # print("SELECT sum((e_consumed * cl.tariff) + (e_consumed * cl.tariff * 0.05)) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and bill.create_date Between '2019-07-01' and '%s' and bill.create_date != '%s'" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))
                        prev_econsumed = cr.fetchall()
                        print(prev_econsumed)
                        try:
                                july_balance = float(prev_econsumed[0]['rate']) + float(records[i]['credit'])
                        except Exception as e:
                                july_balance = records[i]['credit']
            
                        for j_pay in july_payment:
                                july_balance = float(july_balance) - float(j_pay['amount'])
                                #July Payment and Arrears
                                #August Payment and Arrears
                                #September Payment and Arrears
                        cr.execute("SELECT payment_date,amount from account_payment where partner_id = '%s' and payment_date Between '%s' and  '%s' and bill_description = 'bill' order by payment_date asc" % (records[i]['customer_id'],bill_prev_create_date,records[i]['create_date']))     
                        bill_payment = cr.fetchall()
            
                        prev = 0
                        if True:
                                for b in bill_prev:
                                        prev = prev + round(b_rate + (b_rate * 0.05));
                                        a_to_use = july_balance
                                        records[i]['arrears'] = (float(a_to_use) + float(prev))
                                        records[i]['net_arrears'] = '{:,.2f}'.format((float(a_to_use) + float(prev)))

                                        arrears = records[i]['arrears']
            
                        payment_amount = 0
                        if True:
                                for pay in bill_payment:        
                                        records[i]['payment_date'] = pay["payment_date"]
                                        payment_amount += pay["amount"]
                                        arrears = float(arrears) - float(pay["amount"])
                        
                        records[i]['payment_amount'] = '{:,.2f}'.format(payment_amount)
            
                        # records[i]['arrears'] = records[i]['arrears'] - elec_total
                        # print(elec_total)
                        records[i]['arrears'] = '{:,.2f}'.format(arrears)
                        records[i]['vat'] = '{:,.2f}'.format(round(records[i]['rate'] * 0.05,2))
                        records[i]['amount'] = '{:,.2f}'.format(round(records[i]['amount']))
                        records[i]['total_pay'] = '{:,.2f}'.format(round(arrears +  round(records[i]['rate'],2) + round(records[i]['rate'] * 0.05,2),2))
                        records[i]['contact'] = 'Customer Name: %s \n Old Account Number: %s \n Customer Account Number: %s \n Arrears: %s \n Month Due: %s \n' % (records[i]['name'],records[i]['old_acc_no'],records[i]['account_no'],records[i]['arrears'],records[i]['amount'])
                        data_contact = records[i]['contact']
                        contact = str(base64.b64encode(data_contact.encode("utf-8")),"utf-8")
                        encode2 = str(base64.b64encode(contact.encode("utf-8")),"utf-8")
                        encode3 = str(base64.b64encode(encode2.encode("utf-8")),"utf-8")
                        encode4 = str(base64.b64encode(encode3.encode("utf-8")),"utf-8")
                        records[i]['contact'] = encode4


                        
                context= {'district': 'OGUI DISTRICT','bill': records}
            
                    # context= {'district': 'OGUI DISTRICT'}
                return render(request,'report/print.html',context)
def bill_report(request):
    rec = []
    return render(request,'report/bill_print_form.html',{'data':rec})
def bill_generate(request):
    rec = []
    return render(request,'report/print.html',{'data':rec})
def accountsearch(request):
    rec = []
    return render(request,'report/accountsearch.html',{'data':rec})
def crmforms(request):
    rec = []
    # print("DATA URL"+request.META['PATH_INFO'].split("/")[2])
    url = request.META['PATH_INFO'].split("/")[2]
    return render(request,'report/form/%s' % (url),{'data':rec})

def district(request):
    cr = connection = myclasss.Connect().postgresConnect()
    cr.execute("SELECT distinct name from res_district")
    records = cr.fetchall()
    rec = {'district': records}
    return render(request,'report/select_html.html',rec)
def marketer(request):
    cr = connection = myclasss.Connect().postgresConnect()
    # cr.execute("select row_number() over (order by m.id) as sn, count(bill.id) as count, m.name,m.id,marketer_phone from marketer m LEFT JOIN res_partner c on c.marketer = m.id and c.customer_category = '%s' LEFT JOIN feeder_customer_details bill on bill.customer_ids = c.id and bill.e_month = %s and bill.e_year = %s and bill.e_consumed > 0 LEFT JOIN res_district d on d.id = m.district_id where d.name = '%s' group by m.id,m.name,m.marketer_phone,c.marketer" % (request.POST.get('category'),request.POST.get('month'),request.POST.get('year'),request.POST.get('district')))
    cr.execute("select row_number() over (order by marketer_id) as sn, count(bill.id) as count, marketer_name as name,marketer_id as id,marketer_phone from bill_download bill where customer_category = '%s' and bill.month_num = %s and bill.year = %s and bill.e_consumed > 0  and district = '%s' group by marketer_id,marketer_name,marketer_phone,marketer_id" % (request.POST.get('category'),request.POST.get('month'),request.POST.get('year'),request.POST.get('district')))
    print("select row_number() over (order by marketer_id) as sn, count(b.id) as count, marketer_name as name,marketer_id as id,marketer_phone from bill_download bill left join bill_download b on b.marketer_id = bill.marketer_id where customer_category = '%s' and bill.month_num = %s and bill.year = %s and bill.e_consumed > 0  and district = '%s' group by marketer_id,marketer_name,marketer_phone" % (request.POST.get('category'),request.POST.get('month'),request.POST.get('year'),request.POST.get('district')));
    records = cr.fetchall()
    print()
    for key,val in request.POST.items():
        print('key %s val %s' % (key,val))
    rec = {'marketers': records,'category': request.POST.get('category'),'district': request.POST.get('district'),'month': request.POST.get('month') ,'year': request.POST.get('year') }
    return render(request,'report/marketers.html',rec)
def books(request):
    
     # psycopg2.connect(user = user,
     #                                                                password = password,
     #                                                                host = host,
     #                                                                port = port,
     #                                                                database = database)
    cr = connection = myclasss.Connect().postgresConnect() #connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # cr =
    cr.execute("select row_number() over (order by b.id) as sn, count(bill.id) as count, m.name,b.id,b.name as bkcode,m.marketer_phone  from book_feeder b LEFT JOIN res_partner c on c.book_id = b.id and c.customer_category = '%s' LEFT JOIN marketer m ON m.id = c.marketer LEFT JOIN bill_download bill on bill.customer_id = c.id and bill.month_num = %s and bill.year = %s and bill.e_consumed > 0 LEFT JOIN res_district d on d.id = c.district where d.name = '%s' group by b.id,b.name,m.name,m.marketer_phone,c.marketer" % (request.GET.get('category'),request.GET.get('month'),request.GET.get('year'),request.GET.get('district')))
    records = cr.fetchall()
    rec = {'books': records,'district': request.GET.get('district'),'category': request.GET.get('category'),'month': request.GET.get('month') ,'year': request.GET.get('year') }
    # return JsonResponse(rec,safe=False)
    return render(request,'report/book.html',rec)
def tariffs(request):
    
     # psycopg2.connect(user = user,
     #                                                                password = password,
     #                                                                host = host,
     #                                                                port = port,
     #                                                                database = database)
    cr = connection = myclasss.Connect().postgresConnect() #connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # cr =
    cr.execute("SELECT row_number() over (order by marketer_id) as sn, tariff,count(bill.id) as count, marketer_name as name,marketer_id as id,marketer_phone from bill_download bill where customer_category = '%s' and bill.month_num = %s and bill.year = %s and bill.e_consumed > 0  and district = '%s' group by marketer_id,marketer_name,marketer_phone,marketer_id,tariff order by marketer_name" % (request.GET.get('category'),request.GET.get('month'),request.GET.get('year'),request.GET.get('district')))
    records = cr.fetchall()
    for key,val in request.POST.items():
        print('key %s val %s' % (key,val))
    rec = {'marketers': records,'category': request.GET.get('category'),'district': request.GET.get('district'),'month': request.GET.get('month') ,'year': request.GET.get('year') }
    # return JsonResponse(rec,safe=False)
    return render(request,'report/tariff.html',rec)

def customers_bill(request):
    
     # psycopg2.connect(user = user,
     #                                                                password = password,
     #                                                                host = host,
     #                                                                port = port,
     #                                                                database = database)
    cr = connection = myclasss.Connect().postgresConnect() #connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # cr =
    if request.GET.get('marketer') != 'customer':
        cr.execute("SELECT row_number() over ( order by bill.id) as sn,c.id as id, d.name as district,c.customer_category as category, c.name as name, c.old_acc_no,c.acc_no,to_char(e_consumed,'FM9,999,999,999') as e_consumed, to_char(e_consumed * cl.tariff,'FM9,999,999,999,999') as amount,e_month as month , e_year as year,adjustment as adjust from feeder_customer_details bill LEFT JOIN res_partner c on c.id = bill.customer_ids LEFT JOIN customer_class cl on cl.id = user_class LEFT JOIN res_district d on d.id = c.district  where c.customer_category = '%s' and bill.e_month = %s and bill.e_year = %s and bill.e_consumed > 0 and d.name = '%s' and c.marketer = %s" % (request.GET.get('category'),request.GET.get('month'),request.GET.get('year'),request.GET.get('district'),request.GET.get('marketer')))
    else:
        cr.execute("SELECT row_number() over ( order by bill.id) as sn,c.id as id,d.name as district,c.customer_category as category, c.name as name, c.old_acc_no,c.acc_no,to_char(e_consumed,'FM9,999,999,999') as e_consumed, to_char(e_consumed * bill.tariff_rate,'FM9,999,999,999,999') as amount,e_month as month , e_year as year,adjustment as adjust from feeder_customer_details bill LEFT JOIN res_partner c on c.id = bill.customer_ids LEFT JOIN customer_class cl on cl.id = user_class LEFT JOIN res_district d on d.id = c.district  where c.acc_no = '%s' or c.old_acc_no = '%s' " % (request.GET.get('acc_no'),request.GET.get('acc_no')))
    records = cr.fetchall()
    rec = {'bills': records }
    # return JsonResponse(rec,safe=False)
    return render(request,'report/customers.html',rec)

def success(request):
    rec = {'formid': request.GET.get('formid')}
    return render(request,'report/success.html',rec)
def search(request):
    cr = connection = myclasss.Connect().postgresConnect137()
    cr.execute("select * from %s where id = %s" % (request.POST.get("table"),request.POST.get("id")))
    rec = cr.fetchall()
    rec_data = {}
    for r in rec:
        rec_data = rec[0]

    return JsonResponse(rec_data,safe=False)
def apiCheck(request):
    cr = connection = myclasss.Connect().postgresConnect()
    cr.execute("SELECT juice_acc_no,customer_class,feeder_id,customer_category,old_acc_no,(credit::float + ((arrears::float * tariff::float) + (arrears::float * tariff::float * 0.05))) - payments::float as credit,billdate,name,(billedamount::float * tariff::float * 0.075) as vat,tariff,transformer_id,lastpayamount,(billedamount::float * tariff::float) as billedamount,acc_no,meter_no,street,metering_type,allow_meter,district,id,lastpaydate,phone_no,street2,feeder_code,transformer_code from stage_api where acc_no = '%s'  limit 1" % (request.GET.get("acc_no")))
    rec = cr.fetchall()
    rec_data_dis = rec
    response = JsonResponse(rec,safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    return response
def licence(request):
    cr = connection = myclasss.Connect().postgresConnect()
    cr.execute("SELECT end_date,status from licence_setting order by end_date desc limit 1" )
    rec = cr.fetchall()
    rec_data_dis = rec
    response = JsonResponse(rec,safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    return response



def customersDashboard(request):
    cr = connection = myclasss.Connect().postgresConnect()
    cr.execute("SELECT count(case when r.customer_category = 'MD' then r.id  end) as md_customers,count(case when r.customer_category = 'NON-MD' then r.id end ) as  nmd_customers, count(r.id) as all_customers,count(case when r.create_date between '%s' and '%s' then r.id end ) as new_customers,count(case when r.metering_type = 'prepaid' then r.id  end) as prepaid_customers,count(case when r.metering_type = 'postpaid' then r.id  end) as postpaid_customers,count(case when r.metering_type = 'c_prepaid' then r.id  end) as prepaid_card_customers ,count(case when r.allow_meter = true then r.id  end) as metered_customers, count(case when r.allow_meter = false then r.id  end) as unmetered_customers, count(case when r.bill_status = false then r.id  end) as suspended_customers, count(case when r.bill_status = true then r.id  end) as active_customers from res_partner r" % (request.GET.get("start_date"),request.GET.get("end_date")))
    rec = cr.fetchall()
    rec_data = {}
    for r in rec:
        rec_data = rec[0]
    cr.execute("SELECT d.name as district_name ,count(case when r.customer_category = 'MD' then r.id  end) as md_customers,count(case when r.customer_category = 'NON-MD' then r.id end ) as  nmd_customers, count(r.id) as all_customers,count(case when r.create_date between '%s' and '%s' then r.id end ) as new_customers,count(case when r.metering_type = 'prepaid' then r.id  end) as prepaid_customers,count(case when r.metering_type = 'postpaid' then r.id  end) as postpaid_customers,count(case when r.metering_type = 'c_prepaid' then r.id  end) as prepaid_card_customers ,count(case when r.allow_meter = true then r.id  end) as metered_customers, count(case when r.allow_meter = false then r.id  end) as unmetered_customers, count(case when r.bill_status = false then r.id  end) as suspended_customers, count(case when r.bill_status = true then r.id  end) as active_customers from res_partner r left join res_district d on d.id = r.district  where d.id is not null group by d.name" % (request.GET.get("start_date"),request.GET.get("end_date")))
    rec = cr.fetchall()
    rec_data_dis = rec

    cr.execute("SELECT feeder.name as feeder_name ,count(case when r.customer_category = 'MD' then r.id  end) as md_customers,count(case when r.customer_category = 'NON-MD' then r.id end ) as  nmd_customers, count(r.id) as all_customers,count(case when r.create_date between '%s' and '%s' then r.id end ) as new_customers,count(case when r.metering_type = 'prepaid' then r.id  end) as prepaid_customers,count(case when r.metering_type = 'postpaid' then r.id  end) as postpaid_customers,count(case when r.metering_type = 'c_prepaid' then r.id  end) as prepaid_card_customers ,count(case when r.allow_meter = true then r.id  end) as metered_customers, count(case when r.allow_meter = false then r.id  end) as unmetered_customers, count(case when r.bill_status = false then r.id  end) as suspended_customers, count(case when r.bill_status = true then r.id  end) as active_customers from res_partner r left join feeder_feeder feeder on feeder.id = r.feeder_id  where feeder.id is not null group by feeder.name" % (request.GET.get("start_date"),request.GET.get("end_date")))
    rec = cr.fetchall()
    rec_data_feeder = rec

    
    # cr.execute("SELECT book.name as book_name ,count(case when r.customer_category = 'MD' then r.id  end) as md_customers,count(case when r.customer_category = 'NON-MD' then r.id end ) as  nmd_customers, count(r.id) as all_customers,count(case when r.create_date between '%s' and '%s' then r.id end ) as new_customers,count(case when r.metering_type = 'prepaid' then r.id  end) as prepaid_customers,count(case when r.metering_type = 'postpaid' then r.id  end) as postpaid_customers,count(case when r.metering_type = 'c_prepaid' then r.id  end) as prepaid_card_customers ,count(case when r.allow_meter = true then r.id  end) as metered_customers, count(case when r.allow_meter = false then r.id  end) as unmetered_customers, count(case when r.bill_status = false then r.id  end) as suspended_customers, count(case when r.bill_status = true then r.id  end) as active_customers from res_partner r left join book_feeder book on book.id = r.book_id  where book.id is not null group by book.name" % (request.GET.get("start_date"),request.GET.get("end_date")))
    # rec = cr.fetchall()
    # rec_data_book = rec
    
    # cr.execute("SELECT trans.name as transformer_name ,count(case when r.customer_category = 'MD' then r.id  end) as md_customers,count(case when r.customer_category = 'NON-MD' then r.id end ) as  nmd_customers, count(r.id) as all_customers,count(case when r.create_date between '%s' and '%s' then r.id end ) as new_customers,count(case when r.metering_type = 'prepaid' then r.id  end) as prepaid_customers,count(case when r.metering_type = 'postpaid' then r.id  end) as postpaid_customers,count(case when r.metering_type = 'c_prepaid' then r.id  end) as prepaid_card_customers ,count(case when r.allow_meter = true then r.id  end) as metered_customers, count(case when r.allow_meter = false then r.id  end) as unmetered_customers, count(case when r.bill_status = false then r.id  end) as suspended_customers, count(case when r.bill_status = true then r.id  end) as active_customers from res_partner r left join feeder_transformer trans on trans.id = r.transformer_id  where trans.id is not null group by trans.name" % (request.GET.get("start_date"),request.GET.get("end_date")))
    # rec = cr.fetchall()
    # rec_data_trans = rec

    cr.execute("SELECT tariff.name as tariff_name ,count(case when r.customer_category = 'MD' then r.id  end) as md_customers,count(case when r.customer_category = 'NON-MD' then r.id end ) as  nmd_customers, count(r.id) as all_customers,count(case when r.create_date between '%s' and '%s' then r.id end ) as new_customers,count(case when r.metering_type = 'prepaid' then r.id  end) as prepaid_customers,count(case when r.metering_type = 'postpaid' then r.id  end) as postpaid_customers,count(case when r.metering_type = 'c_prepaid' then r.id  end) as prepaid_card_customers ,count(case when r.allow_meter = true then r.id  end) as metered_customers, count(case when r.allow_meter = false then r.id  end) as unmetered_customers, count(case when r.bill_status = false then r.id  end) as suspended_customers, count(case when r.bill_status = true then r.id  end) as active_customers from res_partner r left join customer_class tariff on tariff.id = r.customer_class  where tariff.id is not null group by tariff.name" % (request.GET.get("start_date"),request.GET.get("end_date")))
    rec = cr.fetchall()
    rec_data_tariff = {}
    # for r in rec:
    rec_data_tariff = rec
    customers = {'customers':rec_data,'district': rec_data_dis,'tariff': rec_data_tariff,'feeder': rec_data_feeder}
    response = JsonResponse(customers,safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    return response

def paymentsDashboard(request):
    cr = connection = myclasss.Connect().postgresConnect()
    cr.execute("SELECT count(case when r.customer_category = 'MD' then r.id  end) as md_customers,count(case when r.customer_category = 'NON-MD' then r.id end ) as  nmd_customers, count(r.id) as all_customers,count(case when r.create_date between '%s' and '%s' then r.id end ) as new_customers,count(case when r.metering_type = 'prepaid' then r.id  end) as prepaid_customers,count(case when r.metering_type = 'postpaid' then r.id  end) as postpaid_customers,count(case when r.metering_type = 'c_prepaid' then r.id  end) as prepaid_card_customers ,count(case when r.allow_meter = true then r.id  end) as metered_customers, count(case when r.allow_meter = false then r.id  end) as unmetered_customers, count(case when r.bill_status = false then r.id  end) as suspended_customers, count(case when r.bill_status = true then r.id  end) as active_customers from res_partner r" % (request.GET.get("start_date"),request.GET.get("end_date")))
    rec = cr.fetchall()
    rec_data = {}
    for r in rec:
        rec_data = rec[0]
    customers = {'payments':rec_data}
    response = JsonResponse(customers,safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    return response

def unique_code(table,col):
    unique = True
    code = 0
    while unique:
        code = random.randint(10000000,99999999)
        data = myclasss.Connect(host="74.208.145.137",user="postgres",password="EedcOsita@123",database="EEDCLIVE").select_single("SELECT id from %s where %s = '%s'" % (table,col,code))
        unique = len(data) > 0
    return code

def customer(request):
    rec = {'formid': unique_code('new_connection','app_no'),'id':''}

    for key,val in request.GET.items():
        if key == 'id':
            rec['id'] = val
        if key == 'formid':
            rec['formid'] = val
    return render(request,'report/eedc form/examples/index.html',rec)


def transformer(request,id):
    cr = myclasss.Connect().postgresConnect()
    cr.execute("SELECT id,name from feeder_transformer where feeder_id = %s " % (id))
    transformer = cr.fetchall()
    rec = {'transformer': transformer}

    return JsonResponse(rec,safe=True)
    
def declaration(request):
    rec = {'formid': unique_code('new_connection','app_no'),'id':''}
    cr = myclasss.Connect().postgresConnect()
    cr.execute("SELECT id,name from feeder_feeder order by name")
    feeder = cr.fetchall()
    cr.execute("SELECT id,name from feeder_transformer order by name")
    transformer = cr.fetchall()
    cr.execute("SELECT id,name from injection_substation order by name")
    substation = cr.fetchall()
    
    for key,val in request.GET.items():
        if key == 'id':
            rec['id'] = val
        if key == 'formid':
            #cr = connection = myclasss.Connect().postgresConnect()
            cr.execute("SELECT id, %s as formid,state,concat(a_surname,' ',a_other_name) as name, a_address as street, a_mobile as mobile from new_connection where app_no = '%s'" % (val,val))
            rec = cr.fetchall()
            if len(rec) == 0:
                return render(request,'report/eedcFOrm/index-2.html',{})
            # rec['formid'] = val
    try:
        if rec[0]['state'] != 'flex':
            return HttpResponse('<p style="color: red"><b>Error:</b> Form Not Approved For Feasibility Entry</p>') 
        rec[0]['feeder'] = feeder
        rec[0]['transformer'] = transformer
        rec[0]['substation'] = substation
        return render(request,'report/eedc form/examples/declaration.html',rec[0])
    except Exception as e:
        return render(request,'report/eedcFOrm/index-2.html',{})
def landlord(request):
    rec = {'formid': random.randint(10000000,99999999),'id':''}
    for key,val in request.GET.items():
        if key == 'id':
            rec['id'] = val
        if key == 'formid':
            cr = connection = myclasss.Connect().postgresConnect()
            cr.execute("SELECT id, %s as formid,concat(a_surname,' ',a_other_name) as name from new_connection where app_no = '%s'" % (val,val))
            rec = cr.fetchall()
            if len(rec) == 0:
                return render(request,'report/eedcFOrm/index-2.html',{'message':'Form ID not found'})
            # rec['formid'] = val
    return render(request,'report/eedc form/examples/landlord.html',rec[0])

# def downloadform(request):
#     rec = {'formid': random.randint(10000000,99999999),'id':''}
#     formid = ''
#     for key,val in request.GET.items():
#         if key == 'id':
#             rec['id'] = val
#         if key == 'formid':
#             cr = connection = myclasss.Connect().postgresConnect()
#             cr.execute("SELECT id, %s as formid,a_surname,a_other_name,a_address,a_landmark,a_lga,premise_type,a_o_premise_type,premise_use,prev_meter_no,prev_address,employer_name,prev_acc_no,district,employer_landmark,employer_address,employer_lga,a_mobile,a_telephone,a_email,app_three_p_id,app_three_p_id_num,a_means_id from new_connection where app_no = '%s'" % (val,val))
#             rec = cr.fetchall()
#             if len(rec) == 0:
#                 return render(request,'report/eedcFOrm/index-2.html',{'message':'Form ID not found'})
#             formid = val

#     response = PDFTemplateResponse(request=request,
#                                     template='report/form.html',
#                                     filename='form_%s .pdf' % (val),
#                                     context= rec[0],
#                                     show_content_in_browser=False,
#                                     cmd_options={'margin-top': 20,},
#                                     )
  
#     return response
def landingpage74(request):
    rec = {'formid': random.randint(10000000,99999999),'id':''}
    return render(request,'report/eedcFOrm/index-2.html',rec)

def addCustomers(request):
    try:
        print(request.POST.items())
        data = {}
        edit = False
        edit_val = ''
        for key,val in request.POST.items():
            data[key] = val 
            if key == "edit":
                edit = True
                edit_val = request.POST.get('id')
        print(data)
        if edit == False:
            use = connection = myclasss.Connect().insert(data)
        else:
            if request.POST.get('appli') != None:
                # print(request.POST.get('appli'))
                for val in json.loads(request.POST.get('appli')):
                    print(val)
                    myclasss.Connect().insert(val)      
            use = connection = myclasss.Connect().update(data,'id',edit_val)
        rec = use
        return HttpResponse(rec)
    except Exception as e:
        return HttpResponse(str(e))




def addCustomers153(request):
    print(request.POST.items())
    data = {}
    edit = False
    edit_val = ''
    for key,val in request.POST.items():
        data[key] = val 
        if key == "edit":
            edit = True
            edit_val = request.POST.get('id')
    print(data)
    if edit == False:
        use = connection = myclasss.Connect(host="74.208.145.153",database="ENUGUBACK",password="EedcOsita").insert(data)
    else:
        if request.POST.get('appli') != None:
            # print(request.POST.get('appli'))
            for val in json.loads(request.POST.get('appli')):
                print(val)
                myclasss.Connect().insert(val)      
        use = connection = myclasss.Connect().update(data,'id',edit_val)
    rec = use
    return HttpResponse(rec)

def login_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if 'acc_no' in request.session.keys():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/Login')
    return wrap

def connector():
    return myclasss.Connect(host='70.35.204.21',user='postgres',password='EedcOsita@123',database='EEDCBACK21',port='5432')

def connector137():
    return myclasss.Connect(host='74.208.145.137',user='postgres',password='EedcOsita@123',database='EEDCLIVE',port='5432')

def portalsearch(request):
    cr = connection = connector137()
    
    rec = cr.select_single("select * from %s where id = '%s'" % (request.POST.get("table"),request.session['acc_id']))
    rec_data = rec
    # for r in rec:
    #   rec_data = rec[0]

    return JsonResponse(rec_data,safe=False)
@csrf_exempt
def portalsearch_api(request):
    cr = connection = connector137()
    # rec = cr.select_single("select * from %s where id = '%s'" % (request.POST.get("table"),request.POST.get('acc_id')))
    rec = cr.select_single("select * from "+ request.POST.get("table") +" where id = "+ request.POST.get('acc_id') +"")
    rec_data = rec
    # for r in rec:
    #   rec_data = rec[0]

    return JsonResponse(rec_data,safe=False)
def login(request):
    try:
        user_name = request.POST.get('username','')
        password = request.POST.get('password','')
        # print("SELECT acc_no from res_partner where acc_no = '%s' and password = '%s' or old_acc_no = '%s' and password = '%s' or meter_no = '%s' and password = '%s'  " % (request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password")))
        rec = connection = connector137().select_single("SELECT acc_no,id,email,name, metering_type from res_partner where acc_no = '%s' and password = '%s' or old_acc_no = '%s' and password = '%s' or meter_no = '%s' and password = '%s' or juice_acc_no = '%s' and password = '%s'  " % (request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password")))
        if len(rec) > 0:    
            request.session['acc_no'] = rec['acc_no']
            request.session['acc_id'] = rec['id']
            request.session['name'] = rec['name']
            request.session['email'] = rec['email']
            request.session['metering_type'] = rec['metering_type']
            
            if 'api' in request.GET.keys():
                return JsonResponse(rec,safe=False)
            return HttpResponse(1)
        else:
            if 'api' in request.GET.keys():
                return JsonResponse([{'message':'Login Details Error!!!'}],safe=False)
            return HttpResponse("Login Details Error!!!")
    except Exception as e:
        return HttpResponse(str(e))


@csrf_exempt
def login_api(request):
    # return JsonResponse([{'message':'Login Details Error!!!'}],safe=False)
    try:
        user_name = request.POST.get('username','')
        password = request.POST.get('password','')
        # rec = connection = connector137().select_single("SELECT acc_no,id,email,name from res_partner where acc_no = '%s' and password = '%s' or old_acc_no = '%s' and password = '%s' or meter_no = '%s' and password = '%s'  " % (request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password")))
        rec = connection = connector137().select_single("SELECT acc_no,id,email,name, metering_type from res_partner where acc_no = '%s' and password = '%s' or old_acc_no = '%s' and password = '%s' or meter_no = '%s' and password = '%s' or juice_acc_no = '%s' and password = '%s'  " % (request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password"),request.POST.get("username"),request.POST.get("password")))
        if len(rec) > 0:    
            request.session['acc_no'] = rec['acc_no']
            request.session['acc_id'] = rec['id']
            request.session['name'] = rec['name']
            request.session['email'] = rec['email']
            request.session['metering_type'] = rec['metering_type']
            
            # if 'api' in request.GET.keys():
            return JsonResponse(rec,safe=False)
            # return HttpResponse(1)
        else:
            # if 'api' in request.GET.keys():
            return JsonResponse([{'message':'Login Details Error!!!'}],safe=False)
            # return HttpResponse("Login Details Error!!!")
    except Exception as e:
        # return JsonResponse([{'message':str(e)}],safe=False)
        return HttpResponse(str(e))


def sign_in(request):
    return render(request, 'report/custormer_portal/sign-in1.html')



def change_password(request):
    rec = connector137().select_single("SELECT id,password from res_partner where id = '%s'" % (request.session['acc_id']))
    return render(request, 'report/custormer_portal/changepassword.html',rec)


def changeaddress(request):
    rec = connector137().select_single("SELECT id,street from stage_api where id = '%s'" % (request.session['acc_id']))
    return render(request, 'report/custormer_portal/changeall.html',rec)

def changephone(request):
    rec = connector137().select_single("SELECT id,street from stage_api where id = '%s'" % (request.session['acc_id']))
    return render(request, 'report/custormer_portal/changephone.html',rec)



def active_user(request):
    rec = connection = connector137().select_single("SELECT name,email,phone from res_partner where acc_no = '%s' or old_acc_no = '%s' or meter_no = '%s'" % (request.session['acc_no'],request.session['acc_no'],request.session['acc_no']))
    return JsonResponse(rec,safe=True)

def get_table(request,sql):
    rec = connection = connector137().selectall(sql)

    print(sql)
    return JsonResponse({"data":rec},safe=False)

def logout(request):
    if 'acc_no' in request.session.keys():
        request.session.pop('acc_no')
    return HttpResponseRedirect('/')
def lock(request):
    return render(request, 'report/custormer_portal/lock1.html')

    
@login_only
def paybill(request):
    rec = connector137().select_single("SELECT c.name,c.wallet,ROUND(cast((billedamount::float * s.tariff_rate::float) as numeric) ,2) as billedamount,ROUND(cast((billedamount::float * s.tariff_rate::float * 0.075) as numeric) ,2) as vat,ROUND(cast((s.credit::float + (case when adjustment::float is null then 0 else adjustment::float end) + arrears::float - payments::float) as numeric) ,2) as credit,ROUND(cast(((billedamount::float * s.tariff_rate::float) + (billedamount::float * s.tariff_rate::float * 0.075) + (s.credit::float + (case when adjustment::float is null then 0 else adjustment::float end) + arrears::float - payments::float)) as numeric) ,2) as total from stage_api s left join res_partner c on c.id = s.id::int  where s.id = '%s'" % (request.session['acc_id']))
    return render(request, 'report/custormer_portal/paybill.html',rec)


    def invoice(request):
        context = {
            "email":request.session['email'],
            "metering_type": request.session['metering_type']
        }
        return render(request, 'report/custormer_portal/invoicing.html',context)

# @data()
@login_only
def account(request):
    context = {'request':request,"email":request.session['email'], "metering_type": request.session['metering_type']}
    return render(request, 'report/custormer_portal/account.html',context)


@login_only
def meter(request):
    context = {'request':request,"email":request.session['email'],"metering_type": request.session['metering_type']}
    return render(request, 'report/custormer_portal/meter.html',context)


@login_only
def billing(request):
    context = {'request':request, "email":request.session['email'], "metering_type": request.session['metering_type']}
    return render(request, 'report/custormer_portal/billing.html',context)

@login_only
def Consumption(request):
    temp_view = connector137().selectall("SELECT a.e_consumed as consume,e_month as month,e_year as year, a.create_date as dat from res_partner b left join feeder_customer_details a on a.customer_ids = b.id where b.id = %s order by a.id desc limit 12" % (request.session['acc_id']))
    view=[]
    for v in temp_view:
        if v['dat'] == None or v['dat'] == False:
            v['dat'] = "%s-%s-01" % (v['year'],v['month'])
        try:
            view.append({
            "consume": v["consume"],
            "date":v["dat"].strftime("%m"),
            "year":v["dat"].strftime("%Y"),
            })
        except Exception as e:
            return HttpResponse("%s %s" % (v['dat'],str(e)))

    context={
        "view":view,
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/consumption.html',context)



@login_only
def new_conection(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/newconection.html',context)

def general_details(request):
    return JsonResponse({},safe=True)
    

@login_only
def history(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/customer_history.html',context)
@login_only
def charges_and_penaltes(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/charges_and_penaltes.html',context)
@login_only
def estimateconsumption(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/estimate_consumption.html',context)
@login_only
def vending(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/vending.html',context)

@login_only
def makepayment(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/payarrears.html',context)




@login_only
def payments(request):
    temp_pay = connector137().selectall("SELECT a.amount as amount, a.payment_date as paydate from res_partner b left join account_payment a on a.partner_id = b.id where b.id = %s and a.bill_description = 'bill' order by a.id desc limit 12" % (request.session['acc_id']))
    pay=[]
    for p in temp_pay:
        pay.append({
            "amount":p["amount"],
            "paydate":p["paydate"].strftime("%m"),
            "payear":p["paydate"].strftime("%Y"),
            "acc_id": request.session['acc_id']
            })
    context={
        "pay":pay,
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/payment.html',context)

@login_only
def transaction(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/prepaidtransaction.html',context)


@login_only
def alltransaction(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/alltransaction.html',context)

@login_only
def dashboard(request):
    # if request.session['metering_type'] == 'prepaid':
    # 	name = "its prepaid ooo"
    res = connector137().select_single("SELECT a.created as date,a.serialnumber as meter,ROUND(cast(a.amount as numeric) ,2) as amount,a.ststoken as token,a.units as energy,a.unit as unit from res_partner b left join prepaid_trans a on a.user_t = b.id where b.id = %s order by a.created desc limit 12" % (request.session['acc_id']))
    pat_view = connector137().selectall("SELECT a.created as dat,a.serialnumber as meter,a.ststoken as token, a.units as consume from res_partner b left join prepaid_trans a on a.user_t = b.id where b.id = %s order by a.created desc limit 12" % (request.session['acc_id']))
    pat_pay = connector137().selectall("SELECT a.amount as amount, a.created as date from res_partner b left join prepaid_trans a on a.user_t = b.id where b.id = %s order by a.created desc limit 12" % (request.session['acc_id']))

    rec = connector137().select_single("SELECT wallet,ROUND(cast(new_arrears as numeric) ,2) as new_arrears,last_pay,ROUND(cast(b_amount as numeric) ,2) as b_amount from res_partner where id = %s" % (request.session['acc_id']))
    temp_view = connector137().selectall("SELECT a.e_consumed as consume,e_month as month,e_year as year, a.create_date as dat from res_partner b left join feeder_customer_details a on a.customer_ids = b.id where b.id = %s order by a.id desc limit 12" % (request.session['acc_id']))
    temp_pay = connector137().selectall("SELECT a.amount as amount, a.payment_date as paydate from res_partner b left join account_payment a on a.partner_id = b.id where b.id = %s and a.bill_description = 'bill' order by a.id desc limit 12" % (request.session['acc_id']))
    try:
        name=[]
        for p in pat_pay:
            if p['date'] == None or p['date'] == False:
                p['date'] = "%s-%s-01"
            
            name.append({
                "amount":p["amount"],
                "date":p["date"],
                # "paydate":p["paydate"].strftime("%Y"),
                })
    except Exception as e:
            print(str(e))
    view=[]
    for v in temp_view:
        if v['dat'] == None or v['dat'] == False:
            v['dat'] = "%s-%s-01" % (v['year'],v['month'])
        try:
            view.append({
            "consume": v["consume"],
            "date":v["dat"].strftime("%m"),
            "year":v["dat"].strftime("%Y"),
            })
        except Exception as e:
            print(str(e))
    pay=[]
    for p in temp_pay:
        pay.append({
            "amount":p["amount"],
            "paydate":p["paydate"].strftime("%m"),
            "payear":p["paydate"].strftime("%Y"),
            })
    context={
        "rec":rec,
        "view":view,
        "pay":pay,
        "ppay":name,
        "res":res,
        "email":request.session['email'],
        "email":request.session['email'],
        "metering_type": request.session['metering_type'],
    } 
    return render(request, 'report/custormer_portal/dashboard.html',context)

# @login_only
@csrf_exempt
def paystack_payment(request,trans_ref,payment_for):

    url = "https://api.paystack.co/transaction/verify/%s" % (trans_ref)
    rec = requests.request('GET',url,headers={'Authorization':'Bearer sk_live_8b0faf614d85452fe4022c08f96489a2d516259d'})
    data = rec.json()

    if 'data' in data.keys():
        if data['data']['status'] == 'success':
            if payment_for == 'wallet':
                response = wallettrans(request.session['acc_id'] if 'api' not in request.GET.keys() else request.GET.get('api'),(data['data']['amount']/100),'credit')
                if response['message'] == 'success':
                    if 'api' not in request.GET.keys():
                        return HttpResponseRedirect('/dashboard')
                    else:
                        return JsonResponse([response],safe=False)
                else:
                    if 'api' not in request.GET.keys():
                        return HttpResponseRedirect('/fundwallet')
                    else:
                        return JsonResponse([response],safe=False)  
            elif payment_for == 'payment':
                response = billpayment(request.session['acc_no'] if 'api' not in request.GET.keys() else request.GET.get('api'),(data['data']['amount']/100),'test_sterling_gateway')
                if response['message'] == 'success':
                    if 'api' not in request.GET.keys():
                        return HttpResponseRedirect('/payments')
                    else:
                        return JsonResponse([response],safe=False)
                else:
                    if 'api' not in request.GET.keys():
                        return HttpResponseRedirect('/paybill')
                    else:
                        return JsonResponse([response],safe=False)
            else:
                response = None
                if 'api' not in request.GET.keys():
                    rec = connector137().select_single("SELECT wallet,new_arrears,juice_acc_no,meter_no from res_partner where id = %s" % (request.session['acc_id']))
                    response = juice_api(rec['juice_acc_no'],rec['meter_no'],(data['data']['amount']/100))
                else:
                    response = juice_api(request.GET.get('api'),request.GET.get('serial'),(data['data']['amount']/100))
                if 'ststoken' in response.keys():
                    if 'api' not in request.GET.keys():
                        return JsonResponse([{"message":"success","ststoken":response['ststoken']}],safe=False)
                    else:
                        return JsonResponse([{"message":"success","ststoken":response['ststoken']}],safe=False)
                else:
                    if 'api' not in request.GET.keys():
                        return JsonResponse([{"message":response['message']}],safe=False)
                    else:
                        return JsonResponse([{"message":response['message']}],safe=False)
    return JsonResponse(data,safe=False)
@csrf_exempt
def wallet_payment(request):
    if 'api' in request.POST.keys():
        rec = connector137().select_single("SELECT wallet,new_arrears,acc_no,id,juice_acc_no,meter_no from res_partner where id = %s" % (request.POST.get('api')))
        if len(rec) == 0:
            return JsonResponse([{'message': 'user error'}],safe=False)
        others = None
        if 'others' in request.POST.keys():
            others = connector137().select_single("SELECT wallet,new_arrears,acc_no,id,juice_acc_no,meter_no from res_partner where id = %s" % (request.POST.get('others')))
            if len(others) == 0:
                return JsonResponse([{'message': 'user error'}],safe=False)
            else:
                rec['acc_no'] = others['acc_no']
                rec['juice_acc_no'] = others['juice_acc_no']
                rec['meter_no'] = others['meter_no']
        if rec['wallet'] > float(request.POST.get('amount')):
            response = wallettrans(rec['id'],float(request.POST.get('amount')),'debit')
            if response['message'] == 'success':
                if 'prepaid' not in request.POST.keys(): 
                    res = billpayment(rec['acc_no'],float(request.POST.get('amount')),'wallet')
                else:
                    res = juice_api(rec['juice_acc_no'],rec['meter_no'],float(request.POST.get('amount')))
                    if 'ststoken' in res.keys():
                        return JsonResponse([{"message":"success","ststoken":res['ststoken']}],safe=False)
                    else:
                        return JsonResponse([{"message":res['message']}],safe=False)
                return JsonResponse([response],safe=False)
            else:
                return JsonResponse([response],safe=False)
        else:
            return JsonResponse([{"error": "Insufficient Balance"}],safe=False)
    else:
        rec = connector137().select_single("SELECT wallet,new_arrears,juice_acc_no,meter_no from res_partner where id = %s" % (request.session['acc_id']))
        if rec['wallet'] > float(request.POST.get('amount')):
            # if 'prepaid' in request.POST.keys():
            #   res = juice_api(rec['juice_acc_no'],rec['meter_no'],float(request.POST.get('amount')))
            #   if 'ststoken' in res.keys():
            #       return HttpResponse(res['ststoken'])
            #   else:
            #       return HttpResponse(res['message'])
            
            response = wallettrans(request.session['acc_id'],float(request.POST.get('amount')),'debit')
            if response['message'] == 'success':
                if 'prepaid' in request.POST.keys():
                    res = juice_api(rec['juice_acc_no'],rec['meter_no'],float(request.POST.get('amount')))
                    if 'ststoken' in res.keys():
                        return HttpResponse("Your Token is %s " % (res['ststoken']))
                    else:
                        return HttpResponse(res['message'])
                
                res = billpayment(request.session['acc_no'],float(request.POST.get('amount')),'wallet')
                return HttpResponse('VALUE INSERTED')
            else:
                return HttpResponse('An Error Occured') 
        else:
            return HttpResponse('Insufficient Balance')

def wallettrans(id,amount,purpose):
    url = "http://74.208.168.47:8069/web/json/wallet.transactions"
    header = {'Authorization':'Basic b3NzeW9nYm9AeWFob28uY29tOkAhI1N0ZXJsaW5nVGVjaDEyMw==','Content-type':'application/json'}
    data =  "{\n\t\"params\": {\n\t\t\t\"partner_id\":%s,\n\"amount\":%s,\n\"type\":\"%s\"\n\t\t  }\n }" %(id,amount,purpose)
    rec = requests.post(url,headers=header,data=data)
    print(rec.text)
    data = rec.json()
    if "result" in data.keys():
        if "Success" in data['result'].keys():
            return {'message':'success'}
        else:
            return {'message': 'failed'}
    else:
        return {'message': 'failed'}
# @login_only
def juice_api(account_num,serialnumber,amount):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    headers = {'Content-Type': 'application/json','User-Agent': user_agent}
    # payload = "{ 'fields' : ['name','partner_id','payment_date','amount']}"
    # mode=balance&account=XXXXXXXXX&submode=detail
    wallet = 'cash'
    # if 'wallet' in request.GET.keys():
    #   wallet = 'wallet'
    
    url = "https://eedc.utiliflex.com/juice4/vending.php?mode=vend&submode=%s&account=%s&serialnumber=%s&amount=%s&return=json" % (wallet,account_num,serialnumber,amount)
    url = url.rstrip()
    cert_file_path = get_txt_path(file='cert.pem')
    key_file_path = get_txt_path(file='key.pem')
    cert = (cert_file_path, key_file_path)
    r = requests.get(url, headers=headers,cert=cert, verify=True, auth=('test','changeme'))
    try:
        data = r.json()
    except Exception as e:
        return r.text
    # print(data)
    return data

def juice_api_api(request,account_num,serialnumber,amount):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    headers = {'Content-Type': 'application/json','User-Agent': user_agent}
    # payload = "{ 'fields' : ['name','partner_id','payment_date','amount']}"
    # mode=balance&account=XXXXXXXXX&submode=detail
    wallet = 'cash'
    if 'wallet' in request.GET.keys():
      wallet = 'wallet'
    
    url = "https://eedc.utiliflex.com/juice4/vending.php?mode=vend&submode=%s&account=%s&serialnumber=%s&amount=%s&return=json" % (wallet,account_num,serialnumber,amount)
    url = url.rstrip()
    cert_file_path = get_txt_path(file='cert.pem')
    key_file_path = get_txt_path(file='key.pem')
    cert = (cert_file_path, key_file_path)
    r = requests.get(url, headers=headers,cert=cert, verify=True, auth=('osita','eedcosita'))
    try:
        data = r.json()
    except Exception as e:
        return HttpResponse(r.text) 
    # print(data)
    return JsonResponse(data,safe=False)

def get_txt_path(file='juice_data_update.txt'):
    directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return os.path.join(directory_path, file)

def billpayment(acc_no,amount,source):
    date = connector137().select_single("SELECT CURRENT_DATE as date")
    url = "http://74.208.168.47:8088/web/json.php"
    header = {'Authorization':'Basic b3NzeW9nYm9AeWFob28uY29tOkVlZGNPc2l0YUAxMjM=','Content-type':'application/json'}
    data =  "{\n\t\"params\": {\n\t\t\t\"partner_id\":%s,\n\"amount\":%s,\n\"name\":\"bill\",\n\"bill_description\":\"bill\",\n\"bill_userid\":\"%s\",\n\"payment_date\":\"%s\",\n\"trans_ref\":\"%s\"\n\t\t  }\n }" %(acc_no,amount,source,date['date'],uuid.uuid4())
    data = {"params":{"amount":amount,"partner_id":acc_no,"trans_ref":str(uuid.uuid4()),"name":"bill","bill_userid":source,"bill_description":"bill","payment_date":str(date['date'])}}
    rec = requests.post(url,headers=header,json=data)
    print(rec.text)
    data = rec.json()
    if "result" in data.keys():
        if "id" in data['result'].keys():
            return {'message':'success'}
        else:
            return {'message': data}
    else:
        return {'message': 'failed'}
    

@login_only
def walet_to_walet(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/waletowalet.html',context)

# @login_only
# def suport(request):
# 	rec = None
# 	if request.method == 'POST':
# 		url = "http://50.21.183.64:8069/web/json/website.support.ticket"
# 		header = {'Authorization':'Basic YWJjQGVudWd1ZGlzY28uY29tOkVudWd1ZGlzY29AMzMz','Content-type':'application/json'}
# 		data = { "params": 
# 				   { "ticket_number_ems": "PI1641215",
# 				     "create_date": "2021-01-25T07:58:25.636Z",
# 				     "category": 117,
# 				     "state": 1,
# 				     "person_name": "Chika",
# 				     "cus_phone": "08150824815",
# 				     "email": "abc@enugudisco.com",
# 				     "description": "Payment is yet to reflect",
# 				     "acc_no": "51/45/21/3275-01",
# 				     "acc_type": "Postpaid",
# 				     "cus_street": "NO 1 RIVER LINEOBED CAMP",
# 				     "created_by": "James",
# 				     "acc_name": "YOUNG COMFORT N.",
# 				     "call_count": 1,
# 				     "priority_id": 2,
# 				     "channel": "Call",
# 				     "subject": "Payment Reconciliation" } }
# 		rec = requests.post(url,headers=header,json=data)
# 		print(rec.text)

# a) SELECT id,name from website_support_ticket_categories order by name

# b) SELECT id,name from website_support_ticket_subcategory where parent_category_id = %s




@login_only
def suport_ticket(request):
    rec = None
    if request.method == 'POST':
        url = "http://50.21.183.64:8069/web/json/website.support.ticket"
        header = {'Authorization':'Basic YWJjQGVudWd1ZGlzY28uY29tOkVudWd1ZGlzY29AMDAw','Content-type':'application/json'}
        name = request.POST.get('name')
        # # email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        created_by = request.POST.get('created_by')
        priority = request.POST.get('priority')
        category_of_issue = request.POST.get('category_of_issue')
        # sub_category = request.POST.get('sub_category')
        description = request.POST.get('description')
        state = request.POST.get('state')
        street = request.POST.get('street')
        # channel = request.POST.get('channel')
        subject = request.POST.get('subject')
        # return JsonResponse([{'data':category_of_issue}],safe=False, status=200)
        # recs = connection = connector137().select_single("SELECT id,name from website_support_ticket_subcategory where parent_category_id = '"+ category_of_issue +"'")
        # if len(recs) < 1:
        # 	return JsonResponse([{'message':'Incorrect'}],safe=False)
        # # ac_ns = recs['name']
        # id_ = recs['id']
        # return JsonResponse([{'data':id_}],safe=False, status=200)
        data = { "params": 
                    {"category":category_of_issue,
                     "sub_category_id":101,
                     "state": state,
                     "person_name": name,
                     "cus_phone": phone_number,
                     "email": request.session['email'],
                     "description": description,
                     "acc_no":  request.session['acc_no'],
                     "acc_type": request.session['metering_type'],
                     "cus_street": street,
                     "created_by": created_by,
                     "priority_id": priority,
                     "acc_name": request.session['name'],
                     # "channel": channel,
                     "subject": subject
                    }
                 }
        rec = requests.post(url,headers=header,json=data)
        # rec.save()
        # messages.success(request, "Successfully!")
        # return redirect('/suport_ticket')
    # 	data = rec.json()
    # 	if "result" in data.keys():
    # 		if "Success" in data['result'].keys():
    # 			return {'message':'success'}
    # 		else:
    # 			return {'message': 'failed'}
    # 	else:
    # 		return {'message': 'failed'}
    context = {
        "rec": rec,
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/suport_ticket.html',context)



class HandlerView(View):
    def get(self, request):
        ac_ns = request.GET.get('ac_ns','')
        # rec = connection = connector137().select_single("SELECT acc_no,id,email,name,password from res_partner where acc_no = '"+ ac_n +"'")
        recs = connection = connector137().select_single("SELECT id,name from website_support_ticket_subcategory where parent_category_id = '"+ ac_ns +"'")
        if len(recs) < 1:
            return JsonResponse([{'message':'Incorrect'}],safe=False)
        cat_n = recs['name']
        # cat_id = recs['id']
        return JsonResponse([{'data':cat_n}],safe=False, status=200)
            # return JsonResponse([{'message':ac_n}],safe=False)
        # return render(request, 'report/custormer_portal/ajax.html')

@login_only
def fundwalet(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/fundwalet.html',context)


@login_only
def invoice(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/invoice.html',context)


@login_only
def update(request):
    context = {
        "email":request.session['email'],
        "metering_type": request.session['metering_type']
    }
    return render(request, 'report/custormer_portal/updateprofile.html',context)

def recrut(request):
    rec = {'formid': random.randint(10000000,99999999),'id':''}
    return render(request,'report/eedc form/examples/recrut.html',rec)


def recrut2(request,id):
    result = myclasss.Connect(host="74.208.145.153",database="ENUGUBACK",password="EedcOsita").select_single("SELECT id from hr_applicant where x_form_id = '%s'" % (id))
    if len(result) > 0:# in result.keys():
        return render(request,'report/eedc form/examples/recrut2.html',{'id': result['id'],'formid': id})
    else:
        rec = {'formid': id,'id':''}
        return render(request,'report/eedc form/examples/recrut.html',rec)
        


def recrut3(request,id):
    result = myclasss.Connect(host="74.208.145.153",database="ENUGUBACK",password="EedcOsita").select_single("SELECT id from hr_applicant where x_form_id = '%s'" % (id))
    if len(result) > 0:#if 'id'in result.keys():
        return render(request,'report/eedc form/examples/recrut3.html',{'id': result['id'],'formid': id})
    else:
        rec = {'formid': id,'id':''}
        return render(request,'report/eedc form/examples/recrut.html',rec)



def recrut4(request,id):
    result = myclasss.Connect(host="74.208.145.153",database="ENUGUBACK",password="EedcOsita").select_single("SELECT id,name from hr_applicant where x_form_id = '%s'" % (id))
    if len(result) > 0:#if 'id'in result.keys():
        return render(request,'report/eedc form/examples/recrut4.html',{'id': result['id'],'formid': id,'name': result['name']})
    else:
        rec = {'formid': id,'id':''}
        return render(request,'report/eedc form/examples/recrut.html',rec)


@csrf_exempt
def change_password(request):
    # return JsonResponse([{'message':'Login Details Error!!!'}],safe=False)
    try:

        acc_no = request.POST.get('acc_no', '')
        password = request.POST.get('password','')
        new_password = request.POST.get('new_password','')

        # validate old password
        rec = connection = connector137().select_single("SELECT acc_no, password from res_partner where acc_no = '"+ acc_no +"' and password = '"+ password +"' ")
        
        if len(rec) < 1:
            return JsonResponse([{'message':'Old Password Incorrect'}],safe=False)
        


        rec = connection = connector137().update({"table": "res_partner", "password":new_password, "csrfmiddlewaretoken": 1, "edit": 1 }, "acc_no", "'"+ acc_no +"'")
        return JsonResponse([{"message": rec}],safe=False)
    except Exception as e:
        return JsonResponse([{'message':"An error occurred " + str(e)}],safe=False)
        # return HttpResponse(str(e))


class AjaxHandlerView(View):
    def get(self, request):
        ac_n = request.GET.get('ac_n')
        # rec = connection = connector137().select_single("SELECT acc_no,id,email,name,password from res_partner where acc_no = '"+ ac_n +"'")
        rec = connection = connector137().select_single("SELECT acc_no,id,email,metering_type,name,password,old_acc_no,meter_no,juice_acc_no from res_partner where acc_no = '"+ ac_n +"' or old_acc_no = '"+ ac_n +"' or meter_no = '"+ ac_n +"' or juice_acc_no = '"+ ac_n +"'")
        if len(rec) < 1:
            return JsonResponse([{'message':'Account Incorrect'}],safe=False)
        ac_ns = rec['name']
        return JsonResponse([{'data':ac_ns}],safe=False, status=200)
        # return JsonResponse([{'message':ac_n}],safe=False)
        return render(request, 'report/custormer_portal/ajax.html')


def reset_form_details(request):
    try:
        if request.method == 'POST':
            acc_no = request.POST.get('acc_no', '')
            email = request.POST.get('email','')
            password = request.POST.get('password','')
             # validate old password
            rec = connection = connector137().select_single("SELECT acc_no,id,email,metering_type,name,password,old_acc_no,meter_no,juice_acc_no from res_partner where acc_no = '"+ acc_no +"' or old_acc_no = '"+ acc_no +"' or meter_no = '"+ acc_no +"' or juice_acc_no = '"+ acc_no +"'")
            # return JsonResponse([{"message": rec['id']}],safe=False)
            if len(rec) < 1:
                return JsonResponse([{'message':'Account Incorrect'}],safe=False)
            u_name = rec['name']
            u_acco = rec['acc_no']	
            # return JsonResponse([{"message": u_name, 'email': email, "acc":u_acco, "password":password }],safe=False)
            rec = connection = connector137().update({"table": "res_partner", "password":password, "email":email, "csrfmiddlewaretoken": 1, "edit": 2  }, "acc_no", "'"+ acc_no +"'") 
            template = render_to_string('report/custormer_portal/email_massage.html',{
                "user": u_name,
                 "email": email,
                  "acc":u_acco,
                "password":password
            })
            send_mail('From EEDC',
            template,
            settings.EMAIL_HOST_USER,
            [email],
            )
            # return JsonResponse([{"message": rec}],safe=False)
            return redirect("/id")

    except Exception as e:
        return JsonResponse([{'message':"An error occurred " + str(e)}],safe=False)
    return render(request, 'report/custormer_portal/reset.html')


def landingpage(request):
    headers = request.headers
    
    if 'Host' in headers.keys():
        if str(headers['Host']).strip() == 'eedcbz.smartpowerbilling.com':
            return district(request)   
    return render(request, 'report/custormer_portal/landingpage.html')

def email_massage(request):
    return render(request, 'report/custormer_portal/email_massage.html')

def id(request):
    return render(request, 'report/custormer_portal/id.html')



def patrick_pdf(request):
    try:
        if request.method == 'POST':
            report_type = request.POST.get('report_type')
            filename = request.POST.get('filename')
            year = request.POST.get('year')
            month = request.POST.get('month')
            account = request.POST.get('account')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            district = request.POST.get('district')
            # use_district = request.POST.get('use_district')

            cr = connection = myclasss.Connect().postgresConnect()
            # id = id
            type = report_type
            sql = ''
            if type == 'account':
                if use_district != True:
                    sql = "SELECT c.name as customer,cl.name as tariff, d.name as district , m.name as marketer , b.name as book  from res_partner c LEFT JOIN account_payment p ON p.partner_id = c.id and p.payment_date  between  '%s' and '%s' left join res_district d on d.id = c.district  left join marketer m on m.id = c.marketer left join book_feeder b on b.id = c.book_id Left Join customer_class cl on cl.id = c.customer_class where p.amount is null" % (start_date,end_date)
                else:
                    sql = "SELECT c.name as customer,cl.name as tariff, d.name as district , m.name as marketer , b.name as book  from res_partner c LEFT JOIN account_payment p ON p.partner_id = c.id and p.payment_date  between  '%s' and '%s' left join res_district d on d.id = c.district  left join marketer m on m.id = c.marketer left join book_feeder b on b.id = c.book_id Left Join customer_class cl on cl.id = c.customer_class where p.amount is null and d.id = '%s'" % (start_date,end_date,district.id)
            if type == 'tariff':
                if use_district != True:
                    sql = "SELECT cl.name as tariff,c.name as customer,p.bill_description as payment_type,p.amount as amount, p.bill_userid as cashier, d.name as district, m.name as marketer , b.name as book,p.payment_date as payment_date from res_partner c LEFT JOIN account_payment p ON p.partner_id = c.id and p.payment_date  between  '%s' and '%s' left join res_district d on d.id = c.district  left join marketer m on m.id = c.marketer left join book_feeder b on b.id = c.book_id Left Join customer_class cl on cl.id = c.customer_class where  p.amount is not null order by cl.name ASC" % (start_date,end_date)
                else:
                    sql = "SELECT cl.name as tariff,c.name as customer,p.bill_description as Payment_Type,p.amount as amount, p.bill_userid as cashier, d.name as district, m.name as marketer , b.name as book,p.payment_date as payment_date from res_partner c LEFT JOIN account_payment p ON p.partner_id = c.id and p.payment_date  between  '%s' and '%s' left join res_district d on d.id = c.district  left join marketer m on m.id = c.marketer left join book_feeder b on b.id = c.book_id Left Join customer_class cl on cl.id = c.customer_class where  p.amount is not null and d.id = '%s' order by cl.name ASC" % (start_date,end_date,district.id)
            if type == 'payment':
                if use_district != True:
                    sql = "SELECT d.name as district,c.name as customer,c.old_acc_no as old_acct_no, c.acc_no as account_no,p.bill_description as payment_type,p.amount as amount, p.bill_userid as cashier, cl.name as tariff,c.tariff_name as new_tariff,case when c.bill_status = true then 'Active' else 'Suspended' end as status,p.trans_ref as trans_ref,c.customer_category as cust_category,f.name as feeder, f.feeder_code as feeder_code, t.name as transformer,t.transformer_code as transformer_code,m.name as marketer ,m.marketer_code as marketer_code,b.name as book,b.book_code as book_code,p.payment_date as Payment_date from res_partner c LEFT JOIN account_payment p ON p.partner_id = c.id and p.payment_date  between  '%s' and '%s' left join res_district d on d.id = c.district  left join marketer m on m.id = c.marketer left join book_feeder b on b.id = c.book_id Left Join customer_class cl on cl.id = c.customer_class Left Join feeder_feeder f on f.id =c.feeder_id left join feeder_transformer t on t.id =c.transformer_id where  p.amount is not null order by d.name ASC" % (start_date,end_date)
                else:
                    sql = "SELECT d.name as district,c.name as customer,c.old_acc_no as old_acct_no, c.acc_no as account_no,p.bill_description as payment_type,p.amount as amount, p.bill_userid as cashier, cl.name as tariff,c.tariff_name as new_tariff,case when c.bill_status = true then 'Active' else 'Suspended' end as status,p.trans_ref as trans_ref,c.customer_category as cust_category,f.name as feeder, f.feeder_code as feeder_code, t.name as transformer,t.transformer_code as transformer_code,m.name as marketer ,m.marketer_code as marketer_code,b.name as book,b.book_code as book_code,p.payment_date as Payment_date from res_partner c LEFT JOIN account_payment p ON p.partner_id = c.id and p.payment_date  between  '%s' and '%s' left join res_district d on d.id = c.district  left join marketer m on m.id = c.marketer left join book_feeder b on b.id = c.book_id Left Join customer_class cl on cl.id = c.customer_class Left Join feeder_feeder f on f.id =c.feeder_id left join feeder_transformer t on t.id =c.transformer_id where  p.amount is not null and d.id = '%s' order by d.name ASC" % (start_date,end_date,district.id)
            if type == 'min_bill_dump':
                if use_district != True:
                    sql = "SELECT c.name as customer,f.name as feeder,t.name as transformer,d.name as district,c.acc_no as account_no,c.old_acc_no as old_acct_no,c.customer_category as category,case when c.allow_meter = true then 'Metered' else 'Unmetered' end as connectiontype, bill.id as bill_id,bill.e_consumed as consumption, case when ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end as month_due,bill.b_arrears as arrears,bill.b_outstand as total_due, bill.tariff_name as tariff,bill.type as type from res_partner c Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district Left JOIN feeder_reading r ON r.name = c.feeder_id and month= %s and year = %s LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = %s and e_year = %s LEFT JOIN customer_class cl ON cl.id = bill.user_class LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.e_consumed is not null and c.active = true and bill.feeder_id is not null" % (month,year,month,year)
                    # sql = "with net_arrears as (select c.id,  (c.credit + sum( (allbill.e_consumed  * bill.tariff_rate) + (allbill.e_consumed * bill.tariff_rate * case when allbill.create_date > '2020-01-31' then 0.075 else 0.05 end))) - sum(allpay.amount) as net_arrears from res_partner c left join feeder_customer_details allbill on allbill.create_date between '2019-07-30' and '%s' and allbill.customer_ids = c.id left join customer_class cl on cl.id = allbill.user_class left join account_payment allpay on allpay.partner_id = c.id and allbill.create_date between '2019-07-30' and '%s' group by c.id)SELECT c.acc_no,c.old_acc_no,b.name as Book,b.book_code as book_code,c.meter_no,cl.name as Tariff,case when c.allow_meter = true then 'Metered' else 'Unmetered' end as ConnectionType, c.customer_category, case when c.bill_status = true then 'Active' else 'Suspended' end as Status, d.name as District,c.name as Customer_name, c.street, c.phone,m.name as marketer ,m.marketer_code as marketer_code,m.marketer_phone,f.name as Feeder,f.feeder_code,t.name as Transformer, t.transformer_code,bill.id as bill_id,bill.current_read as PAR, bill.previous_read as LAR,bill.e_consumed as Billed_Unit, (bill.e_consumed*bill.tariff_rate) as Billed_Amount, CASE WHEN bill.create_date > '2020-02-01' THEN (bill.e_consumed*bill.tariff_rate) *0.075 ELSE (bill.e_consumed*bill.tariff_rate) *0.05 END as VAT ,  case when sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as Month_due, bill.adjustment,case when (sum(ar.net_arrears)) is not null then (sum(ar.net_arrears)) else 0 end ::bigint as arrears, case when (sum(ar.net_arrears)) is not null then (sum(ar.net_arrears)) else 0 end ::bigint + case when bill.adjustment is not null then bill.adjustment else 0 end::bigint + case when sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as total_due,  case when sum(p.amount) is not null then sum(p.amount) else 0 end as last_paid_amount,max(p.payment_date) as Payment_date,(CURRENT_DATE-MAX(p.payment_date)) AS days_from_lastpayment,date(c.create_date) as create_date ,bill.type from res_partner c left join net_arrears ar on ar.id = c.id Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district Left JOIN feeder_reading r ON r.name =  c.feeder_id and month= '%s' and year = '%s' LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = '%s' and e_year = '%s' LEFT JOIN customer_class cl ON cl.id = c.customer_class LEFT JOIN marketer m on m.marketer_code=c.marketer_code LEFT JOIN account_payment p on p.partner_id = c.id and p.payment_date  between  '%s' and '%s' LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.e_consumed is not null and bill.feeder_id is not null group by c.id, b.id,cl.id,d.id,bill.id,m.id,f.id,t.id,ar.net_arrears"  % (vals['start_date'],vals['start_date'],vals['month'],vals['year'],vals['month'],vals['year'],vals['start_date'],vals['end_date'])
                else:
                    sql = "SELECT c.name as customer,f.name as feeder,t.name as transformer,d.name as district,c.acc_no as account_no,c.old_acc_no as old_acct_no,c.customer_category as category,case when c.allow_meter = true then 'Metered' else 'Unmetered' end as connectiontype, bill.id as bill_id,bill.e_consumed as consumption, case when ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end as month_due,bill.b_arrears as arrears,bill.b_outstand as total_due, bill.tariff_name as tariff,bill.type as type from res_partner c Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district Left JOIN feeder_reading r ON r.name = c.feeder_id and month= %s and year =%s LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = %s and e_year = %s LEFT JOIN customer_class cl ON cl.id = bill.user_class LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.e_consumed is not null and c.active = true and bill.feeder_id is not null and d.id = %s" % (month,year,month,year,district.id)
            if type == 'bill_dump':
                if use_district != True:
                    sql = "SELECT c.acc_no as account_no,c.old_acc_no as old_acct_no,b.name as book,b.book_code as book_code,c.meter_no as meter_no,cl.name as tariff,f.f_band as band,bill.tariff_name as new_tariff,c.comment as building_id, case when c.allow_meter = true then 'Metered' else 'Unmetered' end as connectiontype, c.customer_category as cust_category, case when c.bill_status = true then 'Active' else 'Suspended' end as status,c.reason as reason, d.name as district,c.name as customer, c.street as address, c.phone as phone,m.name as marketer ,m.marketer_code as marketer_code,m.marketer_phone as marketer_phone,f.name as feeder,f.feeder_code as feeder_code,t.name as transformer, t.transformer_code as transformer_code,bill.id as bill_id,bill.current_read as par, bill.previous_read as lar,bill.e_consumed as billed_unit, (bill.e_consumed*bill.tariff_rate * bill.discount) as billed_amount, CASE WHEN bill.create_date > '2020-01-31' THEN (bill.e_consumed*bill.tariff_rate * bill.discount) *0.075 ELSE (bill.e_consumed*bill.tariff_rate * bill.discount) *0.05 END as vat ,  case when ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end as month_due, bill.adjustment as adjustment,  case when sum(p.amount) is not null then sum(p.amount) else 0 end as last_payment,max(p.payment_date) as payment_date,(CURRENT_DATE-MAX(p.payment_date)) AS days_from_lastpayment,date(c.create_date) as create_date ,bill.b_arrears as arrears,bill.b_outstand as total_due,bill.type as bill_type from res_partner c Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district Left JOIN feeder_reading r ON r.name =  c.feeder_id and month= '%s' and year = '%s' LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = '%s' and e_year = '%s' LEFT JOIN customer_class cl ON cl.id = bill.user_class LEFT JOIN marketer m on m.id=c.marketer LEFT JOIN account_payment p on p.partner_id = c.id and p.payment_date  between  '%s' and '%s' and p.bill_description = 'bill' LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.e_consumed is not null and c.active = true and bill.feeder_id is not null group by c.id, b.id,cl.id,d.id,bill.id,m.id,f.id,t.id"  % (month,year,month,year,start_date,end_date)
                else:
                    sql = "SELECT c.acc_no as account_no,c.old_acc_no as old_acct_no,b.name as book,b.book_code as book_code,c.meter_no as meter_no,cl.name as tariff,f.f_band as band,bill.tariff_name as new_tariff,c.comment as building_id, case when c.allow_meter = true then 'Metered' else 'Unmetered' end as connectiontype, c.customer_category as cust_category, case when c.bill_status = true then 'Active' else 'Suspended' end as status,c.reason as reason, d.name as district,c.name as customer, c.street as address, c.phone as phone,m.name as marketer ,m.marketer_code as marketer_code,m.marketer_phone as marketer_phone,f.name as feeder,f.feeder_code as feeder_code,t.name as transformer, t.transformer_code as transformer_code,bill.id as bill_id,bill.current_read as par, bill.previous_read as lar,bill.e_consumed as billed_unit, (bill.e_consumed*bill.tariff_rate * bill.discount) as billed_amount, CASE WHEN bill.create_date > '2020-01-31' THEN (bill.e_consumed*bill.tariff_rate * bill.discount) *0.075 ELSE (bill.e_consumed*bill.tariff_rate * bill.discount) *0.05 END as vat ,  case when ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then ((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end as month_due, bill.adjustment as adjustment,  case when sum(p.amount) is not null then sum(p.amount) else 0 end as last_payment,max(p.payment_date) as payment_date,(CURRENT_DATE-MAX(p.payment_date)) AS days_from_lastpayment,date(c.create_date) as create_date ,bill.b_arrears as arrears,bill.b_outstand as total_due,bill.type as bill_type from res_partner c Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district Left JOIN feeder_reading r ON r.name =  c.feeder_id and month= '%s' and year = '%s' LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = '%s' and e_year = '%s' LEFT JOIN customer_class cl ON cl.id = bill.user_class LEFT JOIN marketer m on m.id=c.marketer LEFT JOIN account_payment p on p.partner_id = c.id and p.payment_date  between  '%s' and '%s' and p.bill_description = 'bill' LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.e_consumed is not null and c.active = true and d.id = '%s' and bill.feeder_id is not null group by c.id, b.id,cl.id,d.id,bill.id,m.id,f.id,t.id"  % (month,year,month,year,start_date,end_date,district.id)
            if type == 'month_tariff':
                if use_district != True:
                    sql = "SELECT row_number() over (order by cl.name) as s_no,cl.name as tariff, count(r.id) as pop_billed, to_char(sum(bill.e_consumed),'FM9,999,999,999,999,999') as billed_energy, to_char(sum(p.amount),'FM9,999,999,999,999,999') as amount_collected , to_char(sum((bill.e_consumed * bill.tariff_rate * bill.discount) +  (CASE WHEN bill.create_date > '2020-02-01' THEN (bill.e_consumed*bill.tariff_rate * bill.discount) *0.075 ELSE (bill.e_consumed*bill.tariff_rate * bill.discount) *0.05 END)),'FM9,999,999,999,999,999') as total_bill , count(p.id) as payment_count from res_partner r left join customer_class cl on cl.id = r.customer_class left join feeder_customer_details bill ON bill.customer_ids = r.id and bill.e_month = '%s' and bill.e_year = '%s' LEFT JOIN res_district d ON d.id = r.district left join account_payment p on p.partner_id = r.id and p.payment_date between '%s' and '%s' and p.bill_description = 'bill' where p.amount is not null group by cl.name " % (month,year,start_date,end_date)
                else:
                    sql = "SELECT row_number() over (order by cl.name) as s_no,cl.name as tariff, count(r.id) as pop_billed, to_char(sum(bill.e_consumed),'FM9,999,999,999,999,999') as billed_energy, to_char(sum(p.amount),'FM9,999,999,999,999,999') as amount_collected , to_char(sum((bill.e_consumed * bill.tariff_rate * bill.discount) +  (CASE WHEN bill.create_date > '2020-02-01' THEN (bill.e_consumed*bill.tariff_rate * bill.discount) *0.075 ELSE (bill.e_consumed*bill.tariff_rate * bill.discount) *0.05 END)),'FM9,999,999,999,999,999') as total_bill , count(p.id) as payment_count from res_partner r left join customer_class cl on cl.id = r.customer_class left join feeder_customer_details bill ON bill.customer_ids = r.id and bill.e_month = '%s' and bill.e_year = '%s' LEFT JOIN res_district d ON d.id = r.district left join account_payment p on p.partner_id = r.id and p.payment_date between '%s' and '%s' and p.bill_description = 'bill' where p.amount is not null and d.id = '%s' group by cl.name " % (month,year,start_date,end_date,district.id)
            if type == 'marketer_report':
                if use_district != True:
                    sql = "SELECT row_number() over (order by m.name) as s_no, m.name as marketer,m.marketer_code as marketer_code,m.marketer_phone as marketer_phone,d.name as district,count(c.id) as total_pop,count(case when c.bill_status = False then c.id end) as suspended,count(case when c.bill_status = True then c.id end) as active, to_char(sum(bill.e_consumed),'FM9,999,999,999,999,999') as billed_energy,case when sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as billed_amount, case when (sum(bill.b_arrears)) is not null then (sum(bill.b_arrears)) else 0 end ::bigint as net_arrears, case when (sum(bill.b_outstand)) is not null then (sum(bill.b_outstand)) else 0 end ::bigint as total_due ,count(paid.id) as pay_count, case when (sum(paid.amount)) is not null then (sum(paid.amount)) else 0 end::bigint  as collection   from res_partner c left join marketer m on m.id = c.marketer left join customer_class cl on cl.id = c.customer_class left join feeder_customer_details bill on bill.customer_ids = c.id and bill.e_month = '%s' and bill.e_year = '%s' left join res_district d on d.id = c.district left join account_payment paid on paid.partner_id = c.id and paid.bill_description='bill' and paid.payment_date between '%s' and '%s' where m.name is not null group by m.name, m.marketer_code,m.marketer_phone,d.name " % (month,year,start_date,end_date)
                else:
                    sql = "SELECT row_number() over (order by m.name) as s_no, m.name as marketer,m.marketer_code as marketer_code,m.marketer_phone as marketer_phone,d.name as district,count(c.id) as total_pop,count(case when c.bill_status = False then c.id end) as suspended,count(case when c.bill_status = True then c.id end) as active, to_char(sum(bill.e_consumed),'FM9,999,999,999,999,999') as billed_energy,case when sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as billed_amount, case when (sum(bill.b_arrears)) is not null then (sum(bill.b_arrears)) else 0 end ::bigint as net_arrears, case when (sum(bill.b_outstand)) is not null then (sum(bill.b_outstand)) else 0 end ::bigint as total_due ,count(paid.id) as pay_count, case when (sum(paid.amount)) is not null then (sum(paid.amount)) else 0 end::bigint  as collection   from res_partner c left join marketer m on m.id = c.marketer left join customer_class cl on cl.id = c.customer_class left join feeder_customer_details bill on bill.customer_ids = c.id and bill.e_month = '%s' and bill.e_year = '%s' left join res_district d on d.id = c.district left join account_payment paid on paid.partner_id = c.id and paid.bill_description='bill' and paid.payment_date between '%s' and '%s' where m.name is not null and d.id = '%s' group by m.name, m.marketer_code,m.marketer_phone,d.name " % (month,year,start_date,end_date,district.id)
            # if type == 'feeder_report':
            # 	if use_district != True:
            # 		sql = "SELECT row_number() over (order by f.name) as SN, f.name as feeder, f.feeder_code,d.name as district, count(c.id) as total_pop, count(case when c.bill_status = False then c.id end) as suspended, count(case when c.bill_status = true then c.id end) as Active, to_char(sum(bill.e_consumed),'FM9,999,999,999,999,999') as Billed_Energy,case when sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as Billed_amount,case when (sum(bill.b_arrears)) is not null then (sum(bill.b_arrears)) else 0 end ::bigint as net_arrears ,case when (sum(bill.b_outstand)) is not null then (sum(bill.b_outstand)) else 0 end ::bigint as total_due,count(paid.id) as pay_count, case when (sum(paid.amount)) is not null then (sum(paid.amount)) else 0 end::bigint as collection from res_partner c left join feeder_feeder f on f.id = c.feeder_id left join customer_class cl on cl.id = c.customer_class left join feeder_customer_details bill on bill.customer_ids=c.id and bill.e_month = '%s' and bill.e_year = '%s' left join res_district d on d.id = c.district left join account_payment paid on paid.partner_id = c.id and paid.bill_description='bill' and paid.payment_date between '%s' and '%s' where f.name is not null group by f.name, f.feeder_code,d.name" % (month,year,start_date,end_date)
            # 	else:
            # 		sql = "SELECT row_number() over (order by f.name) as SN, f.name as feeder, f.feeder_code,d.name as district, count(c.id) as total_pop, count(case when c.bill_status = False then c.id end) as suspended, count(case when c.bill_status = true then c.id end) as Active, to_char(sum(bill.e_consumed),'FM9,999,999,999,999,999') as Billed_Energy,case when sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate * bill.discount) + (bill.e_consumed * bill.tariff_rate * bill.discount * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as Billed_amount,case when (sum(bill.b_arrears)) is not null then (sum(bill.b_arrears)) else 0 end ::bigint as net_arrears ,case when (sum(bill.b_outstand)) is not null then (sum(bill.b_outstand)) else 0 end ::bigint as total_due,count(paid.id) as pay_count, case when (sum(paid.amount)) is not null then (sum(paid.amount)) else 0 end::bigint as collection from res_partner c left join feeder_feeder f on f.id = c.feeder_id left join customer_class cl on cl.id = c.customer_class left join feeder_customer_details bill on bill.customer_ids=c.id and bill.e_month = '%s' and bill.e_year = '%s' left join res_district d on d.id = c.district left join account_payment paid on paid.partner_id = c.id and paid.bill_description='bill' and paid.payment_date between '%s' and '%s' where f.name is not null and d.id ='%s' group by f.name, f.feeder_code,d.name" % (month,year,start_date,end_date,district.id)
            # if type == 'arrears':
            # 	sql = "select r.name as customer, to_char(b.b_outstand,'FM999999999.99') as arrears, acc_no as account_no, d.name as district from res_partner r left join feeder_customer_details b on b.customer_ids = r.id left join res_district d on d.id = r.district where r.metering_type = 'postpaid' and b.e_month = '%s' and b.e_year = '%s' " %(month, year)

            # if type == 'credit':
            # 	sql = "select r.name as customer, new_arrears as arrears, acc_no as account_no, d.name as district from res_partner r left join res_district d on d.id = r.district where new_arrears::float<0 and metering_type = 'postpaid' and bill_status = True;"
            # if type == 'cus_history':
            # 	sql = "SELECT a.acc_no as account,a.name as customer,date(b.create_date) as date,d.name as district,c.name as tariff,to_char(b.e_consumed,'FM99999999.99') as energy,to_char(b.b_month,'FM999999999.99') as billed_amount,to_char(b.b_vat, 'FM999999999.99') as vat ,to_char(b.b_amount, 'FM999999999.99') as month_due,b.adjustment as adjustment,b.last_pay as last_payment,to_char(b.b_prev_bal,'FM999999999.99') as previous_balance,to_char(b.b_arrears,'FM999999999.99') as net_arrears,to_char(b.b_outstand,'FM999999999.99') as total_due, b.type as bill_type from res_partner a left join res_district d on d.id = a.district left join feeder_customer_details b on b.customer_ids = a.id left join customer_class c on c.id = b.user_class where b.create_date > '2019-7-31' and a.acc_no = '%s' order by b.create_date" % (account)
            # if type == 'cus_history2':
            # 	sql = "SELECT a.acc_no as account,a.name as customer,date(b.create_date) as date,d.name as district,b.previous_read as lar,b.current_read as par,to_char(b.e_consumed,'FM999999999.99') as energy,to_char(b.b_amount,'FM999999999.99') as month_due,b.adjustment as adjustment,b.last_pay as last_payment,to_char(b.b_outstand, 'FM9999999999.99') as total_due, b.type as bill_type from res_partner a left join res_district d on d.id = a.district left join feeder_customer_details b on b.customer_ids = a.id left join customer_class c on c.id = b.user_class where b.create_date > '2019-7-31' and a.acc_no = '%s' order by b.create_date" % (account)
            # if type == 'customers':
            # 	sql = "SELECT c.name as customer,c.new_arrears as arrears,d.name as district,c.acc_no as account_no,c.old_acc_no as old_acct_no,c.bill_status as status,c.allow_meter as metered,cl.name as tariff,book.name as book, feeder.name as feeder,t.name as transformer from res_partner c left join res_district d on d.id = c.district left join customer_class cl on cl.id = c.customer_class left join feeder_transformer t on t.id = c.transformer_id left join feeder_feeder feeder on feeder.id = c.feeder_id left join book_feeder book on book.id = c.book_id where c.active = true"
            # if type == 'new_customer':
            # 	sql = "SELECT c.name as customer,c.acc_no as account_no,d.name as district,case when c.bill_status = true then 'Active' else 'Suspended' end as status,c.metering_type as type,c.allow_meter as metered,cl.name as tariff,book.name as book, feeder.name as feeder,t.name as transformer,c.create_date as date from res_partner c left join res_district d on d.id = c.district left join customer_class cl on cl.id = c.customer_class left join feeder_transformer t on t.id = c.transformer_id left join feeder_feeder feeder on feeder.id = c.feeder_id left join book_feeder book on book.id = c.book_id where c.active = true and c.create_date between '%s' and '%s'" % (start_date,end_date)
            # if type == 'feeder_bill':
            # 	sql = "select d.name as district,f.name as feeder,f.feeder_code as feeder_code,to_char(e_imported,'FM9,999,999,999,999,999') as energy_imported,to_char(e_ppm,'FM9,999,999,999,999,999') as ppm,to_char(sum(case when bill.type != 'Unmetered' then bill.e_consumed else 0 end),'FM9,999,999,999,999,999') as metered_consumption,to_char(sum(case when bill.type = 'Unmetered' then bill.e_consumed else 0 end),'FM9,999,999,999,999,999') as unmetered_consumption,to_char(sum(case when bill.type != 'Unmetered' then bill.e_consumed else 0 end) + sum(case when bill.type = 'Unmetered' then bill.e_consumed else 0 end) + e_ppm,'FM9,999,999,999,999')  as bu, to_char(((sum(case when bill.type != 'Unmetered' then bill.e_consumed else 0 end) + sum(case when bill.type = 'Unmetered' then bill.e_consumed else 0 end) + e_ppm) / e_imported) * 100,'FM9,999,999') as billing_efficiency from feeder_reading r left join feeder_feeder f on f.id = r.name left join res_district d on d.id = f.district_id left join feeder_customer_details bill on bill.reading_id = r.id where month = %s and year = %s and f.name is not null and e_imported > 0 group by f.name,e_imported,e_ppm,f.feeder_code,d.name order by f.name" % (month,year)
            # if type == 'adj_dump':
            # 	if use_district != True:
            # 		sql = "SELECT c.name as customer,f.name as feeder,f.feeder_code as feeder_code,t.name as transformer,t.transformer_code as transformer_code, d.name as district,c.acc_no as account_no,c.old_acc_no as old_acct_no,c.customer_category as category,bill.b_arrears as arrears,bill.last_pay as last_pay,bill.adjustment as adjustment, bill.b_outstand as total_due, bill.tariff_name as tariff,one.reason as below200_reason,two.reason as above200_reason,three.reason as above2m_reason from res_partner c Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = %s and e_year = %s left join crm_adjustmentone one on one.customers = c.id and one.bill_month = %s and one.bill_year = %s left join crm_adjustmentabv two on two.customers = c.id and two.bill_month = %s and two.bill_year = %s left join crm_adjustmentmill three on three.customers = c.id and three.bill_month = %s and three.bill_year = %s LEFT JOIN customer_class cl ON cl.id = bill.user_class LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.adjustment is not null and c.active = true and bill.feeder_id is not null" % (month,year,month,year,month,year,month,year)
            # 		# sql = "with net_arrears as (select c.id,  (c.credit + sum( (allbill.e_consumed  * bill.tariff_rate) + (allbill.e_consumed * bill.tariff_rate * case when allbill.create_date > '2020-01-31' then 0.075 else 0.05 end))) - sum(allpay.amount) as net_arrears from res_partner c left join feeder_customer_details allbill on allbill.create_date between '2019-07-30' and '%s' and allbill.customer_ids = c.id left join customer_class cl on cl.id = allbill.user_class left join account_payment allpay on allpay.partner_id = c.id and allbill.create_date between '2019-07-30' and '%s' group by c.id)SELECT c.acc_no,c.old_acc_no,b.name as Book,b.book_code as book_code,c.meter_no,cl.name as Tariff,case when c.allow_meter = true then 'Metered' else 'Unmetered' end as ConnectionType, c.customer_category, case when c.bill_status = true then 'Active' else 'Suspended' end as Status, d.name as District,c.name as Customer_name, c.street, c.phone,m.name as marketer ,m.marketer_code as marketer_code,m.marketer_phone,f.name as Feeder,f.feeder_code,t.name as Transformer, t.transformer_code,bill.id as bill_id,bill.current_read as PAR, bill.previous_read as LAR,bill.e_consumed as Billed_Unit, (bill.e_consumed*bill.tariff_rate) as Billed_Amount, CASE WHEN bill.create_date > '2020-02-01' THEN (bill.e_consumed*bill.tariff_rate) *0.075 ELSE (bill.e_consumed*bill.tariff_rate) *0.05 END as VAT ,  case when sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as Month_due, bill.adjustment,case when (sum(ar.net_arrears)) is not null then (sum(ar.net_arrears)) else 0 end ::bigint as arrears, case when (sum(ar.net_arrears)) is not null then (sum(ar.net_arrears)) else 0 end ::bigint + case when bill.adjustment is not null then bill.adjustment else 0 end::bigint + case when sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) is not null then sum((bill.e_consumed  * bill.tariff_rate) + (bill.e_consumed * bill.tariff_rate * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) else  0 end::bigint as total_due,  case when sum(p.amount) is not null then sum(p.amount) else 0 end as last_paid_amount,max(p.payment_date) as Payment_date,(CURRENT_DATE-MAX(p.payment_date)) AS days_from_lastpayment,date(c.create_date) as create_date ,bill.type from res_partner c left join net_arrears ar on ar.id = c.id Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district Left JOIN feeder_reading r ON r.name =  c.feeder_id and month= '%s' and year = '%s' LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = '%s' and e_year = '%s' LEFT JOIN customer_class cl ON cl.id = c.customer_class LEFT JOIN marketer m on m.marketer_code=c.marketer_code LEFT JOIN account_payment p on p.partner_id = c.id and p.payment_date  between  '%s' and '%s' LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.e_consumed is not null and bill.feeder_id is not null group by c.id, b.id,cl.id,d.id,bill.id,m.id,f.id,t.id,ar.net_arrears"  % (vals['start_date'],vals['start_date'],vals['month'],vals['year'],vals['month'],vals['year'],vals['start_date'],vals['end_date'])
            # 	else:
            # 		sql = "SELECT c.name as customer,f.name as feeder,f.feeder_code as feeder_code,t.name as transformer,t.transformer_code as transformer_code, d.name as district,c.acc_no as account_no,c.old_acc_no as old_acct_no,c.customer_category as category,bill.b_arrears as arrears,bill.last_pay as last_pay,bill.adjustment as adjustment, bill.b_outstand as total_due, bill.tariff_name as tariff,one.reason as below200_reason,two.reason as above200_reason,three.reason as above2m_reason from res_partner c Left JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN res_district d ON d.id = c.district LEFT JOIN feeder_customer_details bill ON bill.customer_ids = c.id and e_month = %s and e_year = %s left join crm_adjustmentone one on one.customers = c.id and one.bill_month = %s and one.bill_year = %s left join crm_adjustmentabv two on two.customers = c.id and two.bill_month = %s and two.bill_year = %s left join crm_adjustmentmill three on three.customers = c.id and three.bill_month = %s and three.bill_year = %s LEFT JOIN customer_class cl ON cl.id = bill.user_class LEFT JOIN book_feeder b ON b.id = c.book_id WHERE bill.adjustment is not null and c.active = true and bill.feeder_id is not null and d.id = %s" % (month,year,month,year,month,year,month,year,district.id)
            # print(sql)
            cr = cr
            cr.execute(sql)
            data = cr.dictfetchall()
            print(data)
            print(cr.fetchall())
        else:
            print(1234567)
    except Exception as e:
        return HttpResponse(e)