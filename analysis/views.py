from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Review, Aspect, Sentiment


# HOME
def home(request):
    return render(request, 'index.html')


# ✅ ADD PRODUCT
@csrf_exempt
@api_view(['POST'])
def add_product(request):
    name = request.data.get('name')

    if not name:
        return Response({"error": "Name required"}, status=400)

    product = Product.objects.create(name=name)

    print("SAVED:", product.id, product.name)

    return Response({
        "message": "Product added",
        "id": product.id,
        "name": product.name
    })


# ✅ GET PRODUCTS
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    return Response([
        {"id": p.id, "name": p.name}
        for p in products
    ])


# ✅ ADD REVIEW (ASPECT + RATING)
@csrf_exempt
@api_view(['POST'])
def analyze_review(request):
    print("DATA:", request.data)

    text = request.data.get('text')
    product_id = request.data.get('product')
    aspect_name = request.data.get('aspect', 'general')
    rating = int(request.data.get('rating', 3))

    if not text or not product_id:
        return Response({"error": "Missing data"}, status=400)

    product = get_object_or_404(Product, id=product_id)

    # Save review
    review = Review.objects.create(
        product=product,
        text=text,
        rating=rating
    )

    # Sentiment
    score = 1 if rating >= 3 else -1

    # ✅ FIXED: avoid MultipleObjectsReturned
    aspect = Aspect.objects.filter(name=aspect_name).first()

    if not aspect:
        aspect = Aspect.objects.create(name=aspect_name)

    # Save sentiment
    Sentiment.objects.create(
        review=review,
        aspect=aspect,
        score=score
    )

    print("REVIEW SAVED:", review.text)

    return Response({"message": "Review added"})
# ✅ GRAPH
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


# ✅ STATS
@api_view(['GET'])
def get_stats(request, product_id):
    sentiments = Sentiment.objects.filter(review__product_id=product_id)

    return Response({
        "total": sentiments.count(),
        "positive": sentiments.filter(score__gt=0).count(),
        "negative": sentiments.filter(score__lt=0).count(),
    })


# ✅ REVIEWS BY ASPECT
@api_view(['GET'])
def get_reviews_by_aspect(request, product_id, aspect_name):
    sentiments = Sentiment.objects.filter(
        review__product_id=product_id,
        aspect__name=aspect_name
    )

    return Response([
        {
            "text": s.review.text,
            "score": s.score,
            "rating": s.review.rating   # ⭐ NEW
        }
        for s in sentiments
    ])