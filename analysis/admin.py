from django.contrib import admin
from .models import Product, Review, Aspect, Sentiment

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Aspect)
admin.site.register(Sentiment)