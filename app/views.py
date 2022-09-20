from django import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced,Feedback
from .forms import  CustomerRegistrationForm,CustomerProfileForm,feedbackForm
from django.contrib import messages
from app import models
from app.models import Customer
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .serializers import CustomerSerializer, OrderPlacedSerializer,ProductSerializer,CartSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def customer(request):
    if request.method == "GET":
        regis = Customer.objects.all()
        print("students = ", regis)
        serializer = CustomerSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")

@csrf_exempt
def product(request):
    if request.method == "GET":
        regis = Product.objects.all()
        print("students = ", regis)
        serializer = ProductSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")

@csrf_exempt
def carts(request):
    if request.method == "GET":
        regis = Cart.objects.all()
        print("students = ", regis)
        serializer = CartSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")

@csrf_exempt
def orderplaced(request):
    if request.method == "GET":
        regis = OrderPlaced.objects.all()
        print("students = ", regis)
        serializer = OrderPlacedSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = RegistraionSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)
    return HttpResponse("success")



class ProductView(View):
  def get(self, request):
     totalitem=0
     chair= Product.objects.filter(category='ch')
     table= Product.objects.filter(category='tb')
     officechair= Product.objects.filter(category='oc')
     officetable=Product.objects.filter(category='ot')
     kidsseating=Product.objects.filter(category='kst')
     kidsstudy=Product.objects.filter(category='ks')
     if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
     return render(request, 'app/home.html',{'chair':chair,'table':table,'officechair':officechair,'totalitem':totalitem,'officetable':officetable,'kidsseating':kidsseating,'kidsstudy':kidsstudy})


class ProductDetailView(View):
    def get(self,request,pk):
       totalitem=0
       product= Product.objects.get(pk=pk)
       item_already_in_cart =False
       if request.user.is_authenticated:
        item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
        if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
       return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):
 totalitem=0
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 if request.user.is_authenticated:
  totalitem= len(Cart.objects.filter(user=request.user))
 return redirect('/cart',{'totalitem':totalitem})


def show_cart(request):
 if request.user.is_authenticated:
     totalitem=0
     user=request.user
     cart=Cart.objects.filter(user=user)
     #print(cart)
     amount=0.0
     shipping_amount=70.0
     totalamount=0.0
     cart_product=[p for p in Cart.objects.all() if p.user==user]
     #print(cart_product)
     if request.user.is_authenticated:
      totalitem= len(Cart.objects.filter(user=request.user))
     if cart_product:
         for p in cart_product:
             tempamount=(p.quantity * p.product.discounted_price)
             amount+=tempamount
             totalamount=amount+shipping_amount
         return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'shipping_amount':shipping_amount,'totalitem':totalitem})
     else:
         return render(request,'app/emptycart.html')    

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 totalitem=0
 add =Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
  totalitem= len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html',{'add':add,'active':'btn-warning','totalitem':totalitem})

def orders(request):
 totalitem=0
 op=OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})

def chair(request, data=None):
    totalitem=0
    if data == None:
        chair = Product.objects.filter(category='ch')
    elif data=='below':
        chair=Product.objects.filter(category='ch').filter(discounted_price__lt=500)
    elif data=='above':
        chair=Product.objects.filter(category='ch').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/chair.html',{'chair':chair,'totalitem':totalitem})

def table(request, data=None):
    totalitem=0
    if data == None:
        table = Product.objects.filter(category='tb')
    elif data=='below':
        table=Product.objects.filter(category='tb').filter(discounted_price__lt=1000)
    elif data=='above':
        table=Product.objects.filter(category='tb').filter(discounted_price__gt=1000)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/table.html',{'table':table,'totalitem':totalitem})

def sofa(request, data=None):
    totalitem=0
    if data == None:
        sofa = Product.objects.filter(category='sf')
    elif data=='below':
        sofa=Product.objects.filter(category='sf').filter(discounted_price__lt=1000)
    elif data=='above':
        sofa=Product.objects.filter(category='sf').filter(discounted_price__gt=1000)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/sofa.html',{'sofa':sofa,'totalitem':totalitem})

def officechair(request, data=None):
    totalitem=0
    if data == None:
        officechair = Product.objects.filter(category='oc')
    elif data=='below':
        officechair=Product.objects.filter(category='oc').filter(discounted_price__lt=500)
    elif data=='above':
        officechair=Product.objects.filter(category='oc').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/officechair.html',{'officechair':officechair,'totalitem':totalitem})

def officetable(request, data=None):
    totalitem=0
    if data == None:
        officetable = Product.objects.filter(category='ot')
    elif data=='below':
        officetable=Product.objects.filter(category='ot').filter(discounted_price__lt=2500)
    elif data=='above':
        officetable=Product.objects.filter(category='ot').filter(discounted_price__gt=2500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/officetable.html',{'officetable':officetable,'totalitem':totalitem})

def officesofa(request, data=None):
    totalitem=0
    if data == None:
        officesofa = Product.objects.filter(category='os')
    elif data=='below':
        officesofa=Product.objects.filter(category='os').filter(discounted_price__lt=500)
    elif data=='above':
        officesofa=Product.objects.filter(category='os').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/officesofa.html',{'officesofa':officesofa,'totalitem':totalitem})

def kidsbed(request, data=None):
    print('---------------------------')
    totalitem=0
    if data == None:
        kidsbed = Product.objects.filter(category='kb')
    elif data=='below':
        kidsbed=Product.objects.filter(category='kb').filter(discounted_price__lt=500)
    elif data=='above':
        kidsbed=Product.objects.filter(category='kb').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/kidsbed.html',{'kidsbed':kidsbed,'totalitem':totalitem})

def kidsseating(request, data=None):
    totalitem=0
    if data == None:
        kidsseating = Product.objects.filter(category='kst')
    elif data=='below':
        kidsseating=Product.objects.filter(category='kst').filter(discounted_price__lt=500)
    elif data=='above':
        kidsseating=Product.objects.filter(category='kst').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/kidsseating.html',{'kidsseating':kidsseating,'totalitem':totalitem})

def other_furniture(request, data=None):
    totalitem=0
    if data == None:
        other_furniture = Product.objects.filter(category='otf')
    elif data=='below':
        other_furniture=Product.objects.filter(category='otf').filter(discounted_price__lt=500)
    elif data=='above':
        other_furniture=Product.objects.filter(category='otf').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/other_furniture.html',{'other_furniture':other_furniture,'totalitem':totalitem})

def kidsstudy(request, data=None):
    totalitem=0
    if data == None:
        kidsstudy = Product.objects.filter(category='ks')
    elif data=='below':
        kidsstudy=Product.objects.filter(category='ks').filter(discounted_price__lt=500)
    elif data=='above':
        kidsstudy=Product.objects.filter(category='ks').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, 'app/kidsstudy.html',{'kidsstudy':kidsstudy,'totalitem':totalitem})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations!! You are registered Successfully.')
        return render(request,'app/customerregistration.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class Feedbacks(View):
    def get(self, request):
        form = feedbackForm()
        return render(request, 'app/feedback.html', {'form': form, 'active': 'btn-primary'})
    def post(self, request):
        form = feedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            city = form.cleaned_data['city']
            pincode = form.cleaned_data['pincode']
            state = form.cleaned_data['state']
            description = form.cleaned_data['description']
            reg = Feedback(name=name, mobile=mobile,city=city,pincode=pincode, state = state, description=description)
            reg.save()
            messages.success(request, 'Congratulations!! Feedback Submit Successfully.')
        return render(request, 'app/feedback.html', {'form': form, 'active': 'btn-primary'})
@login_required
def checkout(request):
 totalitem=0
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items= Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 totalamount=0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
 totalamount=amount+shipping_amount
 if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

def payment_done(request):
 
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 
 return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    totalitem=0
    def get(self,request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-warning','totalitem':totalitem})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name,mobile=mobile, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form,'active':'btn-warning','totalitem':totalitem})


def plus_cart(request):
    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount' : amount + shipping_amount
            }
        
        return JsonResponse(data)

def minus_cart(request):
    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount' : amount + shipping_amount
            }
        
        return JsonResponse(data)

def remove_cart(request):
    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount 

        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        
        return JsonResponse(data)

