import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os
from typing import Dict, Any

# Initialize NLP pipeline
nlp = spacy.load("en_core_web_sm")

class EmailClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.model = MultinomialNB()
        self.categories = ["sales", "support", "inquiry", "spam"]
        
        # Load or initialize model
        if os.path.exists("email_classifier.joblib"):
            self.load_model()
    
    def preprocess_text(self, text: str) -> str:
        """Clean and lemmatize text for classification"""
        doc = nlp(text)
        return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
    
    def train(self, X, y):
        """Train the classifier with sample data"""
        X_processed = [self.preprocess_text(text) for text in X]
        X_vectorized = self.vectorizer.fit_transform(X_processed)
        self.model.fit(X_vectorized, y)
        self.save_model()
    
    def predict(self, email_text: str) -> Dict[str, Any]:
        """Classify an email into predefined categories"""
        processed = self.preprocess_text(email_text)
        vectorized = self.vectorizer.transform([processed])
        probas = self.model.predict_proba(vectorized)[0]
        
        return {
            "category": self.categories[self.model.predict(vectorized)[0]],
            "confidence": max(probas),
            "probabilities": dict(zip(self.categories, probas))
        }
    
    def save_model(self):
        """Save the trained model to disk"""
        joblib.dump({
            "vectorizer": self.vectorizer,
            "model": self.model
        }, "email_classifier.joblib")
    
    def load_model(self):
        """Load a trained model from disk"""
        data = joblib.load("email_classifier.joblib")
        self.vectorizer = data["vectorizer"]
        self.model = data["model"]
