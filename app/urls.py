from django.urls import path
from app import views

urlpatterns=[
path('',views.index),
path('about/',views.about),
path('contact/',views.contact),
path('services/',views.services),
path('userreg/',views.userreg),
path('product/',views.product),
path('login/',views.login),
path('logout/',views.logout),
path('image/',views.image),
path('viewproduct/',views.viewproduct),
path('edit/',views.edit),
path('update/',views.update),


path('delete/',views.delete),
path('addtocart/',views.addtocart),
path('deletecart/',views.deletecart),


############ payment ##########
path('buynow/',views.buynow),
path('makepayment/',views.makepayment),
path('cart/',views.cart),

path('clearmycart/',views.clearmycart),











]