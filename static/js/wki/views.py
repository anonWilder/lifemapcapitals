from urllib import response
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from .forms import *
import random
from random import shuffle
import datetime
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
import requests
import json
import csv
import xlwt
from django.contrib.auth.decorators import login_required
from rest_framework import generics,status
from .models import *
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from django.contrib.auth import get_user_model
from django.contrib import messages

class Apisoled(generics.ListCreateAPIView):
	queryset = SoledSerial.objects.all()
	serializer_class = SoledSerializer


# Create your views here.
def index(request):
	return render(request,'index.html')

@login_required
def Gdestroy(request, id):  
	employee = Genarator.objects.get(id=id)  
	employee.delete()
	# data = {
	# 	'status':'deleted successfully',
	# 	'status_text':"your serial data has been deleted successfully",
	# 	'status_icon':"success",
	# };
	# # return response.json(data)
	# return JsonResponse(data)
	return redirect("/genarator")

@login_required
def genarator(request):
	gen_seria = Genarator.objects.order_by('-date_time')[0:20]
	now = datetime.datetime.now()
	year = now.year
	month = now.month
	day = now.day
	if len(str(day)) == 1:
		day = "0" + str(day)
	if len(str(month)) == 1:
		day = "0" + str(month)

	if request.method == 'POST':
		amounts = int(request.POST.get("amount"))
		starts = int(request.POST.get("start"))
		ends = int(request.POST.get("end"))
		serial = "SE"
		date = str(serial) + str(year) + str(month) + str(day)
		
		for i in range(amounts):
			result = []
			temp = random.randint(starts, ends+1)
			roundup = str(date) + str(temp)
			result.append(roundup)
			for results in result:
				result_ = results
			create_comment=Genarator(genarator=result_ , user=request.user)
			create_comment.save()
		return redirect("/genarator")
	else:
		pass
	context = {
		"year":year,
		"month":month,
		"day":day,
		"serial":gen_seria,
		# "serials":roundup,
	}
	return render(request,'genarator.html',context)

@login_required
def export_csv(request):
	response = HttpResponse(content_type='application/csv')
	response['Content-Disposition']='attachment; filename=Genarator'+ str(datetime.datetime.now()) + '.csv'
	writer = csv.writer(response)
	writer.writerow(['SERIAL NUMBER'])
	
	stock = Genarator.objects.filter(stock='Inactive')
	
	for stocks in stock:
		writer.writerow([stocks.genarator])
		Genarator.objects.update(stock='Active')
	return response


@login_required
def export_excel(request):
	response = HttpResponse(content_type='text/ms-excel')
	response['Content-Disposition']='attachment; filename=Genarator'+ str(datetime.datetime.now()) + '.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Genarator')
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	
	columns = ['SERIAL']
	
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
	font_style = xlwt.XFStyle()
	rows = Genarator.objects.filter(stock='Inactive').values_list('genarator')
	
	for row in rows:
		row_num+=1
	
		for col_num in range(len(row)):
			ws.write(row_num, col_num,str(row[row_num]), font_style)
	wb.save(response)
	Genarator.objects.update(stock='Active')

	return response

@login_required
def addnew(request):
	# if request.method == "POST":  
	# 	form = EmployeeForm(request.POST)  
	# 	if form.is_valid():
	# 		event = form.save(commit=False)
	# 		event.staff = request.user
	# 		event.save()
	# 		return redirect('/serial')  
	# else:  
	# 	form = EmployeeForm()
	name = Genarator.objects.filter(stock='Active')
	return render(request,'active.html',{'name':name.order_by('-date_time')[0:100]}) 
	# return render(request,'active.html',{'name':name.order_by('-date_time')[0:100]}) 

@login_required
def dashbord(request):
	for row in SoledSerial.objects.all().reverse():
		if SoledSerial.objects.filter(serial_number=row.serial_number).count() > 1:
			row.delete()
	SoledSerial.objects.values('serial_number').distinct()
	active_count = Genarator.objects.filter(stock='Active').count()
	inactive_count = Genarator.objects.filter(stock='Inactive').count()
	soled_count = SoledSerial.objects.filter(status='Sold').count()
	soled_table = SoledSerial.objects.filter(validation=True)
	active_table = Genarator.objects.filter(stock='Active')
	all_count = Genarator.objects.all().count()

	# view=[]
	# for v in soled_table:
	# 	# if v['dat'] == None or v['dat'] == False:
	# 	# 	v['dat'] = "%s-%s-01" % (v['year'],v['month'])
	# 	try:
	# 		view.append({
	# 		"serial_number": v.serial_number.count(),
	# 		"date":v["date_sold"].strftime("%m"),
	# 		"year":v["date_sold"].strftime("%Y"),
	# 		})
		
	# 	except Exception as e:
	# 		print(str(e))
	context = {
		'active_count':active_count,
		'inactive_count':inactive_count,
		'soled_count':soled_count,
		'soled_table':soled_table.order_by('-date_time')[0:5],
		'active_table':active_table.order_by('-date_time')[0:5],
		# .order_by('-date_time')[0:6],
		# "view":view,
		'all_count':all_count,
	}
	return render(request,'dashbord.html', context)

@login_required
def users(request):
	name = User.objects.all()
	return render(request,'users.html',{'name':name})

@login_required
def userdestroy(request, id):  
	employee = User.objects.get(id=id)  
	employee.delete()  
	return redirect("/users")
  
@login_required
def serial(request, *args, **kwargs):
	name = Genarator.objects.filter(stock='Inactive')
	if request.method =='POST':
		stock_ids = request.POST.getlist('id[]')
		for id in stock_ids:
			stock = Genarator.objects.get(pk=id)
			stock.delete()
		return redirect('/serial')
	return render(request,'table.html',{'name':name.order_by('-date_time')[0:100]})

@login_required
def edit(request, id):  
	employee = Genarator.objects.get(id=id)  
	return render(request,'edittable.html', {'employee':employee})

@login_required
def update(request, id):  
	employee = Genarator.objects.get(id=id)  
	form = EmployeeForm(request.POST, instance = employee)  
	if form.is_valid():  
		form.save()  
		return redirect("/serial")  
	return render(request, 'edittable.html', {'employee': employee})

@login_required
def destroy(request, id):  
	employee = Genarator.objects.get(id=id)  
	employee.delete()  
	return redirect("/serial")

@login_required
def destroy_Sold(request, id):  
	employee = SoledSerial.objects.get(id=id)  
	employee.delete()  
	return redirect("/Soled_Serial")

@login_required
def destroy_Sold(request, id):  
	employee = SoledSerial.objects.get(id=id)  
	employee.delete()  
	return redirect("/Soled_Serial")

@login_required
def Soled_Serial(request, *args, **kwargs):
	for row in SoledSerial.objects.all().reverse():
		if SoledSerial.objects.filter(serial_number=row.serial_number).count() > 1:
			row.delete()
	SoledSerial.objects.values('serial_number').distinct()
	data=[]
	cons = SoledSerial.objects.filter(status='Sold')
	for pho_ in cons:
		pho__s = pho_.serial_number.split()

		for i in pho__s:
			if len(i) == 13:

				data.append({"id":pho_.id,"phone":pho_.contact,"sno":i})
				SoledSerial.objects.filter(id=pho_.id).update(serial_number=i,validation=True)

	status = SoledSerial.objects.filter(validation=False)
	for a in status:
		a.delete()
	# for pho_ in data[0]:
	# 	pho__s = pho_
	# nu = pho__s

	name = SoledSerial.objects.filter(validation=True)
	if request.method =='POST':
		stock_ids = request.POST.getlist('id[]')
		for id in stock_ids:
			stock = SoledSerial.objects.get(pk=id)
			stock.delete()
		return redirect('/Soled_Serial')
	return render(request, 'soled_serial.html',{'name':name.order_by('-date_time')})

@login_required
def SmSend(request, id):
	Sms = "Congratulations!!! You have been selected a winner in the ongoing Bueno Promo. Contact any of our offices for your win."
	phon = SoledSerial.objects.get(id=id)
	url = "https://www.bulksmsnigeria.com/api/v2/sms/create"
	header = {'Authorization':"Bearer suz31d4DL3irxcGZMhCEgk3tc4EXEeUrPJBpYjH1PoXJqKcrmRgUKRWsgd0a",'Content-type':'application/json','Accept': 'application/json'}
	params = {
	  	"to": str(phon),
	  	"from": "BUENO",
	  	"body": Sms,
	  	"gateway": "0",
	  	"append_sender": "0"
	}
	response = requests.post(url, headers=header, json=params)

	if response.status_code == 200:
		# return JsonResponse([{"message":"successfull","code":response.text}],safe=False)
		messages.success(request, "Sms Successfully sent!")
		# return redirect('/promo')
		return HttpResponseRedirect('/promo')
	else:
		# return JsonResponse([{"message":"error","code":response.status_code}],safe=False)
		messages.error(request, "Erorr!.. Sms not sent kindly check your sms Unit Ballance")
		# return redirect('/promo')
		return HttpResponseRedirect('/promo')

@login_required
def Success(request):
	return render(request,'success.html')

@login_required
def Error(request):
	return render(request,'error.html')

@login_required
def promo(request):
	for row in SoledSerial.objects.all().reverse():
		if SoledSerial.objects.filter(serial_number=row.serial_number).count() > 1:
			row.delete()
	SoledSerial.objects.all().distinct('serial_number','id')
	all_won = SoledSerial.objects.filter(winner=True).order_by('-date_time')
	try:
		if request.method == 'POST':
			count_ = int(request.POST.get("co"))
			amount = int(request.POST.get("am"))
			end_date = request.POST.get("st")
			start_date = request.POST.get("ed")
			# lotterys = list(SoledSerial.objects.all().values('serial_number','contact'))
			lotterys = list(SoledSerial.objects.filter(winner=False, validation=True, date_sold__lte=end_date, date_sold__gte=start_date).values('id','serial_number','contact').order_by('-date_time'))
			# return HttpResponse(lotterys)
			# for ser in lotterys:
			# 	lottery__ = []
			# 	lottery_ = lottery__.append(ser)
			# 	return HttpResponse(lottery_)
				# lottery = list(SoledSerial.objects.filter(status='Sold'))
			pickeds = lotterys[0:int(amount)]
			
			# return HttpResponse(pickeds)
			ticket = []
			# return HttpResponse(lottery)
			for ticket_number in range(count_):
				picked_number = shuffle(pickeds)
				picked_number = pickeds.pop()
				# picked_number = random.choice(lottery)
				# return HttpResponse(picked_number)
				ticket.append(picked_number)
				# avalable_number.remove(picked_number)
				# SoledSerial.objects.filter(id=).update(stock='Active')
			# UserMembership.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
			# return HttpResponse(ticket)
			lottery__ = []
			for value in ticket:
				temp = value
				# lottery__.append(temp['serial_number'])
				# lottery__.append(temp['contact'])
				instance = SoledSerial.objects.filter(id=temp['id']).update(winner=True)
			return redirect('/promo')

	except Exception as e:
		return JsonResponse([{"message":"error","reason":str(e)}],safe=False)

	context = {
		'serial':all_won,
	}
	return render(request, 'promo.html',context)


class LoginAPIView(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
	    serializer = self.get_serializer(data=request.data)
	    serializer.is_valid(raise_exception=True)
	    user = serializer.validated_data
	    return Response({
	        "user": UserSerializer(user, context=self.get_serializer_context()).data,
	        "token": AuthToken.objects.create(user)[1]
	    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_view(request, format=None):
    queryset = SoledSerial.objects.filter(winner=True,archived=False).order_by('-date_time')
    serializer = SoledSerializer(queryset,many=True)
    data = serializer.data
    user = request.user.id
    # return HttpResponse(data)
    return Response({
            'messages': 'Result retrieved successfully',
            'status': True,
            'data' : data,
            'user':user
        },status=status.HTTP_200_OK)   


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detail(request,pk,format=None):
    queryset = SoledSerial.objects.get(id=pk)
    serializer = SoledSerializer(queryset,many=False)
    data = serializer.data
    user = request.user.id

    # return HttpResponse(data)
    return Response({
            'messages': 'Result retrieved successfully',
            'status': True,
            'data' : data,
            'user':user
        },status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify(request,format=None):
	user_id = request.data['user_id']
	serial_id = request.data['sold_id']

	SoledSerial.objects.filter(id=serial_id).update(archived=True)

	instance = SoledSerial.objects.get(id=serial_id)


	Archive.objects.create(
	staff = request.user,
	serial_no = instance
	)


	# return HttpResponse(data)
	return Response({
	'messages': 'Created successfully',
	'status': True,
	},status=status.HTTP_200_OK)

@login_required
def archived(request,format=None):
	queryset = Archive.objects.all()

	data = []
	info = {}

	for i in queryset:
		info['id'] = i.id
		info['staff'] = i.staff.username
		info['serial_no'] = i.serial_no.serial_number
		info['date_created'] = i.date_created
		info['time_created'] = i.time_created
		info2 = info.copy()
		data.append(info2)



	# return HttpResponse(data)
	return render(request,'archived.html',{'data':data})