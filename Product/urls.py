from django.urls import path 
from .import views

urlpatterns = [
    path("Product_merchant",views.Product_merchant,name="Product_merchant"),
    path("DeleteProduct/<int:pk>",views.DeleteProduct,name="DeleteProduct"),
    path("ProductSingleview/<int:pk>",views.ProductSingleview,name="ProductSingleview"),
    path("CartPage",views.CartPage,name="CartPage"),
    path("AddToCart/<int:pk>",views.AddToCart,name="AddToCart"),
    path("CartDelete/<int:pk>",views.CartDelete,name="CartDelete"),
    path("CartItemIncrease/<int:pk>",views.CartItemIncrease,name="CartItemIncrease"),
    path("CartItemDecrease/<int:pk>",views.CartItemDecrease,name="CartItemDecrease"),
    path("CheckOut",views.CheckOut,name="CheckOut"),
    path("paymenthandler",views.paymenthandler,name="paymenthandler"),
    path("CustomerCheckOut",views.CustomerCheckOut,name="CustomerCheckOut"),
    path("ViewCustomer/<int:pk>",views.ViewCustomer,name="ViewCustomer"),



    
]