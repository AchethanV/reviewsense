from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import Product, Review, Aspect, Sentiment


# HOME
def home(request):
    return render(request, 'index.html')


# ADD PRODUCT ✅
@api_view(['POST'])
def add_product(request):
    name = request.data.get('name')
    brand = request.data.get('brand')

    if not name:
        return Response({"error": "Name required"})

    product = Product.objects.create(name=name, brand=brand)

    return Response({"message": "Product added"})


# GET PRODUCTS ✅
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    return Response([
        {"id": p.id, "name": p.name}
        for p in products
    ])


# ADD REVIEW + SIMPLE SENTIMENT ✅
@api_view(['POST'])
def analyze_review(request):
    text = request.data.get('text')
    product_id = request.data.get('product')

    product = get_object_or_404(Product, id=product_id)

    review = Review.objects.create(product=product, text=text)

    score = 1 if "good" in text.lower() else -1

    Sentiment.objects.create(
        review=review,
        aspect=Aspect.objects.get_or_create(name="general")[0],
        score=score
    )

    return Response({"message": "Review added"})


# GRAPH (WORKING VERSION) ✅
@api_view(['GET'])
def get_graph(request, product_id):
    sentiments = Sentiment.objects.filter(review__product_id=product_id)

    nodes = []
    edges = []

    product = Product.objects.get(id=product_id)

    nodes.append({"id": product.name, "type": "product"})

    for s in sentiments:
        aspect = s.aspect.name

        if not any(n["id"] == aspect for n in nodes):
            nodes.append({"id": aspect, "type": "aspect"})

        edges.append({
            "source": product.name,
            "target": aspect,
            "weight": s.score
        })

    return Response({
        "nodes": nodes,
        "edges": edges
    })


# STATS
@api_view(['GET'])
def get_stats(request, product_id):
    sentiments = Sentiment.objects.filter(review__product_id=product_id)

    return Response({
        "total": sentiments.count(),
        "positive": sentiments.filter(score__gt=0).count(),
        "negative": sentiments.filter(score__lt=0).count(),
    })


# REVIEWS
@api_view(['GET'])
def get_reviews_by_aspect(request, product_id, aspect_name):
    sentiments = Sentiment.objects.filter(review__product_id=product_id)

    return Response([
        {"text": s.review.text, "score": s.score}
        for s in sentiments
    ])