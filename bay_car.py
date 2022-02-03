#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:36:13 2022

@author: lenovo
"""

import requests
import mysql.connector
from bs4 import BeautifulSoup
from sklearn import preprocessing

cnx = mysql.connector.connect(user = 'root',
                              host = 'localhost',
                              password = 'root',
                              database = 'car')

url = 'https://www.cars.com/shopping/results/?page='
for page in range(1, 100):
    r = requests.get(url + str(page))
    
    soup = BeautifulSoup(r.text, 'html.parser')
    ads = soup.find_all('div', attrs= {'class' : 'vehicle-details'})
    
    for ad in ads:
        car_name = (ad.find('a', attrs = {'class' : 'vehicle-card-link'}).text[6:])
        car_year = (ad.find('a', attrs = {'class' : 'vehicle-card-link'}).text[1:5])
        car_kms = (ad.find('div', attrs = {'class' : 'mileage'}).text)
        car_price = (ad.find('div', attrs = {'class' : 'price-section'}).text)
        
        cursor = cnx.cursor()
        cursor.execute('INSERT INTO ads VALUES (\'%s\',\'%s\',\'%s\',\'%s\')'%(car_name,
                                                                               car_year,
                                                                               car_kms,
                                                                               car_price,))
        cnx.commit()

cursor = cnx.cursor()
query = 'SELECT * FROM ads;'
cursor.execute(query)

cars = []
for (title, year, kms, price) in cursor:
    car = [title, year, kms, price]
    cars.append(car)
for car in cars:
    le = preprocessing.LabelEncoder()
    title, year, kms, price = car
    le = le.fit([title, year, kms, price])

cnx.close()

