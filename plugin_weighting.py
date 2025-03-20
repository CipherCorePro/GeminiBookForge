from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
stopwords_de = set(stopwords.words('german'))

class BaseWeighting:
    def calculate(self, satz: str, kontext: str) -> float:
        raise NotImplementedError("Muss in der Subklasse implementiert werden")

class TFIDFWeighting(BaseWeighting):
    def calculate(self, satz: str, kontext: str) -> float:
        tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords_de)
        tfidf_matrix = tfidf_vectorizer.fit_transform([kontext])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]

        return sum(tfidf_scores[i] for i in range(len(feature_names)) if feature_names[i] in satz.split()) / len(satz.split())

class PositionsbasierteWeighting(BaseWeighting):
    def calculate(self, satz: str, kontext: str) -> float:
        return 0.4  # Beispiel-Wert

class KombinierteWeighting(BaseWeighting):
    def calculate(self, satz: str, kontext: str) -> float:
        # Beispiel-Implementierung für kombinierte Gewichtung
        return 0.6