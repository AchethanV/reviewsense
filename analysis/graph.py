import networkx as nx
from .models import Sentiment

def build_graph(product_id):
    G = nx.Graph()

    sentiments = Sentiment.objects.filter(review__product_id=product_id)

    for s in sentiments:
        product = s.review.product.name
        aspect = s.aspect.name
        score = s.score

        # Add nodes
        G.add_node(product, type="product")
        G.add_node(aspect, type="aspect")

        # Add edge with sentiment weight
        G.add_edge(product, aspect, weight=score)

    return nx.node_link_data(G)