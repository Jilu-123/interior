from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from app.models import  *
import os
import datetime


# Create your views here.
def myfun(request):
	a=("hello iam here")
	return HttpResponse(a)

def index(request):
	prd=table_product.objects.all()
	return render(request,'index.html',{"data":prd})


def about(request):
	return render(request,'about.html')


def contact(request):
	return render(request,'contact.html')


def services(request):
	return render(request,'services.html')	
	
def userreg(request):
    if request.method=="POST":
    	fname=request.POST['w3lName']
    	lname=request.POST['w3lName1']
    	cemail=request.POST['email']
    	cage=request.POST['age']
    	caddress=request.POST['address']
    	cpassword=request.POST['password']
    	add=table_user(firstname=fname,lastname=lname,email=cemail,age=cage,address=caddress,password=cpassword)
    	add.save()
    	return render(request,'userreg.html')
    else:
    	return render(request,'userreg.html')


def product(request):
	if request.session.has_key('myid'):

	    if request.method=="POST":
	    	fname=request.POST['w3lName']
	    	ccategory=request.POST['category']
	    	cprice=request.POST['w3lName1']
	    	cquantity=request.POST['quantity']
	    	cdetails=request.POST['details']
	    	cfileupload=request.FILES['file']
	    	
	    	add=table_product(name=fname,category=ccategory,price=cprice,quantity=cquantity,details=cdetails,fileupload=cfileupload)
	    	add.save()
	    	return render(request,'product.html')
	    else:
	    	return render(request,'product.html')
	else:
	 	return render(request,'login.html')




def login(request):
	if request.method=="POST":
		cemail=request.POST['email']
		cpassword=request.POST['password']
		# crpassword=request.POST['rpassword']
		check=table_user.objects.filter(email=cemail,password=cpassword)
		if check:
			for x in check:
				request.session["myid"]=x.id
			return render(request,'index.html',{"sucess":" pass matches"})
		else:
			return render(request,'login.html',{"error":"  doesnot matches"})
	else:
		return render(request,'login.html')


def logout(request):
	if request.session.has_key('myid'):
		del request.session['myid']
		logout(request)
	return HttpResponseRedirect('/')

def image(request):
	ii=request.GET['id']
	prd=table_product.objects.filter(id=ii)
	return render(request,'image.html',{"db":prd})





def viewproduct(request):
	query=table_product.objects.all()
	return render(request,'viewproduct.html',{"qry":query})

def edit(request):
	id1=request.GET['id']
	query=table_product.objects.all().filter(id=id1)
	return render(request,'update.html',{"db":query})

def update(request):
	if request.method=="POST":
		fname=request.POST['w3lName']
		ccategory=request.POST['category']
		cprice=request.POST['w3lName1']
		cdetails=request.POST['details']
		# cfileupload=request.FILES['file']
		#userid=request.POST['usrid']
		imgup=request.POST['image']
		uid=request.GET['id']
		if imgup=='Yes':
			image1=request.FILES['file']
			oldrec=table_product.objects.all().filter(id=uid)
			updrec=table_product.objects.get(id=uid)
			for x in oldrec:
				imgurl=x.fileupload.url
				pathtoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imgurl
				if os.path.exists(pathtoimage):
					os.remove(pathtoimage)
					print('Successfully deleted')
			updrec.fileupload=image1
			updrec.save()
		table_product.objects.filter(id=uid).update(name=fname,category=ccategory,price=cprice,details=cdetails)
		return HttpResponseRedirect('/viewproduct/')
	else:
		return HttpResponseRedirect('/viewproduct/')

def delete(request):
	ids=request.GET['id']
	query=table_product.objects.all().filter(id=ids)
	table_product.objects.filter(id=ids).delete()
	query1=table_product.objects.all()
	return render(request,'viewproduct.html',{"qry":query1})

def addtocart(request):
	if request.session.has_key('myid'):
		if request.method=="POST":
			pids=request.GET['id']
			prd=table_product.objects.all().filter(id=pids)
			for x in prd:
				unitprice=x.price			
			qty=request.POST['qty']
			print(qty,'**************************************----------------')
			shipping=int(int(unitprice)*10/100)
			total=int(unitprice)*int(qty)+shipping
			date= datetime.datetime.now()
			ii=request.session["myid"]
			print(ii)				
			pid=table_product.objects.get(id=pids)
			ii=table_user.objects.get(id=ii)
			check=table_cart.objects.all().filter(user_id=ii,product_id=pids,price=unitprice,total=total,date=date)
			
			if check:
				myprd=table_cart.objects.all().filter(user_id=ii,status='pending')
				return render(request,'cart.html',{'uv':myprd,'msgkey':'Already Add to cart'})
			else:
				tocart=table_cart(user_id=ii,product_id=pid,price=unitprice,total=total,date=date,quantity=qty)
				tocart.save()
				pdr=table_product.objects.all().filter(id=pids)
				for x in pdr:
					oldqty=x.quantity
				newqty=int(oldqty)-int(qty)
				table_product.objects.all().filter(id=pids).update(quantity=newqty)
				mycart=table_cart.objects.all().filter(user_id=ii,status='pending')
				grandtotal=0
				for x in mycart:
					grandtotal=int(x.total)+grandtotal
				myprd=table_cart.objects.all().filter(user_id=ii,status='pending')
				return render(request,'cart.html',{'uv':myprd,'gt':grandtotal,'msgkey':'Add to cart'})
	else:
		print("*************************************************************")
		return render(request,'login.html')
    
def deletecart(request):
	ids=request.GET['id']
	ii=request.session["myid"]

	cartprd=table_cart.objects.all().filter(id=ids)
	for x in cartprd:
		pid=x.product_id.id
		qty=x.quantity
	prd=table_product.objects.filter(id=pid)
	for x in prd:
		oldqty=x.quantity
	newqty=int(oldqty)+int(qty)
	table_product.objects.filter(id=pid).update(quantity=newqty)
	table_cart.objects.filter(id=ids).delete()
	mycart=table_cart.objects.all().filter(user_id=ii,status='pending')
	grandtotal=0
	for x in mycart:
		grandtotal=int(x.total)+grandtotal
	mypet=table_cart.objects.all().filter(user_id=ii,status='pending')

	return render(request,'cart.html',{'uv':mypet,'gt':grandtotal,'msg':'Successfully deleted'})
  
  
	# return render(request,'cart.html',{"uv":cartprd})

	############  PAYMENT ##################
def buynow(request):
	if request.method=="POST":
		gt=request.GET['gt']
		pid=request.POST['pid']


		
		ii=request.session['myid']
		print(pid,'************')

		user=table_user.objects.filter(id=ii)

		return render(request,'indexpayment.html',{"amount":gt,"user":user})

def makepayment(request):
	if request.method=="POST":
		# ii=request.session['myid']

		amount=request.POST['amnt']
		ii=request.POST['uid']

		uid=table_user.objects.get(id=ii)
		print(uid,"<<<<<<<<<<<<<")
		date= datetime.datetime.now()

		print(uid,"+++++++++++++++")

		check=table_payment.objects.filter(user_id=uid,amount=amount,date=date)
		if check:
			return HttpResponseRedirect('/')
		else:
			table_cart.objects.filter(user_id=uid).update(status='paid')
			
			add=table_payment(user_id=uid,amount=amount,date=date,status='paid')
			add.save()
			return HttpResponseRedirect('/')


def cart(request):
	if request.session['myid']:
		ii=request.session['myid']
		mycart=table_cart.objects.filter(user_id=ii,status='pending')
		grandtotal=0
		for x in mycart:
			grandtotal=int(x.total)+grandtotal
			mypet=table_cart.objects.all().filter(user_id=ii,status='pending')
			if mypet:
				return render(request,'cart.html',{'uv':mypet,'gt':grandtotal})
			
		return render(request,'cart.html')

	else:
		return render(request,'login.html')


def clearmycart(request):
	ii=request.session['myid']
	table_cart.objects.filter(user_id=ii,status='pending').delete()
	return HttpResponseRedirect('/')


