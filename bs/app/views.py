from http import client
from itertools import product
from multiprocessing import Value
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
import razorpay
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist 
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.utils.decorators import method_decorator


# Create your views here.
@login_required
def home(request):
    totalitem =0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = Wishlist.objects.filter(user=request.user).count()     
    return render(request, "app/home.html",locals())

@login_required
def about(request):  
    totalitem =0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
        wishitem = Wishlist.objects.filter(user=request.user).count() 
    return render(request, "app/about.html",locals())

@login_required
def contact(request):  
    totalitem =0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
        wishitem = Wishlist.objects.filter(user=request.user).count() 
    return render(request, "app/contact.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val=None):
        totalitem =0
        wishitem =0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) 
            wishitem = Wishlist.objects.filter(user=request.user).count()   
        category = val if val else "All Categories"  
        books = Product.objects.filter(category=val)  
        title = Product.objects.filter(category=val).values('title').distinct() 
        return render(request, "app/category.html", locals())

@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request, val=None):  
        if val:
            books = Product.objects.filter(title=val)  
            category = books.first().category if books.exists() else "Unknown Category"
            title = Product.objects.filter(category=category).values('title') if books.exists() else []
        else:
            books = []
            category = "All Categories"
            title = Product.objects.all().values('title')
            totalitem =0
            wishitem =0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user)) 
                wishitem = Wishlist.objects.filter(user=request.user).count() 
        return render(request, "app/category.html",locals())

@method_decorator(login_required, name='dispatch')
class BooksDetail(View):
    def get(self, request, bd):
        books = Product.objects.get(id=bd)
        # Wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))

        totalitem =0
        wishitem =0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) 
            wishitem = Wishlist.objects.filter(user=request.user).count() 
        return render(request, "app/Booksdetail.html", locals())



class CustomerRegistrationView(View):  
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()

        return render(request, 'app/customerregistration.html', {
            'form': form,
            'totalitem': totalitem,
            'wishitem': wishitem
        })

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'app/customerregistration.html', {'form': form})



# @method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem =0
        wishitem =0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) 
            wishitem = Wishlist.objects.filter(user=request.user).count() 
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            reg = Customer(
                user=user,
                name=form.cleaned_data['name'],
                locality=form.cleaned_data['locality'],
                mobile=form.cleaned_data['mobile'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode']
            )
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'app/profile.html', locals())

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem =0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
        wishitem = Wishlist.objects.filter(user=request.user).count() 
    return render(request, 'app/address.html',locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, bd):
        add = Customer.objects.get(id=bd)
        form = CustomerProfileForm(instance=add)
        totalitem =0
        wishitem =0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) 
            wishitem = Wishlist.objects.filter(user=request.user).count() 
        return render(request, 'app/updateAddress.html',locals())
    def post(self, request, bd):
        add = Customer.objects.get(id=bd) 
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            add = Customer.objects.get(id=bd)    
            add.name = form.cleaned_data['name'],
            add.locality=form.cleaned_data['locality'],
            add.mobile=form.cleaned_data['mobile'],
            add.city=form.cleaned_data['city'],
            add.state=form.cleaned_data['state'],
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! password Changed Successfully")
            return redirect("address")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/updateAddress.html', locals()) 
    
# def add_to_cart(request):
#     user=request.user
#     product_id=request.GET.get('prod_id')
#     product =Product.objects.get(id=product_id)
#     Cart(user=user,product=product).save()
#     return redirect("/cart")

# def show_cart(request):
#     user =request.user
#     cart =Cart.objects.filter(user=user)
#     amount=0
#     for p in cart:
#         value = p.quantity * p.product.discounted_price
#         amount = amount + value
#     totalamount = amount + 40
#     return render(request, 'app/addtocart.html',locals())


@login_required
def add_to_cart(request):
    """ Adds a product to the cart or increases quantity if already present """
    user = request.user
    product_id = request.POST.get('prod_id')

    if not product_id or not product_id.isdigit():
        messages.error(request, "Invalid product ID!")
        return redirect("showcart")

    product = get_object_or_404(Product, id=int(product_id))
    
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Item added to cart!")
    return redirect("showcart")




@login_required
def show_cart(request):
    """ Displays the cart and calculates the total amount """
    user = request.user
    cart = Cart.objects.filter(user=user)

    if not cart.exists():  
        return render(request, 'app/addtocart.html', {'cart': None})  

    amount = sum(p.quantity * p.product.discounted_price for p in cart)  
    totalamount = amount + 48  # Shipping charge
    totalitem =0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
        wishitem = Wishlist.objects.filter(user=request.user).count() 
    return render(request, 'app/addtocart.html', locals())  


@method_decorator(login_required, name='dispatch')
class Checkout(View): 
    def get(self, request): 
        totalitem =0
        wishitem =0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = Wishlist.objects.filter(user=request.user).count()  
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount =0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount +value
        totalamount =famount + 40
        # razoramount =int(totalamount * 100)
        # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        # data ={ "amount":razoramount, "currency":"INR","receipt":"order_rcptid_{user.id}"}
        # payment_response =client.order.create(data=data)
        # print(payment_response)
        # order_id = payment_response.get['id']  # noqa: F821
        # order_status =payment_response['status']
        # if order_status == 'created':
        #     payment =Payment(
        #         user=user,
        #         amount=totalamount,
        #         razorpay_order_id=order_id,
        #         racorpay_payment_status=order_status
        #     )
        #     payment.save()
        return render(request, 'app/checkout.html',locals())
    

        # def payment_done(request): 
    #     order_id = request.GET.get("order_id") 
    #     payment_id = request.GET.get("payment_id") 
    #     cust_id = request.GET.get("cust_id")  

    #     print(f"Payment Done - Order ID: {order_id}, Payment ID: {payment_id}, Customer ID: {cust_id}")

    #     user = request.user  # Fix: Assign the user properly

    # # Fetch customer
    #     try:
    #         customer = Customer.objects.get(id=cust_id)
    #     except Customer.DoesNotExist:
    #         print("Error: Customer not found")
    #         return redirect("cart")  # Redirect to cart if customer not found

    # # Update payment status
    #     try:
    #        payment = Payment.objects.get(razorpay_order_id=order_id)
    #        payment.paid = True  # Fix: Used '=' instead of '-'
    #        payment.razorpay_payment_id = payment_id  
    #        payment.save()
    #     except Payment.DoesNotExist:
    #        print("Error: Payment record not found")
    #     return redirect("cart")  # Redirect to cart if payment is not found

    # # Save order details
    #     cart_items = Cart.objects.filter(user=user)  
    #     for c in cart_items:  
    #         OrderPlaced.objects.create(
    #         user=user,
    #         customer=customer,
    #         product=c.product,
    #         quantity=c.quantity,
    #         payment=payment
    #     )  
    #     c.delete()  # Remove item from cart after placing the order

    #     return redirect("orders")  # Redirect user to the orders page
        




        # # Initialize Razorpay client
        # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        # data = { "amount": razoramount,  "currency": "INR", "receipt": "order_reptid_12"}  
        # payment_response = client.order.create(data=data)  
        # print(payment_response)  

        # return render(request, "app/checkout.html",locals())

        


# def payment_done(request):
#     order_id = request.GET.get('order_id')
#     payment_id = request.GET.get('payment_id')
#     cust_id = request.GET.get('cust_id')

#     user = request.user  # ✅ Correct assignment

#     try:
#         # ✅ Fetch customer
#         customer = Customer.objects.get(id=cust_id)

#         # ✅ Update payment status
#         payment = Payment.objects.get(razorpay_order_id=order_id)
#         payment.paid = True
#         payment.razorpay_payment_id = payment_id  # ✅ Correct assignment
#         payment.save()

#         # ✅ Move cart items to OrderPlaced
#         cart_items = Cart.objects.filter(user=user)
#         for c in cart_items:
#             OrderPlaced.objects.create(
#                 user=user, 
#                 customer=customer, 
#                 product=c.product, 
#                 quantity=c.quantity, 
#                 payment=payment
#             )
#             c.delete()  # ✅ Remove cart item after order is placed

#         return redirect("orders")  # ✅ Redirect to orders page

#     except (Customer.DoesNotExist, Payment.DoesNotExist) as e:
#         return redirect("checkout")  # ✅ Handle potential errors

@login_required
def orders(request):
    totalitem =0
    wishitem =0
    if request.user.is_authenticated:
       totalitem = len(Cart.objects.filter(user=request.user)) 
       wishitem = Wishlist.objects.filter(user=request.user).count() 
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())


# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id=request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity+=1
#         c.save()
#         user =request.user
#         cart =Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value =p.quantity * p.product.discounted_price
#             amount=amount+value
#         totalamount =amount +40
#         data={
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)


# def minus_cart(request):
#     if request.method == 'GET':
#         prod_id=request.GET.get['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity-=1
#         c.save()
#         user =request.user
#         cart =Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value =p.quantity * p.product.discounted_price
#             amount=amount+value
#         totalamount =amount +40
#         data={
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)


# def remove_cart(request):
#     if request.method == 'GET':
#         prod_id=request.GET.get['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity+=1
#         c.delete()
#         user =request.user
#         cart =Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value =p.quantity * p.product.discounted_price
#             amount=amount+value
#         totalamount =amount + 40
#         data={
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, user=request.user, product_id=prod_id)
        cart_item.quantity += 1
        cart_item.save()

        amount = sum(item.quantity * item.product.discounted_price for item in Cart.objects.filter(user=request.user))
        totalamount = amount + 48  # Shipping cost

        return JsonResponse({'quantity': cart_item.quantity, 'amount': amount, 'totalamount': totalamount})


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, user=request.user, product_id=prod_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity reaches 0

        amount = sum(item.quantity * item.product.discounted_price for item in Cart.objects.filter(user=request.user))
        totalamount = amount + 48  # Shipping cost

        return JsonResponse({'quantity': cart_item.quantity if cart_item.quantity else 0, 'amount': amount, 'totalamount': totalamount})

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, user=request.user, product_id=prod_id)
        cart_item.delete()  # Delete item from cart

        amount = sum(item.quantity * item.product.discounted_price for item in Cart.objects.filter(user=request.user))
        totalamount = amount + 48  # Shipping cost

        return JsonResponse({'amount': amount, 'totalamount': totalamount})




def plus_Wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user

        # Fix: Use product instead of products
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)



def minus_Wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user

        # Fix: Use product instead of products
        wishlist_item = Wishlist.objects.filter(user=user, product=product)

        if wishlist_item.exists():
            wishlist_item.delete()
            data = {
                'message': 'Wishlist Removed Successfully',
            }
            return JsonResponse(data)

        data = {
            'message': 'Item Not Found in Wishlist',
        }
        return JsonResponse(data, status=404)


@login_required
def search(request):
    query = request.GET['search']
    totalitem =0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = Wishlist.objects.filter(user=request.user).count()  
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())


def show_wishlist(request):
    return render(request, 'app/wishlist.html')


