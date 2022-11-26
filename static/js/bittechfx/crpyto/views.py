from django.shortcuts import render, get_object_or_404, redirect,reverse,get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q,Count
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Details
from .models import Userwallet as UserWallet
from bitcoin import *
import bs4
import requests
import ipapi
# import numpy as np
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.views.generic import View
import datetime
import json
import uuid
import os
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from crpyto.forms import EmployeeForm, OrderForm,MembershipForm
from django.template import RequestContext
# Create your views here.
from django.db.models import F

@login_required
# @method_decorator(login_required, name='dispatch')https://cryptowat.ch/charts/KRAKEN:BTC-USD
def DashboardView(request):
	post = UserWallet.objects.all()
	user_post = None
	if request.user == None:

		user_post = post
	else:
		user_post = UserWallet.objects.filter(user=request.user)
	for posts in user_post:
		depo = posts.deposited
		prof = posts.profit
		bon = posts.bonus
		ref_b = posts.ref_bonus
	myposts = []

	balancese = depo + prof + bon + ref_b

	UserWallet.objects.filter(user=request.user).update(balance=balancese)
	user_wall = UserWallet.objects.filter(user=request.user)
	for bal in user_wall:
		ballan = bal.balance
	public_key = ballan
	# return HttpResponse('this what it showed ' + str(public_key))
	res2 = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
	res3 = requests.get('https://coinmarketcap.com/currencies/ethereum/')
	soup2 = bs4.BeautifulSoup(res2.text, 'xml')
	soup3 = bs4.BeautifulSoup(res3.text, 'xml')
	live_price = soup2.find_all('div', {'class': 'priceValue '})
	live_price3 = soup3.find_all('div', {'class': 'priceValue '})
	live_bitcoin_price = live_price[0].getText()	
	live_bitcoin_price1 = live_price[0].getText()
	live_bitcoin_price3 = live_price3[0].getText()	
	live_bitcoin_price31 = live_price3[0].getText()
	# res = requests.get('https://www.blockchain.com/btc/address/'+addr)
	res = public_key

	final_bal1_int = float(res)

	s3 =live_bitcoin_price1.replace(",","")
	e3 =live_bitcoin_price31.replace(",","")
	s3 =s3.replace("$","")
	e3 =e3.replace("$","")
	live_bitcoin_price1_int = float(s3)
	live_bitcoin_price1_int3 = float(e3)
	balance_usds = final_bal1_int*live_bitcoin_price1_int
	balance_usd3 = final_bal1_int*live_bitcoin_price1_int3
	# balance_usd = np.round(balance_usds, 8)
	# balance_usde = np.round(balance_usd3, 8)

	balance_usd = balance_usds
	balance_usde = balance_usd3
	detail = Details()

	detail.live_bitcoin_price = live_bitcoin_price
	detail.live_bitcoin_price1 = live_bitcoin_price1
	detail.live_bitcoin_price3 = live_bitcoin_price3
	detail.balance_usd = float(balance_usd)
	detail.balance_usd3 = float(balance_usde)
	# btcs = UserWallet.get(user=request.user, public_key)
	# btc = UserWallet.objects.filter(user=request.user.public_key)
	user_post = None
	if request.user == None:
		user_post = post
	else:
		user_post = UserWallet.objects.filter(user=request.user)
	for post in user_post:
		print(post.deposited)
	myposts = []
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	return render(request, 'crypto/Dashbord.html', {'detail':detail,'btc':post,'rest':final_bal1_int,'pos':pos})


# @login_required
# # @method_decorator(login_required, name='dispatch')https://cryptowat.ch/charts/KRAKEN:BTC-USD
# def DashboardView(request):
# 	if request.method == 'POST':
# 		addr = request.POST['addr']
# 		res2 = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
# 		soup2 = bs4.BeautifulSoup(res2.text, 'xml')
# 		live_price = soup2.find_all('div', {'class': 'priceValue '})
# 		# live_price = live_price.find_all('div', {'class': 'priceValue '})
			
# 		live_bitcoin_price = live_price[0].getText()
# 		print(live_bitcoin_price)
# 		print(live_bitcoin_price)
# 		print(live_bitcoin_price)
# 		print(live_bitcoin_price)
# 		live_bitcoin_price1 = live_price[0].getText()
# 		res = requests.get('https://www.blockchain.com/btc/address/'+addr)
# 		if res:
# 			soup = bs4.BeautifulSoup(res.text, 'lxml')
# 			# bal = soup.find_all('span', {'class': 'sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk'})
# 			bal = soup.find_all('span', {'class': 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC'})
# 			bal[4].getText()
# 			final_bal = bal[4].getText()
# 			final_bal1 = final_bal.replace(" ", "").rstrip()[:-3].upper()
# 			transactions = bal[1].getText()
# 			total_received = bal[2].getText()
# 			total_received1 = total_received.replace(" ", "").rstrip()[:-3].upper()
# 			total_sent = bal[3].getText()
# 			total_sent1 = total_sent.replace(" ", "").rstrip()[:-3].upper()
# 			final_bal1_int = float(final_bal1)
# 			total_received1_int = float(total_received1)
# 			total_sent1_int = float(total_sent1)
# 			live_bitcoin_price1_int = float(live_bitcoin_price1)
			
# 			balance_usd = final_bal1_int*live_bitcoin_price1_int
# 			total_received_usd = total_received1_int*live_bitcoin_price1_int
# 			total_sent_usd = total_sent1_int*live_bitcoin_price1_int
# 		else:
# 			return redirect('/')

# 		detail = Details()
# 		detail.balance = final_bal
# 		detail.balance1 = final_bal1
# 		detail.transactions = transactions
# 		detail.total_received = total_received
# 		detail.total_received1 = total_received1
# 		detail.total_sent = total_sent
# 		detail.total_sent1 = total_sent1
# 		detail.live_bitcoin_price = live_bitcoin_price
# 		detail.live_bitcoin_price1 = live_bitcoin_price1
# 		detail.balance_usd = int(balance_usd)
# 		detail.total_received_usd = int(total_received_usd)
# 		detail.total_sent_usd = int(total_sent_usd)


# 	else:
# 		detail = '   '
# 	# btcs = UserWallet.get(user=request.user, public_key)
# 	# btc = UserWallet.objects.filter(user=request.user.public_key)
# 	post = UserWallet.objects.all()
# 	user_post = None
# 	if request.user == None:

# 		user_post = post
# 	else:
# 		user_post = UserWallet.objects.filter(user=request.user)
# 	for post in user_post:
# 		print(post.deposited)
# 	myposts = []
	
# 	return render(request, 'crypto/Dashbord.html', {'detail':detail,'btc':post})


@login_required
def transaction(request):
	# btcs = UserWallet.get(user=request.user, public_key)
	# btc = UserWallet.objects.filter(user=request.user.public_key)

	user_post = Deposit_history.objects.filter(user=request.user)
	user_postd = Withdraw_request.objects.filter(user=request.user)
	user_postc = Deposit_history.objects.filter(user=request.user).count()
	user_postdc = Withdraw_request.objects.filter(user=request.user).count()
	# for post in user_post:
	# 	print(post.user)
	for p in user_postd:
		request.session['address'] = p.userwallet
	myposts = []

	addr = request.session['address']
	res2 = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
	soup2 = bs4.BeautifulSoup(res2.text, 'xml')
	live_price = soup2.find_all('div', {'class': 'priceValue '})
	live_bitcoin_price = live_price[0].getText()	
	live_bitcoin_price1 = live_price[0].getText()
	
	posty = UserWallet.objects.all()
	user_posts = UserWallet.objects.filter(user=request.user)
	for posts in user_posts:
		depo = posts.deposited
		prof = posts.profit
		bon = posts.bonus
		ref_b = posts.ref_bonus
	myposts = []

	balance = depo + prof + bon + ref_b

	public_key = balance

	res2 = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
	res3 = requests.get('https://coinmarketcap.com/currencies/ethereum/')
	soup2 = bs4.BeautifulSoup(res2.text, 'xml')
	soup3 = bs4.BeautifulSoup(res3.text, 'xml')
	live_price = soup2.find_all('div', {'class': 'priceValue '})
	live_price3 = soup3.find_all('div', {'class': 'priceValue '})
	live_bitcoin_price = live_price[0].getText()	
	live_bitcoin_price1 = live_price[0].getText()
	live_bitcoin_price3 = live_price3[0].getText()	
	live_bitcoin_price31 = live_price3[0].getText()
	# res = requests.get('https://www.blockchain.com/btc/address/'+addr)
	res = public_key

	final_bal1_int = float(res)

	s3 =live_bitcoin_price1.replace(",","")
	e3 =live_bitcoin_price31.replace(",","")
	s3 =s3.replace("$","")
	e3 =e3.replace("$","")
	live_bitcoin_price1_int = float(s3)
	live_bitcoin_price1_int3 = float(e3)
	balance_usds = final_bal1_int*live_bitcoin_price1_int
	balance_usd3 = final_bal1_int*live_bitcoin_price1_int3
	# balance_usd = np.round(balance_usds, 8)
	# balance_usde = np.round(balance_usd3, 8)

	balance_usd = balance_usds
	balance_usde = balance_usd3
	detail = Details()

	detail.live_bitcoin_price = live_bitcoin_price
	detail.live_bitcoin_price1 = live_bitcoin_price1
	detail.live_bitcoin_price3 = live_bitcoin_price3
	detail.balance_usd = float(balance_usd)
	detail.balance_usd3 = float(balance_usde)
	# btcs = UserWallet.get(user=request.user, public_key)
	# btc = UserWallet.objects.filter(user=request.user.public_key)
	# user_post = None
	# if request.user == None:
	# 	user_post = post
	# else:
	# 	user_post = UserWallet.objects.filter(user=request.user)
	# posttt = user_post
	# myposts = []
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	context = {
		'detail':detail,
		'post':user_post,
		'addr':addr,
		'wcount':user_postdc,
		'dcount':user_postc,
		'pos':pos
	}
	return render(request,'crypto/transaction.html', context)

def transaction_first(request):
	return render(request,'crypto/transaction_first.html')


# Create your views here.
def index(request, *args, **kwargs):
	# code = str(kwargs.get('ref_code'))
	# try:
	# 	referal = Referal.objects.get(code=code)
	# 	request.session['ref_profile']= referal.id
	# 	print('id', referal.id)
	# except:
	# 	pass
	# print(request.session.get_expiry_date())
	# data = ipapi.location(output='json')


	# def get_ip(request):
	# 	adress = request.META.get('HTTP_X_FORWARDED_FOR')
	# 	if adress:
	# 		ip = adress.split(',')[-1].split()
	# 	else:
	# 		ip = request.META.get('REMOTE_ADDR')
	# 	return ip
	# ip = get_ip(request)
	# u=User_ip(ip=ip)
	# print(ip)
	# result=User_ip.objects.filter(Q(ip__icontains=ip))
	# if len(result)==1:
	# 	print("user exist")
	# elif len(result)>1:
	# 	print("user exist more....")
	# else:
	# 	u.save()
	# 	print("user is unique")
	# count=User_ip.objects.all().count()
	# print("total user is",count)

	# addres = request.GET.get('addres')
	# city = request.GET.get('city')
	# country = request.GET.get('country')
	# languages = request.GET.get('languages')
	# latitude = request.GET.get('latitude')
	# longitude = request.GET.get('longitude')
	# timezone = request.GET.get('timezone')
	# call_code = request.GET.get('call_code')
	# currency = request.GET.get('currency')
	# org = request.GET.get('org')
	# c_code = request.GET.get('c_code')
	# postal = request.GET.get('postal')
	# utc_offset = request.GET.get('utc_offset')
	# u=Client_ips(addres=addres, city=city, country=country, languages=languages,latitude = latitude, longitude=longitude, timezone=timezone, country_calling_code=call_code,currency=currency, org=org, continent_code=c_code, postal=postal, utc_offset=utc_offset)
	# # u.save()
	# # instance = Client_ips.objects.create(addres=addres, city=city, country=country, languages=languages,latitude = latitude, longitude=longitude, timezone=timezone, country_calling_code=call_code,currency=currency, org=org, continent_code=c_code, postal=postal, utc_offset=utc_offset)
	# # # tutor_validator = instance.save(commit=False)
 # #    tutor_validator.user = self.request.user.tutor_profile 
	# # instance.save()
	# context = {"data": data}
	return render(request, 'crypto/index.html')

@login_required
def deposit(request):
	if request.method == 'POST':
		pode = Deposit_history()
		pode.amount = request.POST.get('amount')
		pode.currency = request.POST.get('currency')
		pode.user=request.user
		# pode.user.id=request.user.id
		if len(request.FILES) != 0:
			pode.prof = request.FILES['image']
		pode.save()
		template = render_to_string('crypto/deposit_massage.html',{
			"user": pode.user,
			"currency": pode.currency,
			"amount":pode.amount,
			"date":pode.created_date,
			"prof":pode.prof
			})
		send_mail('Deposit From '+ str(pode.user),
		template,
		settings.EMAIL_HOST_USER,
		# [settings.EMAIL_HOST_USER],
		['payment@bittechfx.com']
		)
		messages.success(request, 'Your Deposit have been submited Successfully')
		return redirect('/deposit')
	history = Deposit_history.objects.all()
	user_post = None
	if request.user == None:
		user_post = history
	else:
		user_post = Deposit_history.objects.filter(user=request.user)
	# for post in user_post:
	# 	print(post.user)
	post = user_post
	myposts = []
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	context = {
	'post':post,
	'pos':pos
	}
	return render(request,'crypto/deposit.html', context)

@login_required
def referal(request):
	profile = Referal.objects.get(user=request.user)
	my_recs = profile.get_recommended_referals()
	post = Referal.objects.all()
	user_post = None
	if request.user == None:

		user_post = post
	else:
		user_post = Referal.objects.filter(user=request.user)
	for post in user_post:
		print(post.code)
	myposts = []
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	context = {'my_recs':my_recs,'post':post,'pos':pos}
	return render(request,'crypto/referal.html',context)

@login_required
def withdraw(request):
	if request.method == 'POST':
		private_key = request.POST['btc']
		public_key = request.POST['pricet']
		withd = request.POST['types']
		addr = request.POST['addr']

		res2 = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
		soup2 = bs4.BeautifulSoup(res2.text, 'xml')
		live_price = soup2.find_all('div', {'class': 'priceValue '})
		live_bitcoin_price = live_price[0].getText()	
		live_bitcoin_price1 = live_price[0].getText()
		# res = requests.get('https://www.blockchain.com/btc/address/'+addr)
		res = public_key

		final_bal1_int = float(res)

		s3 =live_bitcoin_price1.replace(",","")
		s3 =s3.replace("$","")
		live_bitcoin_price1_int = float(s3)
		balance_usds = final_bal1_int/live_bitcoin_price1_int
		balance_usd = round(balance_usds, 4)
		detail = Details()

		detail.live_bitcoin_price = live_bitcoin_price
		detail.live_bitcoin_price1 = live_bitcoin_price1
		detail.balance_usd = int(balance_usd)
		post = UserWallet.objects.all()
		user_post = None
		if request.user == None:

			user_post = post
		else:
			user_post = UserWallet.objects.filter(user=request.user)
		for posts in user_post:
			depo = posts.deposited
			prof = posts.profit
			bon = posts.bonus
			ref_b = posts.ref_bonus
		myposts = []

		balance = depo + prof + bon + ref_b

		public = balance
		myposts = []

		price = float(res)
		if public <= price:
			messages.error(request, f'Your Account balance is not enough')
		else:
			request.session['price']= price
			request.session['btc']= private_key
			request.session['with']= withd
			request.session['addr']= addr
			return redirect('/collect_payment/btc/form=cloctpa&oq=cloctpa&aqs=chrome..69i57.7541j0j7&sourceid=chrome&ie=UTF-8/')
	history = Withdraw_request.objects.all()
	user_post = None
	if request.user == None:
		user_post = history
	else:
		user_post = Withdraw_request.objects.filter(user=request.user)
	# for post in user_post:
	# 	print(post.user)
	post = user_post
	myposts = []
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	context = {'post':post,'pos':pos}
	
	return render(request, 'crypto/withdraw.html', context)

def collect_payment(request):
	# context = {}
	# btc = request.POST.get('btc', None)
	# price = request.POST.get('pricet', None)
	# addr = request.POST.get('addr', None)

	# context['btc'] = btc
	# context['price'] = price
	# context['addr'] = addr
	price = request.session['price']
	btc = request.session['btc']
	addr = request.session['addr']
	wit = request.session['with']
	if request.method == 'POST':
		amount = request.POST['amount']
		currency = request.POST['currency']
		userwallet = request.POST['address']
		withdrew_from = request.POST['with']
		user=request.user
		instances = Withdraw_request.objects.create(user = user, amount=amount, currency=currency,withdrew_from=withdrew_from, userwallet=userwallet)
		instances.save()
		template = render_to_string('crypto/email_massage.html',{
			"user": instances.user,
			"currency": instances.currency,
			"amount":instances.amount,
			"userwallet":instances.userwallet,
			"withdraw_from":withdrew_from
			})
		send_mail('From '+ str(instances.user),
		template,
		settings.EMAIL_HOST_USER,
		['admin@bittechfx.com'],
		)
		messages.success(request, 'Your request has been sent Successfully')
		return redirect('/withdraw')
	context = {
		'price':price,
		'btc':btc,
		'addr':addr,
		'wi':wit
	}
	return render(request,'crypto/collect_payment.html', context)


def support(request):
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	return render(request, 'crypto/support.html',{'pos':pos})

# if pakage == 'Basic':
# 				return HttpResponse('the ' + str(balance_amount) +' ' + str(amounts) +''+ str(pakage))
# 				if float(amounts) > balance_amount:
# 					messages.error(request, 'minimum 100 of and Maximum of 4999 Required')
# 					return HttpResponse('itsss not enough'+ balance_amount + amounts)
# 					return redirect('/parkages')
# 				# elif float(amounts) < 100 or float(amounts) > 4999:
# 				# 	messages.error(request, 'minimum 100 of and Maximum of 4999 Required')
# 				# 	return HttpResponse('its bigeer or lee')
# 				# 	return redirect('/parkages')
# 				# else:
# 				# 	return HttpResponse('it works')
# 				# 	deposited = balance_amount - float(amounts)
# 				# 	UserWallet.objects.filter(user=request.user).update(deposited=deposited)
# 				# 	event = form.save(commit=False)
# 				# 	event.user = request.user
# 				# 	event.save()
# 				# 	messages.success(request, 'Your request has been add')
# 				# 	return redirect('/parkages')

# def parkages(request):
# 	form = MembershipForm()
# 	if request.method == 'POST':
# 		#print('Printing POST:', request.POST)
# 		form = MembershipForm(request.POST)
# 		if form.is_valid():
# 			pakage = form.cleaned_data.get('membership')
# 			amounts = form.cleaned_data.get('amount')
# 			user_wall = UserWallet.objects.filter(user=request.user)
# 			for bal in user_wall:
# 				ballan = bal.deposited
# 			balance_amount = float(ballan)
# 			amountes = float(amounts)
# 			if  amountes >= balance_amount and pakage == 'Basic':
# 				messages.error(request, 'minimum 100 of and Maximum of 4999 Required')
# 				return redirect('/parkages')
# 			else:
# 				pakage == 'Basic' and amountes < balance_amount or amountes < 4999 or amountes > 100
# 				# return HttpResponse(str(amountes) + ' ' + 'wow ' + str(pakage))
# 				deposited = balance_amount - float(amounts)
# 				UserWallet.objects.filter(user=request.user).update(deposited=deposited)
# 				event = form.save(commit=False)
# 				event.user = request.user
# 				event.save()
# 				messages.success(request, 'Your request has been add')
# 				return redirect('/parkages')

# 			if pakage == 'Silver' and float(amounts) > balance_amount or float(amounts) > 14999 or float(amounts) < 5000:
# 				messages.error(request, 'minimum 5000 of and Maximum of 14999 Required')
# 				return redirect('/parkages')	
# 			else:
# 				deposited = balance_amount - float(amounts)
# 				UserWallet.objects.filter(user=request.user).update(deposited=deposited)
# 				event = form.save(commit=False)
# 				event.user = request.user
# 				event.save()
# 				messages.success(request, 'Your request has been add')
# 				return redirect('/parkages')

# 			if pakage == 'Elite' and float(amounts) > balance_amount or float(amounts) < 200000:
# 				messages.error(request, 'minimum 200000 of and Maximum of Unlimited Required')
# 				return redirect('/parkages')	
# 			else:
# 				deposited = balance_amount - float(amounts)
# 				UserWallet.objects.filter(user=request.user).update(deposited=deposited)
# 				event = form.save(commit=False)
# 				event.user = request.user
# 				event.save()
# 				messages.success(request, 'Your request has been add')
# 				return redirect('/parkages')

# 			if pakage == 'Gold' and float(amounts) > balance_amount or float(amounts) > 49999 or float(amounts) < 15000:
# 				messages.error(request, 'minimum 15000 of and Maximum of 49999 Required')
# 				return redirect('/parkages')	
# 			else:
# 				deposited = balance_amount - float(amounts)
# 				UserWallet.objects.filter(user=request.user).update(deposited=deposited)
# 				event = form.save(commit=False)
# 				event.user = request.user
# 				event.save()
# 				messages.success(request, 'Your request has been add')
# 				return redirect('/parkages')

# 			if pakage == 'Platinum' and float(amounts) > balance_amount or float(amounts) > 199999 or float(amounts) < 50000:
# 				messages.error(request, 'minimum 50000 of and Maximum of 199999 Required')
# 				return redirect('/parkages')	
# 			else:
# 				deposited = balance_amount - float(amounts)
# 				# return HttpResponse(deposited)
# 				UserWallet.objects.filter(user=request.user).update(deposited=deposited)
# 				event = form.save(commit=False)
# 				event.user = request.user
# 				event.save()
# 				messages.success(request, 'Your request has been add')
# 				return redirect('/parkages')

# 		# amounts = request.POST['amount']
# 		# pakage = request.POST['pakage']


# 		# # if pakage == 'basic' & amounts > balance_amount || amounts > 4999 || amounts < 100:
# 		# if pakage == 'Basic' and float(amounts) > balance_amount or float(amounts) > 4999 or float(amounts) < 100:
# 		# 	messages.error(request, 'Your request has errr')
# 		# 	# return redirect('/parkages')
# 		# 	return HttpResponse(pakage)
# 		# else:
# 		# 	balance = balance_amount - float(amounts)
# 		# 	# return HttpResponse(bal)
# 		# 	UserWallet.objects.filter(user=request.user).update(balance=balance)
# 		# 	instance = UserMembership.objects.create(user=request.user, membership=2, amount=amounts)
# 		# 	instance.save()
# 		# 	messages.success(request, 'Your request has been add')
# 		# 	return redirect('/parkages')

# 	user_packages = UserMembership.objects.filter(user=request.user).order_by('-item_created_date')
# 	user_packages_count = UserMembership.objects.filter(user=request.user).count()
# 	# for package in user_packages:
# 	# 	pk = package.status
# 	user_postt = kycs.objects.filter(user=request.user)
# 	for postt in user_postt:
# 		pos = postt.status
# 	return render(request, 'crypto/parkages.html',{'pos':pos,'pk':user_packages.filter(appruved=True),"count":user_packages_count,'form':form})


def parkages(request):
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = MembershipForm(request.POST)
		if form.is_valid():
			pakage = form.cleaned_data.get('membership')
			amounts = form.cleaned_data.get('amount')
			user_wall = UserWallet.objects.filter(user=request.user)
			for bal in user_wall:
				ballan = bal.deposited
			balance_amount = float(ballan)
			amountes = float(amounts)
				# return HttpResponse(str(amountes) + ' ' + 'wow ' + str(pakage))
			deposited = balance_amount - amountes
			UserWallet.objects.filter(user=request.user).update(deposited=deposited)
			event = form.save(commit=False)
			event.user = request.user
			event.save()
			template = render_to_string('crypto/pakage_massage.html',{
				"user": event.user,
				"pakage": pakage,
				"amountes": amountes,
				})
			send_mail('Plan Request From '+ str(event.user),
			template,
			settings.EMAIL_HOST_USER,
			# [settings.EMAIL_HOST_USER],
			['admin@bittechfx.com']
			)
			messages.success(request, 'Your request has been add')
			return redirect('/parkages')
		else:
			form = MembershipForm(request.POST)
	else:
		form = MembershipForm()

	user_packages = UserMembership.objects.filter(user=request.user).order_by('-item_created_date')
	user_packages_count = UserMembership.objects.filter(user=request.user).count()
	# for package in user_packages:
	# 	pk = package.status
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	return render(request, 'crypto/parkages.html',{'pos':pos,'pk':user_packages.filter(appruved=True),"count":user_packages_count,'form':form})





@login_required
def adminPAR(request):
	employe = UserMembership.objects.filter(appruved=True).order_by('-item_created_date')
	employee = UserMembership.objects.filter(appruved=False).order_by('-item_created_date')
	return render(request,'crypto/adminPAR.html', {'employee':employee, 'employe':employe})

def pardestroy(request, id):  
	employee = UserMembership.objects.get(id=id)  
	employee.delete()
	messages.success(request, 'Transaction has been Deleted Successfully') 
	return redirect("/adminPAR")

# def edit(request, id):  
# 	employee = Deposit_history.objects.get(id=id) 
# 	return render(request,'crypto/edit.html', {'employee':employee})  

# def createOrders(request):
# 	form = EmployeeForm()
# 	if request.method == 'POST':
# 		#print('Printing POST:', request.POST)
# 		form = EmployeeForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')

# 	context = {'form':form}
# 	return render(request, 'crypto/createOrders.html', context)


# def update(request, id):  
# 	employee = Deposit_history.objects.get(id=id)  
# 	form = EmployeeForm(instance = employee)
# 	if request.method == 'POST':
# 		form = EmployeeForm(request.POST, instance=employee)
# 		if form.is_valid():  
# 			form.save()
# 			return redirect("/adminDT")  
# 	return render(request, 'crypto/edit.html', {'employee': employee,'form':form})  




@login_required
def adminDT(request):
	history = Deposit_history.objects.all()
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	return render(request, 'crypto/dt.html', {'history':history,'pos':pos})



def adminWD(request):
	history = Withdraw_request.objects.all()
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	return render(request, 'crypto/wd.html', {'history':history,'pos':pos})

@login_required
def all_user(request):
	user = User.objects.all()
	employee = UserWallet.objects.all()
	user_postt = kycs.objects.filter(user=request.user)
	for postt in user_postt:
		pos = postt.status
	return render(request, 'crypto/all_user.html', {'employee':employee,'user':user,'pos':pos})


def subscrib(request):
	plan = request.GET.get('sub_plane')
	fetch_membership = Membership.objects.filter(membership_type=plan).exists()
	if fetch_membership == False:
		return redirect('subscrib')
	membership = Membership.objects.get(membership_type=plan)
	price = float(membership.price)
	price2 = float(membership.price2)
	
	posty = UserWallet.objects.all()
	user_post = None
	if request.user == None:
		user_post = posty
	else:
		user_post = UserWallet.objects.filter(user=request.user)
	for posts in user_post:
		depo = posts.deposited
		prof = posts.profit
		bon = posts.bonus
		ref_b = posts.ref_bonus
	myposts = []

	balance = depo + prof + bon + ref_b

	public_key = balance

	res = price
	res2 = price2
	if public_key < price and price2:
		messages.error(request, f'Your Account balance is not enough')
		return redirect('/parkages')
	else:
		instance = PayHistory.objects.create(amount=res, payment_for=membership, user=request.user)
		UserMembership.objects.filter(user=instance.user).update(membership=membership)
		PayHistory.objects.filter(user=instance.user).update(paid=True)
		messages.success(request, 'Your request has been sent Successfully')
		return redirect('/dashboard')

	# instance = PayHistory.objects.create(amount=amount, payment_for=membership, user=request.user)
	# UserMembership.objects.filter(user=instance.user).update()
	# PayHistory.objects.filter(user=instance.user).update(paid=True)
	# new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
	# instance = Membership.objects.get(id=new_payment.payment_for.id)
	# return redirect('/subscribed')  
	
	return render(request, 'crypto/subscrib.html')


# @login_required
def kyc(request):
	if request.method == 'POST':
		pode = kycs()
		pode.id_type = request.POST.get('idname')
		pode.id_number = request.POST.get('id')
		pode.user=request.user
		if len(request.FILES) != 0:
			pode.id_front = request.FILES['idimage1']
			pode.id_back = request.FILES['idimage2']
			pode.id_body = request.FILES['idimage3']
		pode.save()
		template = render_to_string('crypto/kyc_massage.html',{
			"user": pode.user,
			"id_type": pode.id_type,
			"id_front": pode.id_front,
			"id_back":pode.id_back,
			"id_body":pode.id_body,
			"id_number":pode.id_number
			})
		send_mail('KYC From '+ str(pode.user),
		template,
		settings.EMAIL_HOST_USER,
		# [settings.EMAIL_HOST_USER],
		['admin@bittechfx.com']
		)
		messages.success(request, 'Your credentials have been submited Successfully')
		return redirect('/kycmassage')
	pos = kycs.objects.all()
	return render(request,'crypto/kyc.html',{'pos':pos})

def kycmassage(request):
	return render(request,'crypto/kycmassage.html')

def edit(request, id):  
	employee = Deposit_history.objects.get(id=id) 
	return render(request,'crypto/edit.html', {'employee':employee})  

def createOrders(request):
	form = EmployeeForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = EmployeeForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'crypto/createOrders.html', context)


def update(request, id):  
	employee = Deposit_history.objects.get(id=id)  
	form = EmployeeForm(instance = employee)
	if request.method == 'POST':
		form = EmployeeForm(request.POST, instance=employee)
		if form.is_valid():  
			form.save()
			return redirect("/adminDT")  
	return render(request, 'crypto/edit.html', {'employee': employee,'form':form})  


def destroy(request, id):  
	employee = Deposit_history.objects.get(id=id)  
	employee.delete()
	messages.success(request, 'Transaction has been Deleted Successfully') 
	return redirect("/adminDT")

def massage(request, id):  
	employee = Deposit_history.objects.get(id=id)
	return render(request, 'crypto/massage.html', {'employee':employee})

def approvalmail(request, id):  
	employee = Deposit_history.objects.get(id=id)
	if request.method == 'POST':
		user = employee.user
		email = employee.user.email
		amount = employee.amount
		currency = employee.currency
		template = render_to_string('crypto/trans_massage.html',{
			"user": user,
			"currency": currency,
			"amount":amount
		})
		send_mail('From Bittechfx',
		template,
		settings.EMAIL_HOST_USER,
		[email],
		)
		messages.success(request, 'Mail has been sent Successfully')
		# return redirect('/withdraw') 
		return redirect("/adminDT")
	return render(request, 'crypto/send.html', {'employee': employee}) 

def declinmail(request, id):  
	employee = Deposit_history.objects.get(id=id)
	if request.method == 'POST':
		user = employee.user
		email = employee.user.email
		amount = employee.amount
		currency = employee.currency
		template = render_to_string('crypto/decli_massage.html',{
			"user": user,
			"currency": currency,
			"amount":amount
		})
		send_mail('From Bittechfx',
		template,
		settings.EMAIL_HOST_USER,
		[email],
		)
		messages.success(request, 'Mail has been sent Successfully')
		# return redirect('/withdraw') 
		return redirect("/adminDT")
	return render(request, 'crypto/send.html', {'employee': employee}) 

def destroyw(request, id):
	employee = Withdraw_request.objects.get(id=id)  
	employee.delete()
	messages.success(request, 'Transaction has been Deleted Successfully')
	return redirect("/adminDT")

# def exchanged_rate(amount):
#     url = "https://www.blockonomics.co/api/price?currency=USD"
#     r = requests.get(url)
#     response = r.json()
#     return amount/response['price']



# def create_payment(request, pk):
#     price = request.GET.get('price')
#     product_id = pk
#     product = Product.objects.get(id=product_id)
#     url = 'https://www.blockonomics.co/api/new_address'
#     headers = {'Authorization': "Bearer " + settings.API_KEY}
#     r = requests.post(url, headers=headers)
#     print(r.json())
#     if r.status_code == 200:
#         address = r.json()['address']
#         bits = exchanged_rate(price)
#         order_id = uuid.uuid1()
#         invoice = Invoice.objects.create(order_id=order_id,
#                                 address=address,btcvalue=bits*1e8, product=product)
#         return HttpResponseRedirect(reverse('payments:track_payment', kwargs={'pk':invoice.id}))
#     else:
#         print(r.status_code, r.text)
#         return HttpResponse("Some Error, Try Again!")
#     return render(request, 'crypto/payment.html')



# def track_invoice(request, pk):
#     invoice_id = pk
#     invoice = Invoice.objects.get(id=invoice_id)
#     data = {
#             'order_id':invoice.order_id,
#             'bits':invoice.btcvalue/1e8,
#             'value':invoice.product.price,
#             'addr': invoice.address,
#             'status':Invoice.STATUS_CHOICES[invoice.status+1][1],
#             'invoice_status': invoice.status,
#         }
#     if (invoice.received):
#         data['paid'] =  invoice.received/1e8
#         if (int(invoice.btcvalue) <= int(invoice.received)):
#             data['path'] = invoice.product.product_image.url
#     else:
#         data['paid'] = 0  

#     return render(request,'invoice.html',context=data)

	
# def receive_payment(request):
	
#     if (request.method != 'GET'):
#         return 
	
#     txid  = request.GET.get('txid')
#     value = request.GET.get('value')
#     status = request.GET.get('status')
#     addr = request.GET.get('addr')

#     invoice = Invoice.objects.get(address = addr)
	
#     invoice.status = int(status)
#     if (int(status) == 2):
#         invoice.received = value
#     invoice.txid = txid
#     invoice.save()
#     return HttpResponse(200)

# def IpSearch(request):
 
#         search = request.POST.get('search')
	 
#         data = ipapi.location(ip=search, output='json')
 
#         context = {"data": data}
 
#         return render(request, 'index.html', context)



# template = render_to_string('report/custormer_portal/email_massage.html',{
# 				"user": u_name,
# 			 	"email": email,
# 			  	"acc":u_acco,
# 			    "password":password
# 			})
# 			send_mail('From EEDC',
#             template,
#             settings.EMAIL_HOST_USER,
#             [email],
#             )





def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'crypto/order_form.html', context)

# def updateOrder(request, pk):

# 	order = UserWallet.objects.get(id=pk)
# 	form = OrderForm(instance=order)

# 	if request.method == 'POST':
# 		form = OrderForm(request.POST, instance=order)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/all_user') 

# 	context = {'form':form}
# 	return render(request, 'crypto/order_form.html', context)


def updateOrder(request, pk):

	order = UserWallet.objects.get(id=pk)
	# form = OrderForm(instance=order)
	fs = order.user

	if request.method == 'POST':
		dp = request.POST['number']
		UserWallet.objects.filter(user=fs).update(deposited=F('deposited') + dp)
		messages.success(request, 'Your request has been sent Successfully')
		return redirect('/all_user')
		# form = OrderForm(request.POST, instance=order)
		# for forr in form:
		# 	balance_usd = forr.deposited
		# 	pr

		# if form.is_valid():
		# 	form.save()
		# 	return redirect('/all_user') 

	# context = {'form':form}
	return render(request, 'crypto/order_form.html', {'employee': order})


def updateOrder1(request, pk):

	order = UserWallet.objects.get(id=pk)
	# form = OrderForm(instance=order)
	fs = order.user

	if request.method == 'POST':
		dp = request.POST['bnumber']
		UserWallet.objects.filter(user=fs).update(bonus=F('bonus') + dp)
		messages.success(request, 'Your request has been sent Successfully')
		return redirect('/all_user')
		# form = OrderForm(request.POST, instance=order)
		# for forr in form:
		# 	balance_usd = forr.deposited
		# 	pr

		# if form.is_valid():
		# 	form.save()
		# 	return redirect('/all_user') 

	# context = {'form':form}
	# return render(request, 'crypto/order_form.html', {'employee': order})

def updateOrder2(request, pk):

	order = UserWallet.objects.get(id=pk)
	# form = OrderForm(instance=order)
	fs = order.user

	if request.method == 'POST':
		dp = request.POST['cnumber']
		UserWallet.objects.filter(user=fs).update(profit=F('profit') + dp)
		messages.success(request, 'Your request has been sent Successfully')
		return redirect('/all_user')
		# form = OrderForm(request.POST, instance=order)
		# for forr in form:
		# 	balance_usd = forr.deposited
		# 	pr

		# if form.is_valid():
		# 	form.save()
		# 	return redirect('/all_user') 

	# context = {'form':form}
	# return render(request, 'crypto/order_form.html', {'employee': order})

def updateOrder3(request, pk):

	order = UserWallet.objects.get(id=pk)
	# form = OrderForm(instance=order)
	fs = order.user

	if request.method == 'POST':
		dp = request.POST['dnumber']
		UserWallet.objects.filter(user=fs).update(ref_bonus=F('ref_bonus') + dp)
		messages.success(request, 'Your request has been sent Successfully')
		return redirect('/all_user')
		# form = OrderForm(request.POST, instance=order)
		# for forr in form:
		# 	balance_usd = forr.deposited
		# 	pr

		# if form.is_valid():
		# 	form.save()
		# 	return redirect('/all_user') 

	# context = {'form':form}
	# return render(request, 'crypto/order_form.html', {'employee': order})


def deleteOrder(request, pk):
	order = UserWallet.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'crypto/delete.html', context)