# from django.db import models
# from django.urls import reverse
# from django.core.validators import RegexValidator
# from farmer.models import Crop, Farmer

# # Create your models here.



# class Warehouse(models.Model):
#     name = models.CharField(max_length=100)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     storage_capacity = models.PositiveIntegerField()

# class Manager(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     phone_number = models.CharField(
#         max_length=10,
#         # validators = [
#         #     RegexValidator(
#         #         regex='^\d{10,11}$',
#         #         message='Phone number must be valid',
#         #         code='invalid_phone_number'
#         #     ),
#         # ]
#     )
#     warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=254)
#     password = models.CharField(max_length=12, null=True)

#     def __str__(self):
#         return f'{self.email} {self.phone_number}'

# class Crop_stored(models.Model):
#     storage_date = models.DateField()
#     crop_id = models.ForeignKey(Crop, on_delete=models.CASCADE)
#     farmer_id = models.ForeignKey(Farmer, on_delete=models.CASCADE)
#     warehouse_id= models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

# class Reservation(models.Model):
#     crop_id = models.ForeignKey(Crop, on_delete=models.CASCADE)
#     farmer_id = models.ForeignKey(Farmer, on_delete=models.CASCADE)
#     warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     reservation_date = models.DateField()

