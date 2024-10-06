from django.shortcuts import render,redirect
from .forms import VendorForm,LoginForm,ProductForm,UserForm,VendorUpdateForm,UserUpdateForm
from .models import Vendor_Registration,Product,User_Registration,Cart,Order,OrderItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
def HomeView(request):
    return render(request,"home.html")


def Vendor_Registration_View(request):
    if request.method=="POST":
        form=VendorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration successfull")
            return redirect("vendor_login")
        else:
            messages.error(request,"please correct the error below")
    else:
        form=VendorForm()
    return render(request,"vendor_registration.html",{'form':form})


def Login_View(request):
    form = LoginForm(request.POST or None)  

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = Vendor_Registration.objects.get(username=username)
            if user.password == password: 
                request.session['vendor_id'] = user.id
                return redirect('vendor_home')  
            else:
                messages.error(request, "Invalid credentials.")
        except Vendor_Registration.DoesNotExist:
            messages.error(request, "Vendor does not exist. Please register.")
    return render(request, 'vendor_login.html', {'form': form})


def Logout_View(request):
    if 'vendor_id' in request.session:
        del request.session['vendor_id']  
        messages.success(request, "You have successfully logged out.")
    else:
        messages.info(request, "You are not logged in.")

    return redirect('home')


def Vendor_Home_View(request):
    vendor_id = request.session.get('vendor_id')  # Get vendor ID from session
    
    if vendor_id:
        vendor = Vendor_Registration.objects.get(id=vendor_id)
        print(vendor_id)
        return render(request, "vendor_home.html", {'vendor': vendor})


def Product_View(request):
    vendor_id = request.session.get('vendor_id')
    
    if vendor_id:
        vendor = get_object_or_404(Vendor_Registration, id=vendor_id)
        
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES)  
            if form.is_valid():
                product = form.save(commit=False) 
                product.vendor = vendor
                product.save() 
                return redirect("your_item") 
        else:
            form = ProductForm()

        return render(request, "add_items.html", {'form': form, 'vendor': vendor})



def Your_List_View(request):
    vendor_id = request.session.get('vendor_id')  # Get vendor ID from session
    if vendor_id: 
        vendor = get_object_or_404(Vendor_Registration, id=vendor_id)  
        products = vendor.products.all()  
      
    else:
        products = []  
    return render(request, "your_items.html", {'products': products}) 
            
    
    
    
    #user:
def User_Registration_View(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration successfull")
            return redirect("user_login")
        else:
            messages.error(request,"please correct the error below")
    else:
        form=UserForm()
    return render(request,"user_registration.html",{'form':form})


def User_Login_View(request):
    form = LoginForm(request.POST or None)  

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = User_Registration.objects.get(username=username)
            if user.password == password: 
                request.session['user_id'] = user.id
                return redirect('user_home')  
            else:
                messages.error(request, "Invalid credentials.")
        except Vendor_Registration.DoesNotExist:
            messages.error(request, "user does not exist. Please register.")
    return render(request, 'user_login.html', {'form': form})


def User_Logout_View(request):
    if 'user_id' in request.session:
        del request.session['user_id']  
        messages.success(request, "You have successfully logged out.")
    else:
        messages.info(request, "You are not logged in.")

    return redirect('home')


def User_Home_View(request):
    user_id = request.session.get('user_id')  # Get vendor ID from session
    
    if user_id:
        user = User_Registration.objects.get(id=user_id)
        print(user_id)
        return render(request, "user_home.html", {'user': user})
    
def Vendor_List_view(request):
    mydata = Vendor_Registration.objects.all()
    context = {'vendors': mydata}
    return render(request,"vendor.html",context)

def Vendor_Product_View(request, vendor_name):
    vendor = get_object_or_404(Vendor_Registration, username=vendor_name)
    products = Product.objects.filter(vendor=vendor)
    context = {'vendor': vendor, 'products': products}
    return render(request, "vendor_products.html", context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.session.get('user_id')  # Assuming you store the user's ID in the session

    if user:
        user_instance = get_object_or_404(User_Registration, id=user)  # Get user instance

        # Create or update the cart item
        cart_item, created = Cart.objects.get_or_create(user=user_instance, product=product)
        if not created:
            cart_item.quantity += 1  # Increment quantity if item already in cart
            cart_item.save()

    return redirect('cart_view')  # Redirect to the cart view or wherever you want

# View to display cart items
def cart_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(User_Registration, id=user_id)
        cart_items = Cart.objects.filter(user=user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)  # Calculate total price
        context = {'cart_items': cart_items, 'total_price': total_price}
        return render(request, "cart.html", context)
    else:
        return redirect('login')  # Redirect to login if user is not authenticated

# View to remove an item from the cart
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_view')  # Redirect to the cart view


def place_order_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(User_Registration, id=user_id)
        cart_items = Cart.objects.filter(user=user)

        if cart_items.exists():
            # Create a new order object
            order = Order.objects.create(user=user, status='Pending')
            
            # Transfer items from the cart to the order (assuming an OrderItem model)
            for item in cart_items:
                
                order.items.create(product=item.product, quantity=item.quantity, price=item.product.price)
                
            
            
            
            return redirect('order_status', order_id=order.id)

    return redirect('cart')  # If no items or user not found, redirect back to the cart

def order_status_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_order_price = sum(item.quantity * item.price for item in order.items.all())
    
    context = {'order': order, 'total_order_price': total_order_price}
    return render(request, 'order.html', context)
@login_required
def Admin_View(request):
    return render(request,"admin_home.html")

def Admin_Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin account created successfully. You can now log in.')
            return redirect('login') 
    else:
        form = UserCreationForm() 
    return render(request, 'admin_registration.html', {'form': form})
  

def Admin_Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            next_url = request.GET.get('next')  
            if next_url:  
                return redirect(next_url)
            return redirect('admin_view')  
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('login')
@login_required
def User_list(request):
    
    users = User_Registration.objects.all()  
    return render(request, "user_list.html", {'users': users})
@login_required
def Vendor_list(request):
    
    vendors = Vendor_Registration.objects.all()  
    return render(request, "vendor_list.html", {'vendors': vendors})
@login_required
def update_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor_Registration, id=vendor_id)
    
    if request.method == 'POST':
        form = VendorUpdateForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor details updated successfully.')
            return redirect('vendor_list')  
    else:
        form = VendorUpdateForm(instance=vendor)  

    return render(request, 'update_vendor.html', {'form': form, 'vendor': vendor})
@login_required
def update_user(request, user_id):
    user = get_object_or_404(User_Registration, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'user details updated successfully.')
            return redirect('user_list')  
    else:
        form = UserUpdateForm(instance=user)  

    return render(request, 'update_user.html', {'form': form, 'vendor': user})

def user_delete_view(request,id):
    user=get_object_or_404(User_Registration,id=id)
    user.delete()
    return redirect('user_list')
def vendor_delete_view(request,id):
    vendor=get_object_or_404(Vendor_Registration,id=id)
    vendor.delete()
    return redirect('vendor_list')
