from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.form import CategoryForm, PageForm
from rango.form import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.decorators import login_required



@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")



@login_required
def user_logout(request):
	#Since we know the user is logged in,we can now just log them out
	logout(request)
	#Take the user back to the homepage
	return HttpResponseRedirect('/rango/')




def user_login(request):
	if request.method=='POST':
		username = request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango')
			else:
				return HttpResponse("your Rango account is disabled")
		else:
			print "Invalid login details:{0},{1}".format(username,password)
			return HttpResponse("Invalid login details supplied")
	else:
		return render(request,'rango/login.html',{})


def register(request):
	registered=False 
	if request.method == 'POST':
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()
			profile=profile_form.save(commit=False)
			profile.user=user 

			if 'picture' in request.FILES:
				profile.picture =request.FILES['picture']

			profile.save()
			registered=True 
		else:
			print user_form.errors,profile_form.errors 
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()
	return render(request,'rango/register.html', 
			{'user_form':user_form,
			'profile_form':profile_form,
			'registered':registered})





#post  add-category
@login_required
def add_category(request):
	print "fuck here"
	if request.method =='POST':
		form =CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit =True)
			return index(request)
		else:
			print form .errors
	else:
		form =CategoryForm()
	return render(request,'rango/add_category.html',{'form':form})	

#post page
def add_page(request,category_name_slug):
	try:
		cat=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat =None

	if request.method=='POST':
		form =PageForm(request.POST)
		if form.is_valid():
			if cat:
				page=form.save(commit=True)
				page.category=cat 
				page.views=0
				page.save()
				return category(request,Category_name_slug)
			else:
				print form.errors
	else:
		form =PageForm()
		context_dict={'form':form,'category':cat}
	return render(request,'rango/add_page.html',context_dict)


def category(request, category_name_slug):
	context_dict = {} 
	print "fuck here*******************"
	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
		context_dict['category_name_slug']=category_name_slug 
	except Category.DoesNotExist:
		pass

	return render(request, 'rango/category.html', context_dict)




#def index(request):
#	return HttpResponse("<br/>Rango says hey there world!")

def index(request):
	category_list=Category.objects.all()
	context_dict = {'categories':category_list}
	return render(request,'rango/index.html',context_dict)

def about(request):
	xianhua_dict={'xianhua':"I Love You"}
	return render(request,'rango/about.html',xianhua_dict)
