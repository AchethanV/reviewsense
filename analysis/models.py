from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=3)  # ⭐ REQUIRED

    def __str__(self):
        return self.text[:50]


class Aspect(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 🔥 ADD THIS

    def __str__(self):
        return self.name


class Sentiment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE)
    score = models.FloatField()
