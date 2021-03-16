import pandas as pd
import pickle
LA = pd.read_csv("D:\Datasets\LoanApproval.csv")
LA.dropna(inplace=True)
LA.drop(["Loan_ID"],axis=1,inplace=True)
LA["Loan_Status"]=LA.Loan_Status.map({"Y": 1, "N": 0})
LA["Gender"]=LA.Gender.map({"Male":1,"Female":0})
LA["Married"]=LA.Married.map({"No":0,"Yes":1})
LA["Education"]=LA.Education.map({"Not Graduate":0,"Graduate":1})
LA["Self_Employed"]=LA.Self_Employed.map({"No":0,"Yes":1})
LA["Property_Area"]=LA.Property_Area.map({"Urban":0,"Semiurban":1,"Rural":2})
x = LA.loc[:,"Gender":"Property_Area"]
y = LA.Loan_Status.values
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.70,random_state=0)
from sklearn.ensemble import RandomForestClassifier
rand_for=RandomForestClassifier(n_estimators=500,max_depth=7,min_samples_split=3,random_state=42)
rand_for.fit(x_train,y_train)
pred = rand_for.predict(x_test)
pickle.dump(rand_for, open('model.pkl','wb'))
