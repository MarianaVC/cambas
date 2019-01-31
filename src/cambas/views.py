from django.shortcuts import render,redirect

def index(request):
	if request.user.is_authenticated():

		return redirect('users/profile')
	else:
		return render(request,'index.html',{'valid':True})


def sing_up(request):
	if request.user.is_authenticated():
		return redirect('users/profile')
	else:		
		return render(request,'sing-up.html',{'valid':True})