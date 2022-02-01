from django.db import models

# Create your models here.
class table_user(models.Model):
	firstname=models.CharField(max_length=50, default="")
	lastname=models.CharField(max_length=50, default="")
	email=models.CharField(max_length=100, default="")
	age=models.TextField(default="")
	address=models.TextField(default="")
	password=models.CharField(max_length=100, default="")

class table_product(models.Model):
	name=models.CharField(max_length=50, default="")
	category=models.CharField(max_length=50, default="")
	price=models.CharField(max_length=100, default="")
	quantity=models.CharField(max_length=100, default="")
	details=models.TextField(default="")
	fileupload=models.FileField(upload_to="product")


class table_cart(models.Model):
	user_id=models.ForeignKey(table_user, on_delete=models.CASCADE)
	product_id=models.ForeignKey(table_product, on_delete=models.CASCADE)
	price=models.CharField(max_length=100, default="")
	quantity=models.CharField(max_length=100, default="")
	total=models.CharField(max_length=100,default="")
	status=models.CharField(max_length=100,default="pending")
	date=models.CharField(max_length=100,default="")

class table_payment(models.Model):
	user_id=models.ForeignKey(table_user, on_delete=models.CASCADE)
	amount=models.CharField(max_length=100, default="")
	status=models.CharField(max_length=100,default="pending")
	date=models.CharField(max_length=100,default="")

