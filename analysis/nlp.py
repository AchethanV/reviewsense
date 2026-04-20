import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()
ASPECTS = ["battery", "screen"]

# You can expand later
ASPECTS = ["battery", "screen", "camera", "delivery", "price"]

def extract_aspects(text):
    doc = nlp(text.lower())
    return [token.text for token in doc if token.text in ASPECTS]

def get_sentiment(text):
    return analyzer.polarity_scores(text)["compound"]