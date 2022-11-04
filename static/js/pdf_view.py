from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
from django.http import HttpResponse
from django.core.mail import EmailMessage
import psycopg2
import qrcode
import base64
from PIL import  Image
from io import BytesIO

class MyPDFView(View):
		template='report/print.html'
		

		def get(self, request):
				name = "bill_report.pdf"
				email_failed = 0
				email_sent = 0
				connection = psycopg2.connect(user = "postgres",
																	password = "EedcOsita@123",
																	host = "localhost",
																	port = "5432",
																	database = "EEDCLIVE")
				cr = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				if request.GET.get('type') == 'marketer':
					cr.execute("SELECT id,cluster,building,create_date,customer_id,name,meter_no,tariff,tariff_rate,account_no,rate,(rate * case when create_date > '2020-01-31' then 0.075 else 0.05 end) as new_vat,adjustment,credit,old_acc_no,phone,address,district,year,month_num,e_consumed,arrears,amount,previous_read,current_read,multiplicity,feeder,transformer,marketer_name,marketer_phone,last_bill,prev_dates,prev_amount,prev_payment_amount,current_payment_amount,current_payment_date,email from bill_download bill  where marketer_id = %s and customer_category = '%s' and month_num = %s and year = %s and rate::int > 0 " % (request.GET.get('id'),request.GET.get('category'),request.GET.get('month'),request.GET.get('year')))
				elif request.GET.get('type') == 'books':
					cr.execute("SELECT id,cluster,building,create_date,customer_id,name,meter_no,tariff,tariff_rate,account_no,rate,(rate * case when create_date > '2020-01-31' then 0.075 else 0.05 end) as new_vat,adjustment,credit,old_acc_no,phone,address,district,year,month_num,e_consumed,arrears,amount,previous_read,current_read,multiplicity,feeder,transformer,marketer_name,marketer_phone,last_bill,prev_dates,prev_amount,prev_payment_amount,current_payment_amount,current_payment_date,email from bill_download bill  where book_id = %s and customer_category = '%s' and month_num = %s and year = %s and rate::int > 0 " % (request.GET.get('id'),request.GET.get('category'),request.GET.get('month'),request.GET.get('year')))
				elif request.GET.get('type') == 'tariff':
					cr.execute("SELECT id,cluster,building,create_date,customer_id,name,meter_no,tariff,tariff_rate,account_no,rate,(rate * case when create_date > '2020-01-31' then 0.075 else 0.05 end) as new_vat,adjustment,credit,old_acc_no,phone,address,district,year,month_num,e_consumed,arrears,amount,previous_read,current_read,multiplicity,feeder,transformer,marketer_name,marketer_phone,last_bill,prev_dates,prev_amount,prev_payment_amount,current_payment_amount,current_payment_date,email from bill_download bill  where marketer_id = %s and customer_category = '%s' and month_num = %s and year = %s and tariff = '%s' and rate::int > 0 " % (request.GET.get('id'),request.GET.get('category'),request.GET.get('month'),request.GET.get('year'),request.GET.get('tariff')))				
				else:
					cr.execute("SELECT bill.id,bill.create_date as create_date,c.id as customer_id,c.name,c.meter_no,class.name as tariff,class.tariff as tariff_rate,c.acc_no as account_no,adjustment,c.credit as credit,c.old_acc_no,c.phone,c.street as address,d.name as district,bill.e_year as year,bill.e_month as month_num, bill.e_consumed,c.credit as arrears,(bill.e_consumed  * class.tariff) as rate, ((bill.e_consumed  * class.tariff) + (bill.e_consumed * class.tariff * case when bill.create_date > '2020-01-31' then 0.075 else 0.05 end)) as amount,bill.previous_read,bill.current_read,c.multiplicity,f.name as feeder,t.name as transformer,m.name as marketer_name,m.marketer_phone as marketer_phone from feeder_customer_details bill LEFT JOIN res_partner c on c.id = bill.customer_ids LEFT JOIN feeder_feeder f ON f.id = c.feeder_id LEFT JOIN feeder_transformer t ON t.id = c.transformer_id LEFT JOIN marketer m on m.id = c.marketer LEFT JOIN res_district d on d.id = c.district LEFT JOIN customer_class class on class.id = c.customer_class  where c.id = %s and c.customer_category = '%s' and e_month = %s and e_year = %s" % (request.GET.get('id'),request.GET.get('category'),request.GET.get('month'),request.GET.get('year')))
				records = cr.fetchall() 
				month = ['January','February','March','April','May','June','July','August','September','October','November','December']
				# print("STARTING %s %s %s %s" % (request.GET.get('id'),request.GET.get('category'),request.GET.get('month'),request.GET.get('year')))
				for i in range(len(records)):
						# if records[i]['month_num'] == 2 and records[i]['year'] == 2020:
						# 	records[i]['vat'] = '{:,.2f}'.format(round(records[i]['rate'] * 0.075,2))
						# else:
						records[i]['vat'] = '{:,.2f}'.format(round(records[i]['new_vat'],2))
						
						# records[i]['vat'] = '{:,.2f}'.format(round(records[i]['rate'] * 0.05,2))

						prev_month = int(records[i]['month_num']) - 1
						prev_year = records[i]['year']
						records[i]['month'] = month[int(records[i]['month_num']) - 1]
						records[i]['bill_month'] = month[int(records[i]['month_num']) - 2]
						if prev_month == 0:
								prev_month = 12
								prev_year = int(records[i]['year']) - 1
						# cr = self._cr
						records[i]['bill_year'] = prev_year
						# bill_prev = self.env['feeder.customer.details'].search([('customer_ids','=',records[i]['customer_id']),('e_month','=',prev_month),('e_year','=',prev_year)],order='id desc')
						# if
						# if request.GET.get('type') == 'marketer' and request.GET.get('id') == 970:
						# 	print("SELECT e_consumed,bill.create_date,(e_consumed * cl.tariff) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and e_month = %s  and e_year = %s" % (records[i]['customer_id'],prev_month,prev_year))
						# cr.execute("SELECT e_consumed,bill.create_date,(e_consumed * cl.tariff) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and e_month = %s  and e_year = %s" % (records[i]['customer_id'],prev_month,prev_year))     
						bill_prev = []#cr.fetchall()
						b_rate = 0
						arrears = 0
						
						bill_prev_create_date = False
						if len(bill_prev) == 0:
								bill_prev_create_date = records[i]['prev_dates']#'%s-%s-06' % (prev_year,prev_month)
								b_rate = records[i]['last_bill']
						else:
								bill_prev_create_date = bill_prev[0]['create_date']
								b_rate = bill_prev[0]['rate']
						# if request.GET.get('type') == 'marketer' and request.GET.get('id') == 970:
						# 	print("SELECT payment_date,amount from account_payment where partner_id = '%s' and payment_date Between '2019-07-01' and  '%s' and payment_date != '%s' and bill_description = 'bill' order by payment_date desc" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))
						# cr.execute("SELECT max(payment_date) as payment_date,sum(amount) as amount from account_payment where partner_id = '%s' and payment_date Between '2019-07-01' and  '%s' and payment_date != '%s' and bill_description = 'bill' order by payment_date desc" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))     
						july_payment = [] #cr.fetchall()
						
						# if request.GET.get('type') == 'marketer' and request.GET.get('id') == 970:
						# 	print("SELECT sum((e_consumed * cl.tariff) + (e_consumed * cl.tariff * 0.05)) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and bill.create_date Between '2019-07-01' and '%s' and bill.create_date != '%s'" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))
						
						# cr.execute("SELECT sum((e_consumed * cl.tariff) + (e_consumed * cl.tariff * 0.05)) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and bill.create_date Between '2019-07-01' and '%s' and bill.create_date != '%s'" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))      
						# print("SELECT sum((e_consumed * cl.tariff) + (e_consumed * cl.tariff * 0.05)) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and bill.create_date Between '2019-07-01' and '%s' and bill.create_date != '%s'" % (records[i]['customer_id'],bill_prev_create_date,bill_prev_create_date))
						prev_econsumed = []#cr.fetchall()
						# print("Credit %s %s %s" % (records[i]['customer_id'],request.GET.get('id'),records[i]['credit']))
						# try:
						# 		july_balance = float(prev_econsumed[0]['rate']) + float(records[i]['credit'])
						# except Exception as e:
						if records[i]['credit'] == None:
							records[i]['credit'] = 0
						july_balance = (float(records[i]['prev_amount']) + float(records[i]['credit'])) - float(records[i]['prev_payment_amount'])
						
						# print("PREV_PAYMENT %s CREDIT %s PREV_BILLS %s" % (records[i]['prev_payment_amount'],records[i]['credit'],records[i]['prev_payment_amount']))
						# for j_pay in july_payment:
						# 		try:
						# 			july_balance = float(july_balance) - float(j_pay['amount'])
						# 		except Exception as e:
						# 			july_balance = july_balance
								#July Payment and Arrears
								#August Payment and Arrears
								#September Payment and Arrears
						# cr.execute("SELECT payment_date,amount from account_payment where partner_id = '%s' and payment_date Between '%s' and  '%s' and bill_description = 'bill' and payment_date != '%s' order by payment_date asc" % (records[i]['customer_id'],bill_prev_create_date,records[i]['create_date'],records[i]['create_date']))     
						bill_payment = []#cr.fetchall()
			
						prev = 0
						if True:
						# 		for b in bill_prev:
						# 			try:
						# 				prev = float(prev) + float(b['rate'] + (b['rate'] * 0.05));
						# 			except Exception as e:
						# 				prev = float(prev) + float(records[i]['last_bill'] + (records[i]['last_bill'] * 0.05));
						# 				print(b['rate'])
						# 				# print("SELECT e_consumed,bill.create_date,(e_consumed * cl.tariff) as rate from feeder_customer_details bill LEFT JOIN customer_class cl on cl.id = user_class where customer_ids = '%s' and e_month = %s  and e_year = %s" % (records[i]['customer_id'],prev_month,prev_year))
										# raise e
								prev = float(prev) + float(records[i]['last_bill'])										
								if july_balance == None:
									july_balance = 0
								a_to_use = july_balance
								records[i]['arrears'] = (float(a_to_use) + float(prev))
								# print("ARREARSLAST BILL %s" % a_to_use)
								records[i]['net_arrears'] = '{:,.2f}'.format((float(a_to_use) + float(prev)))

								arrears = records[i]['arrears']
			
						payment_amount = 0
						if True:
								# for pay in bill_payment:        
								if True:
										records[i]['payment_date'] = records[i]["current_payment_date"]
										payment_amount += records[i]["current_payment_amount"]
										arrears = float(arrears) - float(records[i]["current_payment_amount"])
						
						records[i]['payment_amount'] = '{:,.2f}'.format(payment_amount)
			
						# records[i]['arrears'] = records[i]['arrears'] - elec_total
						# print(elec_total)
						if records[i]['adjustment'] == None:
							records[i]['adjustment'] = 0
						records[i]['arrears'] = '{:,.2f}'.format(arrears)
						# records[i]['vat'] = '{:,.2f}'.format(round(records[i]['rate'] * 0.05,2))
						records[i]['total_pay'] = '{:,.2f}'.format(round(records[i]['adjustment'] + arrears + records[i]['amount'],2))
						records[i]['amount'] = '{:,.2f}'.format(round(records[i]['amount'],2))
						# records[i]['total_pay'] = '{:,.2f}'.format(round(records[i]['adjustment'] + arrears +  round(records[i]['rate'],2) + round(records[i]['rate'] * 0.05,2),2))

						records[i]['e_consumed'] = '{:,.2f}'.format(round(records[i]['e_consumed'],2))
						records[i]['rate'] = '{:,.2f}'.format(round(records[i]['rate'],2))

						records[i]['contact'] = 'Customer Name: %s \n Old Account Number: %s \n Customer Account Number: %s \n Arrears: %s \n Month Due: %s \n' % (records[i]['name'],records[i]['old_acc_no'],records[i]['account_no'],records[i]['arrears'],records[i]['amount'])
						data_contact = records[i]['contact']
						contact = str(base64.b64encode(data_contact.encode("utf-8")),"utf-8")
						encode2 = str(base64.b64encode(contact.encode("utf-8")),"utf-8")
						encode3 = str(base64.b64encode(encode2.encode("utf-8")),"utf-8")
						encode4 = str(base64.b64encode(encode3.encode("utf-8")),"utf-8")
						records[i]['contact'] = encode4
						email_address = records[i]['email']
						# records[i]['contact'] = encode10
						email = EmailMessage(
 									   'EEDC BILL',
    									'Electricity bill for %s %s' % (month[int(request.GET.get('month')) - 1],request.GET.get('year')),
    									'billing@enugudisco.com',
    									[records[i]['email']],
    									[],
    									reply_to=['billing@enugudisco.com'],
    									headers={'Message-ID': 'EEDC'},
										)
						try:
							if request.GET.get('send') == 'email':
								context= {'district': 'OGUI DISTRICT','bill': [records[i]]}
								
								if email_address != False and email_address != None:
									response = PDFTemplateResponse(request=request,
																			 template=self.template,
																			 filename=name,
																			 context= context,
																			 show_content_in_browser=False,
																			 cmd_options={'margin-top': 20,},
																			 )
									email.attach('bill.pdf',response.rendered_content,'application/pdf')
									if email.send():

										email_sent = email_sent + 1
									else:
										email_failed = email_failed + 1
								else:
									email_failed = email_failed + 1
						except Exception as e:
							email_failed = email_failed + 1
								


				# print("DONE %s %s %s %s" % (request.GET.get('id'),request.GET.get('category'),request.GET.get('month'),request.GET.get('year')))
				context= {'district': 'OGUI DISTRICT','bill': records}
				name = request.GET.get('name_of_file')
				response = PDFTemplateResponse(request=request,
																			 template=self.template,
																			 filename=name,
																			 context= context,
																			 show_content_in_browser=False,
																			 cmd_options={'margin-top': 20,},
																			 )
				if request.GET.get('send') == 'email':
					return HttpResponse('%s Emails Sent , %s Emails Failed' % (email_sent,email_failed))
				else:
					return response