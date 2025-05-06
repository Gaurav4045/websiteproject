from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import razorpay
from .models import Product,Profilee,cart,OrderPlaced,Payment,Wishlist
from django.db.models import Count,Q
from .form import CustomerRegistrationform,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Home view
@login_required
def home(request):
    return render(request, "apps/home.html")

def about(request):
    return render(request, "apps/about.html")

def contact(request):
    return render(request, "apps/contact.html")


# Category view
class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val)
        titles = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request, "apps/category.html", {'products': products, 'titles': titles})

# Category Title view
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        if product.exists():
            product = product.first()  # Get the first matching product
            return render(request, "apps/productetail.html", {'product': product})
        else:
            return render(request, "apps/category.html", {'error': "Product not found"})
# Product Detail view


class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user)).exists()
        return render(request, "apps/productetail.html", {'product': product, 'wishlist': wishlist})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationform()
        return render(request,'apps/CustomerRegistration.html' ,locals())
    def post(self,request):
        form=CustomerRegistrationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"congarulations user register sucesfull")
        else:
            messages.warning(request,"invalid input")
        return render(request,'apps/CustomerRegistration.html' ,locals())

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'apps/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Profilee(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.warning(request, "Invalid input. Please correct the errors below.")
        return render(request, 'apps/profile.html', locals())

def address(request):
    add=Profilee.objects.filter(user=request.user)
    return render(request, 'apps/address.html', locals())

class updateAdress(View):
    def get(self,request,pk):
        add=Profilee.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request, 'apps/updateaddress.html', locals())

    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Profilee.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"congratulations profile updated successfully")
        else:
            messages.warning(request,"invalid input")

        return redirect("adress")
    
#shopping

# Add to Cart
def add_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('showcart')


# Show Cart
def showcart(request):
    user = request.user
    cart_items = cart.objects.filter(user=user)

    if cart_items.exists():
        amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
        total_amount = amount + 40  # Flat shipping fee
    else:
        amount = 0
        total_amount = 0

    return render(request, 'apps/addtocart.html', {
        'cart': cart_items,
        'amount': amount,
        'totalamount': total_amount,
    })

from django.shortcuts import render
from .models import Wishlist

def show_wishlist(request):
    if request.user.is_authenticated:
        # Retrieve the wishlist items for the logged-in user
        wishlist_items = Wishlist.objects.filter(user=request.user)
        
        # Pass the wishlist items to the template
        return render(request, 'apps/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        # If the user is not logged in, you can either redirect or show a message
        return render(request, 'apps/wishlist.html', {'message': 'Please log in to view your wishlist.'})

class Checkout(View):
    def get(self, request):
        user = request.user
        add = Profilee.objects.filter(user=user)
        cart_items = cart.objects.filter(user=user)

        if cart_items.exists():
            amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
            total_amount = amount + 40  # Flat shipping fee
            razoramount = int(total_amount * 100)

            # Razorpay client initialization
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            data = {
                "amount": razoramount,
                "currency": "INR",
                "receipt": "order_rcptid_11"
            }
            payment_response = client.order.create(data=data)  # Corrected method name
            order_id = payment_response['id']  # Razorpay order ID
            print(payment_response)
        else:
            amount = 0
            total_amount = 0
            order_id = None

        return render(request, 'apps/checkout.html', {
            'add': add,
            'cart_items': cart_items,
            'amount': amount,
            'totalamount': total_amount,
            'razoramount': razoramount if cart_items.exists() else 0,
            'order_id': order_id,
        })


class PaymentDone(View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        cust_id = request.GET.get('cust_id')

        if not payment_id:
            return HttpResponse("Payment ID is missing in the request.", status=400)

        try:
            payment = Payment.objects.get(razorpay_payment_id=payment_id)
        except Payment.DoesNotExist:
            return HttpResponse(f"Payment with ID {payment_id} does not exist.", status=404)

        payment.razorpay_order_id = order_id
        payment.paid = True
        payment.save()

        customer = Profilee.objects.get(id=cust_id)
        cart_items = cart.objects.filter(user=request.user)
        for item in cart_items:
            OrderPlaced.objects.create(
                user=request.user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                payment=payment,
            )
            item.delete()

        return redirect("orders")

                   

class OrderView(View):
    def get(self, request):
        user = request.user
        orders = OrderPlaced.objects.filter(user=user)

        return render(request, 'apps/order.html', locals())

            



# Increase Quantity
def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        try:
            cart_item = cart.objects.get(product_id=prod_id, user=user)
            cart_item.quantity += 1
            cart_item.save()

            all_cart_items = cart.objects.filter(user=user)
            amount = sum(item.product.discounted_price * item.quantity for item in all_cart_items)
            total_amount = amount + 40

            return JsonResponse({
                'status': 'success',
                'quantity': cart_item.quantity,
                'amount': amount,
                'total_amount': total_amount,
                
            })

        except cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart item not found'}, status=404)


# Decrease Quantity
def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        try:
            cart_item = cart.objects.get(product_id=prod_id, user=user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

            all_cart_items = cart.objects.filter(user=user)
            amount = sum(item.product.discounted_price * item.quantity for item in all_cart_items)
            total_amount = amount + 40

            return JsonResponse({
                'status': 'success',
                'quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
                'amount': amount,
                'total_amount': total_amount,
            })

        except cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart item not found'}, status=404)


# Remove Cart Item
#from django.http import JsonResponse

def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        print(f"Received prod_id: {prod_id}")  # Debugging
        user = request.user
        try:
            cart_item = cart.objects.get(product_id=prod_id, user=user)
            print(f"Found cart item: {cart_item}")  # Debugging
            cart_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
        except cart.DoesNotExist:
            print("Cart item does not exist")  # Debugging
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    print("Invalid request method")  # Debugging
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Wishlist

# Add product to wishlist
def plus_wishlist(request):
    if request.method == 'GET' and request.user.is_authenticated:
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        user = request.user

        # Check if the product is already in the wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

        if created:
            data = {'status': 'success', 'message': 'Product added to wishlist'}
        else:
            data = {'status': 'exists', 'message': 'Product already in wishlist'}
        return JsonResponse(data)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# Remove product from wishlist
def minus_wishlist(request):
    if request.method == 'GET' and request.user.is_authenticated:
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        user = request.user

        # Remove the product from the wishlist
        wishlist_item = Wishlist.objects.filter(user=user, product=product)
        if wishlist_item.exists():
            wishlist_item.delete()
            data = {'status': 'success', 'message': 'Product removed from wishlist'}
        else:
            data = {'status': 'error', 'message': 'Product not in wishlist'}
        return JsonResponse(data)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




def search(request):
    query = request.GET.get('search', '').strip()  # Get search term, default to an empty string
    product = []
    
    if query:  # Only search if query is not empty
        product = Product.objects.filter(Q(title__icontains=query))  # Case-insensitive search
    
    return render(request, "apps/search.html", {
        'product': product,
        'query': query,  # Pass query back to template for display
    })