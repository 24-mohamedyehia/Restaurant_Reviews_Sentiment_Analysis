from flask import Flask, request, render_template
import joblib
import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')

naive_bayes_model = joblib.load(open('./ml_model/Sentiment Analysis Restaurant Reviews naive bayes/MultinomialNB.pkl', 'rb'))
naive_bayes_vectorizer = joblib.load(open('./ml_model/Sentiment Analysis Restaurant Reviews naive bayes/vectorizer.pkl', 'rb'))

# List of common negative words to exclude
negative_words = ['no', 'not', 'never', 'none', 'nobody', 'nothing', 'nowhere']

# Remove negative words from stop_words
filtered_stop_words = [word for word in stop_words if word not in negative_words]

def preprocess_text(review: str) -> str:
    sentence = review.lower()
    without_punc_digit_spaces = re.sub('\s+', ' ', re.sub('[^a-z]', ' ', sentence))  # Remove punctuations, numbers, and multiple spaces
    word_tokens = word_tokenize(without_punc_digit_spaces)      # word tokenization
    without_stopwords = [w for w in word_tokens if not w in filtered_stop_words]   # Remove stopwords
    lema_sent = [lemmatizer.lemmatize(word) for word in without_stopwords ]   # Word Lematization
    sen = ' '.join(lema_sent)   # convert list to string
    return sen

def get_sentiment(review: str) -> str:
    # preprocessing
    text = preprocess_text(review) 
    # vectorization
    text_vector = naive_bayes_vectorizer.transform([text]).toarray()
    # prediction
    prediction = naive_bayes_model.predict(text_vector)[0]

    return prediction

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    # Extract text review from form
    review = list(request.form.values())[0]

    prediction_map = {0: "Negative", 1: "Positive"} 

    sentiment_output = get_sentiment(review)

    return render_template('index.html', Sentiment=f"Sentiment Is: {prediction_map[sentiment_output]}")



if __name__ == "__main__":
    app.run(port=5000, debug=True)
