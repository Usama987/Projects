from flask import Flask, render_template, request
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/reviews',methods=['POST'])
def review():
    x = request.form['prod']
    path = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(path)
    time.sleep(2)
    driver.get("https://www.amazon.in")
    time.sleep(0.8)
    search = driver.find_element_by_id('twotabsearchtextbox')
    search.send_keys(x)
    search.submit()
    driver.find_elements(By.TAG_NAME, 'h2')[0].click()
    time.sleep(0.9)
    driver.switch_to_window(driver.window_handles[2])
    allrev = driver.find_elements(By.LINK_TEXT, 'See all reviews')[0].click()
    prod = []
    for i in range(3):
        time.sleep(2)
        r1 = driver.find_elements(By.CLASS_NAME, 'review')
        prod.extend([(i.text) for i in r1])
        time.sleep(0.9)
        driver.find_element_by_class_name('a-last').click()
    names = []
    titles = []
    for i in prod:
        names.append(i.splitlines()[0])
        titles.append(i.splitlines()[1])
    rev = zip(names, titles)
    return render_template('reviews.html',result=rev)

if __name__ == '__main__':
    app.run()
