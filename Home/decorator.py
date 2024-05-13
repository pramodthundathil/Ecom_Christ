from django.shortcuts import redirect 

def admin_only(view_fun):
    def wrapper_fun(request,*args,**kwargs):
        group = None 
        if request.user.groups.all().exists():
            group = request.user.groups.all()[0].name
        if group == "admin":
            return redirect("AdminIndex")
        if group == "merchant":
            return redirect("MerchantIndex")
        else:
            return view_fun(request,*args, **kwargs)
    return wrapper_fun

