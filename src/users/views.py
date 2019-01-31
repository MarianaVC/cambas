#users/views.py

from django.shortcuts import render,redirect
from .models import User
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import facebook
from rest_framework.authtoken.models import Token
import json
from django.http import HttpResponseNotFound,HttpResponseRedirect


#======API ======

@csrf_exempt
def facebook_login_api(request):
	"""Funtion for login and register with Facebook
		:return:token for authorization or error
	"""
	try:
		data = json.loads(request.body.decode('utf-8'))
		access_token = data.get('accessToken')

	except (ValueError, KeyError) as e:
		return JsonResponse({'error':'you most provide an accessToken'}, safe = False, status=400)
	
	new_user = False
	try:
		graph = facebook.GraphAPI(access_token=access_token)
		user_info = graph.get_object(
			id='me',
			fields='first_name, middle_name, last_name, id, '
			'currency, hometown, location, locale, '
			'email, gender, interested_in, picture.type(large),'
			' birthday, cover')
	except facebook.GraphAPIError:
		return JsonResponse({'error': 'invalid data'}, safe=False, status=403)
	try:
		user = User.objects.get(facebook_id=user_info.get('id'))

	except User.DoesNotExist:
		password = User.objects.make_random_password()
		user = User(
			first_name=user_info.get('first_name'),
			last_name=user_info.get('last_name'),
			email=user_info.get('email')
			or '{0} without email'.format(user_info.get('last_name')),
			facebook_id=user_info.get('id'),
			profile_image=user_info.get('picture')['data']['url'],	
			created_at=datetime.now(),
			username=user_info.get('email') or user_info.get('last_name'),
			gender=user_info.get('gender'),
			is_active=1)
		user.set_password(password)
		user.save()
		new_user = True

	token = Token.objects.get(user=user).key
	if token:
		return JsonResponse({'auth_token': token, 'new_user': new_user},
							safe=False, status = 200)
	else:
		return JsonResponse({'error': 'Invalid data'}, safe=False, status=400)

@csrf_exempt
def login_api(request):
	"""Function for login with password and Email
	   :return: token for authorization or error 
	"""
	from django.contrib.auth import authenticate
	try:
		data = json.loads(request.body.decode('utf-8'))
		username = data.get('username')
		password = data.get('password')
		user = authenticate(username=username, password=password)
		token = Token.objects.get(user=user).key

		if token:
			return JsonResponse({'auth_token': token, 'new_user':False}, safe=False, status=200)
		else:
			return JsonResponse({'error': 'Invalid data'}, safe=False, status=400)
	
	except (ValueError, KeyError) as e:
		return JsonResponse({'error':'you most provide username and password'}, safe = False, status=400)		

	except Token.DoesNotExist:
		return JsonResponse({'error':'invalid username or password'}, safe = False, status = 400)



@csrf_exempt
def register(request):
	from django.db import IntegrityError
	from django.utils import timezone

	"""Funcion for register with password and Email
	   :return: token for authorization or error.
	"""
	try:
		data = json.loads(request.body.decode('utf-8'))
		email = data.get('email')
		password = data.get('password')
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		username = data.get('username')
		gender = data.get('gender')

	except (ValueError, KeyError) as e:
		return JsonResponse({'error':'you most provide all fields'}, safe = False, status=400)
	
	try:
		user = User.objects.get(email=email)
		return JsonResponse({'error':'a user with this email already registered'}, safe = False, status = 400)
	except User.DoesNotExist:
		#this is ok
		user = User(
			first_name= first_name,
			last_name= last_name,
			email= email,
			facebook_id= "",
			profile_image= "",	
			created_at= timezone.now(),
			username= username,
			gender= gender,
			is_active=1)
		user.set_password(password)
		try:
			user.save()
		except IntegrityError as e:
			return JsonResponse({'error':'a user with this username already exists'}, safe=False, status=400)	
		
		new_user = True		
		token = Token.objects.get(user=user).key
		login(request,user)
		if token:
			return JsonResponse({'auth_token': token, 'new_user': new_user},safe=False,status = 200)
		else:
			return JsonResponse({'error': 'Invalid data'}, safe=False, status=400)

@csrf_exempt
def update_profile(request):
	"""Function for updating a user profile, user has to be in session to be able to use it
	   :return: json reposponse with status 200 or error
	"""	
	if request.user.is_authenticated() and request.method == 'POST':
		try:
			user = User.objects.get(pk = request.user.id)
			print(request.FILES)
			if len(request.FILES) > 0:
				print("aqui")
				print(request.FILES['profile_image'])
				profile_image = request.FILES['profile_image']
			else:
				profile_image = user.profile_image

			user.first_name = request.POST.get('firstname')
			user.last_name = request.POST.get('lastname')
			user.phone = request.POST.get('phone') 
			user.profile_image = profile_image
			user.email = request.POST.get('email')
			user.middle_name = request.POST.get('middlename')
			user.save()
			return redirect('/users/profile/')
		except Exception as e:
			print(e)				
	else:
		return HttpResponseNotFound("Content not found")  
		
#====== Views ======

def my_profile(request):
	"""My profile view"""
	if request.user.is_authenticated():

		user = User.objects.get(pk = request.user.id)

		return render(request,'users/profile.html',{'user':user})
	else:
		return HttpResponseNotFound("Content not found")  

@csrf_exempt
def facebook_login_web(request):
	"""Function for login with password and Email
	   :return: user authenticated and profile view
	"""
	from django.contrib.auth import authenticate, login	
	if (request.method == 'POST'):
		try:
			data = request.POST
			access_token = data.get('accessToken')
		except (ValueError, KeyError) as e:
			return JsonResponse({'error':'you most provide an accessToken'}, safe = False, status=400)		
		new_user = False
		try:
			graph = facebook.GraphAPI(access_token=access_token)
			user_info = graph.get_object(
				id='me',
				fields='first_name, middle_name, last_name, id,'
				'email, gender, interested_in, picture.type(large),'
				' birthday, cover')
		except facebook.GraphAPIError:
			return JsonResponse({'error': 'invalid data'}, safe=False, status=403)
		try:
			user = User.objects.get(facebook_id=user_info.get('id'))
	
		except User.DoesNotExist:
			password = User.objects.make_random_password()
			user = User(
				first_name=user_info.get('first_name'),
				last_name=user_info.get('last_name'),
				email=user_info.get('email')
				or '{0} without email'.format(user_info.get('last_name')),
				facebook_id=user_info.get('id'),
				profile_image=user_info.get('picture')['data']['url'],	
				created_at=datetime.now(),
				username=user_info.get('email') or user_info.get('last_name'),
				gender=user_info.get('gender'),
				is_active=1)
			user.set_password(password)
			user.save()
			new_user = True
			
		token = Token.objects.get(user=user).key
		login(request, user)
		if token:
			return JsonResponse({'status':'ok'}, status = 200)
		else:
			return JsonResponse({'error': 'Invalid data'}, safe=False, status=400)
	else:
		return JsonResponse({'error':'bad request method'}, safe = False, status=400)
		
def login_web(request):
	"""Login Function for web"""
	from django.contrib.auth import authenticate, login
	if (request.method == 'POST'):
		try:
			data = request.POST
			username = data.get('username')
			password = data.get('password')
			user = authenticate(username=username, password=password)
			token = Token.objects.get(user=user).key
			login(request,user)
			if token:
				return redirect('/users/profile')
			else:
				return JsonResponse({'error': 'Invalid data'}, safe=False, status=400)
				
		except (ValueError, KeyError) as e:
			return JsonResponse({'error':'you most provide username and password'}, safe = False, status=400)			

		except Token.DoesNotExist:
		 	return render(request,'index.html',{'valid':False})

	else:
		return HttpResponseNotFound("Content not found")  

def sing_up_web(request):
	"""Sing up for web"""		     
	from django.contrib.auth import authenticate, login
	from django.utils import timezone

	if (request.method == 'POST'):
		try:
			data = request.POST
			email = data.get('email')
			password = data.get('password')
			first_name = data.get('firstname')
			last_name = data.get('lastname')
			username = data.get('username')
	
		except (ValueError, KeyError) as e:
			return JsonResponse({'error':'you most provide all fields'}, safe = False, status=400)		
	
		try:
			user = User.objects.get(email=email)
			return render(request,'sing-up.html',{'valid':False})
		except User.DoesNotExist:
			#this is ok
			user = User(
				first_name= first_name,
				last_name= last_name,
				email= email,
				facebook_id= "",
				created_at= timezone.now(),
				username= username,
				is_active=1)
			user.set_password(password)
		try:
			user.save()
			new_user = True	
			token = Token.objects.get(user=user).key
			login(request,user)
			return redirect('/users/profile')		

		except IntegrityError as e:
		 	return render(request,'sing-up.html',{'valid':False})		

		except Token.DoesNotExist:
		 	return render(request,'sing-up.html',{'valid':False})

	else:
		return HttpResponseNotFound("Content not found")  

def fanpage(request):
	import requests

	url = "https://graph.facebook.com/oauth/access_token?client_id=1111248135724804&client_secret=ad76d19ea6fc74a25a7183283170a2af&grant_type=client_credentials"
	resp = requests.get(url, params = []).json()
	access_token = (resp['access_token'])
	posts = "https://graph.facebook.com/v2.9/LADbible/posts?access_token="+access_token
	data = requests.get(posts, params = []).json
	return render(request,'users/fanpage.html',{'data':data})

def logout_user(request):
	from django.contrib.auth import logout
	"""Log out"""	
	logout(request)
	return redirect('/')
