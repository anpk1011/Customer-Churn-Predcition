from django.db import models

# Create your models here.
class Customer(models.Model):
    RowNumber = models.IntegerField()
    CustomerId = models.IntegerField()
    Surname = models.CharField(max_length=255)
    CreditScore = models.IntegerField()
    Geography = models.CharField(max_length=255)
    Gender = models.CharField(max_length=10)
    Age = models.IntegerField()
    Tenure = models.IntegerField()
    Balance = models.FloatField()
    NumOfProducts = models.IntegerField()
    HasCrCard = models.IntegerField()
    IsActiveMember = models.IntegerField()
    EstimatedSalary = models.FloatField()
    Exited = models.IntegerField()
