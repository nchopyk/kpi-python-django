from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Technique(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    energy_efficiency_class = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    electricity_costs_per_year = models.IntegerField()
    price = models.IntegerField()
    photo_url_path = models.CharField(max_length=400, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.model}"
