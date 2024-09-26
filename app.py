import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open('./ml_model/model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from form data
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    
    # Make prediction using the model
    prediction = model.predict(final_features)
    
    # Prepare output for rendering
    output = round(prediction[0])
    
    return render_template('index.html', prediction_text="Number of Weekly Rides Should be {}".format(output))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
