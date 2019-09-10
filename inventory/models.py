from django.db import models

# Create your models here.


class Product(models.Model):
    p_id = models.IntegerField(primary_key=True)
    p_name = models.CharField(max_length=255)
    p_price = models.FloatField()
    stocks = models.IntegerField(null=True)

    def __str__(self):
        return str(self.p_name)


class Restock(models.Model):
    date = models.DateField()
    r_id = models.AutoField(primary_key=True, serialize=True)
    gst = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return str(self.r_id)


class Stock(models.Model):
    restock_id = models.ForeignKey("Restock", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    in_stock = models.IntegerField()  # quantity coming in
    amount = models.FloatField()

    def __str__(self):
        return str(self.restock_id)


class Sale(models.Model):
    date = models.DateField()
    sale_id = models.AutoField(primary_key=True, serialize=True)
    gst = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return str(self.sale_id)


class Bill(models.Model):
    bill_id = models.ForeignKey("Sale", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return str(self.bill_id)
