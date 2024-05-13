from django.shortcuts import render, redirect, HttpResponse
from .forms import ProductAddForm
from django.contrib import messages
from .models import Products, Cart, Checkout
from django.contrib.auth.decorators import login_required
from Home.models import BillingAdress
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User

razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def Product_merchant(request):
    form = ProductAddForm()
    # product = Products.objects.all()
    product = Products.objects.filter(user = request.user)

    print(product,".......................................")
    if request.method == "POST":
        form = ProductAddForm(request.POST,request.FILES )
        if form.is_valid():
            product = form.save()
            product.user = request.user
            product.save()
            messages.info(request,"Product added To List")
            return redirect("Product_merchant")


    context = {
        "form":form,
        "product":product,
    }
    return render(request,"products_merchant.html",context)

def DeleteProduct(request,pk):

    product = Products.objects.get(id = pk)
    product.delete()
    messages.info(request,"Product Deleted")
    return redirect("Product_merchant")


def ProductSingleview(request,pk):
    product = Products.objects.get(id = pk)

    context = {
        "product":product
    }
    return render(request,"detail.html",context)


@login_required(login_url="SignIn")
def CartPage(request):
    cart_items = Cart.objects.filter(user = request.user)
    cart_items_count = Cart.objects.filter(user = request.user).count()
    total_cart_amount = 0

    for i in cart_items:

        total_cart_amount += i.total_price

    gst = (total_cart_amount * 18 )/100
    subtotal = total_cart_amount - gst
    


    context = {
        "cart_items":cart_items,
        "cart_items_count":cart_items_count,
        "total_cart_amount":total_cart_amount,
        "gst":gst,
        "subtotal":subtotal
    }
    return render(request,'cart.html',context)


@login_required(login_url="SignIn")
def AddToCart(request,pk):
    product = Products.objects.get(id = pk)
    if Cart.objects.filter(product = product,user = request.user).exists():
        cart = Cart.objects.get(product = product,user = request.user)
        cart.items += 1
        cart.save()
        cart.total_price = cart.items * product.Product_Price
        cart.save()
    else:
        cart = Cart.objects.create(product = product, items = 1, total_price = product.Product_Price,user = request.user  )
        cart.save()

    messages.info(request,"Item Added To Cart.....")
    return redirect("CartPage")

def CartDelete(request,pk):
    Cart.objects.get(id = pk).delete()
    messages.info(request,"Item Added To Cart.....")
    return redirect("CartPage")

def CartItemIncrease(request,pk):
    cart = Cart.objects.get(id = pk)
    cart.items += 1
    cart.save()
    cart.total_price = cart.items * cart.product.Product_Price
    cart.save()
    messages.info(request,"Item quantity increased in Cart.....")
    return redirect("CartPage")

def CartItemDecrease(request,pk):
    cart = Cart.objects.get(id = pk)
    cart.items -= 1
    cart.save()
    cart.total_price = cart.items * cart.product.Product_Price
    cart.save()
    if cart.items <= 0:
        cart.delete()
    messages.info(request,"Item quantity increased in Cart.....")
    return redirect("CartPage")


def CheckOut(request):
    cart_items = Cart.objects.filter(user = request.user)
    cart_items_count = Cart.objects.filter(user = request.user).count()
    total_cart_amount = 0

    for i in cart_items:

        total_cart_amount += i.total_price

    gst = (total_cart_amount * 18 )/100
    subtotal = total_cart_amount - gst

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        mob = request.POST['mnum']
        add = request.POST['add']
        city = request.POST['city']
        state = request.POST['state']
        pin = request.POST['pin']
        country = request.POST['country']

        for cart in cart_items:
            checkout = Checkout.objects.create(product = cart.product,items = cart.items,total_price = cart.total_price,user = request.user,delivery_status = "Item Orederd")
            checkout.save()
            cart.delete()

        address = BillingAdress.objects.create(firstname = fname, lastname = lname,mobile_number = mob,address = add,city = city,state = state,zipcode = pin,country = country, user = request.user )
        address.save()
        currency = 'INR'
        amount = float(total_cart_amount) * 100 # Rs. 200 
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                            currency=currency,
                            payment_capture='0'))
        
        razorpay_order_id = razorpay_order["id"]
        callback_url = 'paymenthandler'

        context = {
            "cart_items":cart_items,
            "cart_items_count":cart_items_count,
            "total_cart_amount":total_cart_amount,
            "gst":gst,
            "subtotal":subtotal
        }
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url 
        context['slotid'] = "1",

        return render(request, "makepayment.html",context)

   

    context = {
        "cart_items":cart_items,
        "cart_items_count":cart_items_count,
        "total_cart_amount":total_cart_amount,
        "gst":gst,
        "subtotal":subtotal
    }
   
    return render(request,'checkout.html',context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 800 * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Index')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Index')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'Index')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    

def CustomerCheckOut(request):
    checkout = Checkout.objects.filter(product__user = request.user)

    context = {
        "checkout":checkout
    }
    return render(request,"customercheckout.html",context)

def ViewCustomer(request,pk):
    user = User.objects.get(id = pk)
    add = BillingAdress.objects.get(user = user)

    context = {
        "add":add
    }

    return render(request,"viewcustomer.html",context)

