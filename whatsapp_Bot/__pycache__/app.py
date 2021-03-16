from flask import Flask,render_template,request
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from flaskwebgui import FlaskUI #get the FlaskUI class
from selenium.webdriver.chrome.options import Options
from PIL import Image



app = Flask(__name__)
ui = FlaskUI(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/send',methods=['POST'])
def send():
    unknown=[]
    file = request.files['file']
    fileimg=request.files['fileimg']
    #image = Image.open(fileimg)
    #image.show()
    #image.save('ab.jpg')

    print(fileimg)
    print(file)
    #img = request.form['myfile']
    #print(img)
    conts = pd.read_csv(file)
    var=0
    var1=0
    var2=0
    var3=0
    mes = request.form['message']
    if '<name>' or '<Name>' in mes:
        var = 1
    if '<date>' or '<Date>' in mes:
        var1 = 1
    if '<amount>' or '<Amount>' in mes:
        var2 = 1
    if '<Product>' or '<product>' in mes:
        var3 = 1
    #if '<date>' or '<Date>' in mes:
    #    var4 = 1
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\mohdu\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe', options=options)

    driver.get('https://web.whatsapp.com/')
    time.sleep(20)
    for i in range(len(conts['Name'])):

        time.sleep(1)
        name = conts['Contact Number'][i]
        time.sleep(0.4)
        name1 = conts['Name'][i]
        date = conts['Date'][i]
        amount = conts['amount'][i]
        product = conts['product'][i]

        print(name1,'-----------------------')
        print(mes)
        mes1 = mes
        if var==1:
            mes1 = mes1.replace('<name>',name1)
            #print(mes,'-----------')
        if var1==1:
            mes1 = mes1.replace('<date>',date)
            #print(mes,'-----------')
        if var2==1:
            mes1 = mes1.replace('<amount>',str(amount))
            #print(mes,'-----------')
        if var3==1:
            mes1 = mes1.replace('<product>',product)
            #print(mes,'-----------')
        #if var4==1:
        #    mes1 = mes.replace('<name>',name1)
        print(mes1,'-----------')
        print(i)
        try:
            search2 = driver.find_element_by_class_name('_1awRl')
        except:
            return "Please Authenticate whatsapp qr code within 20 seconds of pressing start button"
        # name=input("Enter the name to send: ")
        search2 = driver.find_element_by_class_name('_1awRl')
        search2.clear()
        search2.send_keys(str(name))
        time.sleep(1)
        try:
            print(driver.find_elements_by_class_name('_1C6Zl')[0].text.splitlines())

            first_chat = driver.find_elements_by_class_name('_3dHYI')[0]
            first_chat.click()
            time.sleep(0.8)
            print('bb')
            message = driver.find_elements(By.CLASS_NAME, 'selectable-text')[-1]
            message.send_keys(mes1)
            send = driver.find_elements(By.CLASS_NAME, '_2Ujuu')[0]
            #send.click()
            time.sleep(0.4)
            driver.find_elements_by_class_name('bDS3i')[0].click()
            driver.find_elements_by_tag_name('input')[1].send_keys('ab.jpg')
            time.sleep(0.4)
            #driver.find_elements_by_class_name('q2PP6')[0].click()
            time.sleep(0.5)
        except IndexError:
            unknown.append(name)
        except:
            print('a')
    driver.close()
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\mohdu\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe', options=options)
    time.sleep(2)
    for i in unknown:

        driver.get('https://web.whatsapp.com/send?phone='+'+91'+str(i)+'&text='+mes1)
        time.sleep(10)
        send = driver.find_elements(By.CLASS_NAME, '_2Ujuu')[0]
        #send.click()
        time.sleep(0.7)
        driver.find_elements_by_class_name('bDS3i')[0].click()
        time.sleep(0.9)
        driver.find_elements_by_tag_name('input')[1].send_keys(fileimg)
        time.sleep(0.7)
        driver.find_elements_by_class_name('q2PP6')[0].click()
        time.sleep(0.5)
        driver.close()
        options = Options()
        options.add_argument("user-data-dir=C:\\Users\\mohdu\\AppData\\Local\\Google\\Chrome\\User Data")
        driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe', options=options)
        time.sleep(2)
    driver.close()
    return 'Messages Sent'

@app.route('/chatbot',methods=['POST'])
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat',methods=['POST'])
def chat():
    a = request.form['msg']
    print(a)
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run()
    #ui.run()
    #self.flask_app.run(host=self.host, port=self.port)


