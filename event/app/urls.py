from django.urls import path
from . import views
import os  # Import os to use for path construction

urlpatterns = [
    #vendor
    path("", views.HomeView, name="home"),
    path("vendor_registration/",views.Vendor_Registration_View,name="vendor_registration"),
    path("vendor_login/",views.Login_View,name="vendor_login"),
    path("logout_vendor/",views.Logout_View,name="logout_vendor"),
    path("vendor_home/",views.Vendor_Home_View,name="vendor_home"),
    path('add_item/', views.Product_View, name='add_item'),
    path("your_item/",views.Your_List_View,name="your_item"),
    #user
    path("user_registration/",views.User_Registration_View,name="user_registration"),
    path("user_login/",views.User_Login_View,name="user_login"),
    path("logout_user/",views.User_Logout_View,name="logout_user"),
    path("user_home/",views.User_Home_View,name="user_home"),
    path("vendor_list/",views.Vendor_List_view,name="vendor_list"),
    path('vendors/<str:vendor_name>/products/', views.Vendor_Product_View, name='vendor_products'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order_view, name='place_order'),  # URL for placing the order
    path('order/<int:order_id>/', views.order_status_view, name='order_status'),
    
    #admin
    path('admin_view/', views.Admin_View, name='admin_view'),  
    path("signup/", views.Admin_Signup, name="signup"),  # Signup view
    path("login/", views.Admin_Login, name="login"),  # Login view (no leading slash)
    path("logout/", views.logout_view, name="logout"),
    path('users/', views.User_list, name='user_list'),
    path('vendors/', views.Vendor_list, name='vendor_list'),
    path('vendor/update/<int:vendor_id>/', views.update_vendor, name='update_vendor'),
    path('user/update/<int:user_id>/', views.update_user, name='update_user'),
    path('vendor/delete/<int:id>/', views.vendor_delete_view, name='delete_vendor'),
    path('user/delete/<int:id>/', views.user_delete_view, name='delete_user'),
]

