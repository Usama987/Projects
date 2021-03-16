import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('D:\Flask\Loan Approval Classifier Model Deployment using Flask\model.pkl', 'rb'))

@app.route('/')
def home():
    print("Hello app")
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    print("Hello")
    #For rendering results on HTML GUI

    int_features = [int(x) for x in request.form.values()]
    print(int_features)
    for i in int_features:
        print("---",i,"-----")
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    if prediction[0]==0:
        prediction = "Sorry No Loan For You"
    else:
        prediction = "Congrats! Loan Approved"
    return render_template('index.html', prediction_text='{}'.format(prediction))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    print(prediction)
    output = prediction
    return render_template('index.html', prediction_text=prediction)

if __name__ == "__main__":
    app.run(debug=True)