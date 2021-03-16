from flask import Flask,render_template
import joblib
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
import time


app = Flask(__name__)
model=joblib.load('D:/Flask/Presentation/model.pkl')

@app.route('/')
def home():
    print("Hello app")
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    print("Hello")
    #For rendering results on HTML GUI

    int_features = [float(x) for x in request.form.values()]
    print(int_features)
    for i in int_features:
        print("---",i,"-----")
    prediction = loaded_model.predict([int_features])
    print("-------------prediction--------------------",prediction)
    if prediction[0][0]<0.5:
        prediction = "Good Relation Maintained"
    else:
        prediction = "Need to Focus on the Customer"
    return render_template('index.html', prediction_text='{}'.format(prediction))



@app.route('/predict1',methods=['POST'])
def predict1():
    '''
    For direct API calls trought request
    '''





    fraud_df = request.files['file']
    cust = pd.read_csv(fraud_df)


    #cust = cust.drop(["transaction_initiation"], axis=1)

    categorical_columns = ['user_id', 'payment_method', 'partner_id', 'partner_category',
                           'device_type', 'partner_pricing_category', 'year',
                           'month', 'hour', 'weekofyear']
    train_data = cust

    if 'is_fraud' in cust.columns:
        train_data = cust.drop(["is_fraud"], axis=1)

    train_data.transaction_initiation = pd.to_datetime(train_data.transaction_initiation)

    for each in ['user_id', 'payment_method', 'partner_id', 'partner_category', 'device_type',
                 'partner_pricing_category']:
        train_data[each] = train_data[each].astype('category')
    train_data["year"] = pd.DataFrame(train_data.transaction_initiation.dt.year).astype('category')
    train_data["month"] = pd.DataFrame(train_data.transaction_initiation.dt.month).astype('category')
    train_data["hour"] = pd.DataFrame(train_data.transaction_initiation.dt.hour).astype('category')
    train_data["weekofyear"] = pd.DataFrame(train_data.transaction_initiation.dt.weekofyear).astype('category')
    train_data["year"] = train_data["year"].astype('category')
    train_data["month"] = train_data["month"].astype('category')
    train_data["hour"] = train_data["hour"].astype('category')
    train_data["weekofyear"] = train_data["weekofyear"].astype('category')

    cust=train_data

    num_X_train = pd.DataFrame(cust["money_transacted"])

    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(cust[categorical_columns]))

    # One-hot encoding removed index; put it back
    OH_cols_train.index = cust.index

    # One-hot encoding assigns the sequence numbers as the columns names.
    OH_cols_train.columns = OH_encoder.get_feature_names()

    # Add one-hot encoded columns to imputed numerical features
    Xtrain = pd.concat([num_X_train, OH_cols_train], axis=1)

    prediction = model.predict(Xtrain)
    print(Xtrain.columns)
    l1 = [i for i in cust.user_id]

    pred = []
    li = [i for i in prediction]


    for m in range(len(li)):
        if li[m]>0.50:

            li[m]="Possibly Fraud"
        else:

            li[m]="Legal Transaction"
    time.sleep(4)
    predd=[]
    Exited=[]
    for i in li:
        predd.append(i)
    z1 = zip(l1,predd)

    #print(len(z1))

    return render_template('multi.html',result=z1)



if __name__ == '__main__':
    app.run()
