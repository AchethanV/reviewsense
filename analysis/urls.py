from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('add-product/', add_product),
    path('products/', get_products),
    path('analyze/', analyze_review),
    path('graph/<int:product_id>/', get_graph),
    path('stats/<int:product_id>/', get_stats),
    path('reviews/<int:product_id>/<str:aspect_name>/', get_reviews_by_aspect),
]