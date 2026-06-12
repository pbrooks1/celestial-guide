"""
This file handles the NLP and machine learning portion of Celestial Guide.
It preprocesses user input with spaCy, converts text with TF-IDF,
and uses Logistic Regression to classify the user's intent.
"""

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from training_data import TRAINING_SAMPLES
from difflib import get_close_matches

nlp = spacy.load("en_core_web_sm")

SIGNS = {
    "aries": ["aries", "ariess"],
    "taurus": ["taurus", "taurs", "tauras"],
    "gemini": ["gemini", "gemeni", "geminy"],
    "cancer": ["cancer", "cancr"],
    "leo": ["leo"],
    "virgo": ["virgo", "virgoe"],
    "libra": ["libra", "libra"],
    "scorpio": ["scorpio", "scorpios", "scorp"],
    "sagittarius": [
        "sagittarius",
        "saggitarius",
        "saggitarus",
        "sagitarius",
        "sagitarus",
        "saggitasrus",
        "saggitatusu",
        "sagittarius"
    ],
    "capricorn": ["capricorn", "capicorn", "capricon"],
    "aquarius": ["aquarius", "aquarious", "aquarias"],
    "pisces": ["pisces", "pices", "pisces"]
}

def find_sign(user_input):
    for sign in SIGNS:
        if sign.lower() in user_input.lower():
            return sign
    return None

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(tokens)

def detect_sign(user_input):

    zodiac_signs = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
    ]

    cleaned = (
        user_input.lower()
        .replace("?", "")
        .replace(",", "")
        .replace(".", "")
        .replace("!", "")
    )

    words = cleaned.split()

    # Exact match first
    for word in words:
        if word in zodiac_signs:
            return word.capitalize()

    # Fuzzy match for typos
    for word in words:
        close_match = get_close_matches(word, zodiac_signs, n=1, cutoff=0.65)
        if close_match:
            return close_match[0].capitalize()

    return None

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.is_trained = False

    def train(self):
        texts = [preprocess_text(text) for text, label in TRAINING_SAMPLES]
        labels = [label for text, label in TRAINING_SAMPLES]

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.is_trained = True

    def predict_intent(self, user_input, threshold=0.25):
        if not self.is_trained:
            raise ValueError("Model must be trained first.")

        sign = detect_sign(user_input)
        processed_input = preprocess_text(user_input)
        X_input = self.vectorizer.transform([processed_input])

        probabilities = self.model.predict_proba(X_input)[0]
        best_index = probabilities.argmax()
        predicted_intent = self.model.classes_[best_index]
        confidence = float(probabilities[best_index])

        if confidence < threshold:
            return "unknown", sign, confidence

        return predicted_intent, sign, confidence