import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'Gender':1, 'Married':0, 'Dependents':3,'Education':1,'Self_Employed':1,'ApplicantIncome':100,'CoapplicantIncome':2,'LoanAmount':300,'Loan_Amount_Term':3,'Credit_History':1,'Property_Area':2})

print(r.json())
