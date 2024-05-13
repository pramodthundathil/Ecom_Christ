from .models import Products
from django.forms import ModelForm, TextInput, Select


class ProductAddForm(ModelForm):
    class Meta:
        model = Products
        fields = ["Product_Name","Product_Price","Product_Category","Product_Category_sub","Product_Discription","Product_Stock","Stock_trush","Product_Image"]

        widgets = {
            "Product_Name":TextInput(attrs={"class":"form-control", "placeholder":"Product Name"}),
            "Product_Price":TextInput(attrs={"class":"form-control", "placeholder":"Product Price", "type":"number"}),
            "Product_Discription":TextInput(attrs={"class":"form-control", "placeholder":"Product Description"}),
            "Product_Stock":TextInput(attrs={"class":"form-control", "placeholder":"Product Stock","type":"number"}),
            "Stock_trush":TextInput(attrs={"class":"form-control", "placeholder":"Product Stock Trusholds","type":"number"}),
            "Product_Category":Select(attrs={"class":"form-control"}),
            "Product_Category_sub":Select(attrs={"class":"form-control"}),
        }