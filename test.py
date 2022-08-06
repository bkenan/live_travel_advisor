import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk



sentence = "Cheapest hotel for two people in Paris from September eleventh until October second"


def test():

    tokens = nltk.word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    punctuations = string.punctuation
    tokens = [w for w in tokens if w.lower() not in stop_words and w not in punctuations]
    wordnet_lemmatizer = WordNetLemmatizer()
    tokens = [wordnet_lemmatizer.lemmatize(word).lower().strip() for word in tokens]
    assert len(tokens) == 9


   
