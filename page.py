# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 13:12:04 2022

@author: jin
"""


from flask import Flask
from flask import request
from flask_cors import CORS
from flask import make_response
from flask import render_template
import pymysql
from pandas import DataFrame as df
from datetime import datetime
from random import random

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('newPage.html')


@app.route('/loginPage', methods=['POST', 'GET'])
def loginPage():
    return render_template('login.html')


@app.route('/merchandise', methods=['POST', 'GET'])
def merchandise():
    return render_template('merchandise.html')


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    return render_template('cart.html')


@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    return render_template('checkout.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    idpw = request.get_json()
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "SELECT * FROM idlist WHERE id='{}'".format(idpw['account'])
    cur.execute(command)
    results = cur.fetchall()
    results = df(results)
    if len(results) == 0:
        print('不存在')
        return '不存在'
    elif idpw['password'] != results.iloc[0][1]:
        print('不符合')
        return '不符合'
    else:
        v = str(random())[2:7]
        resp = make_response(idpw['account'])
        resp.set_cookie('result', value='ok')
        resp.set_cookie('ip', value=v)
        ip = v
        command = "update idlist set ip='{}' where id='{}'".format(
                                                          ip, idpw['account'])
        cur.execute(command)
        conn.commit()
        return resp


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    ip = request.cookies.get('ip')
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "SELECT * FROM idlist WHERE ip='{}'".format(ip)
    cur.execute(command)
    results = cur.fetchall()
    results = df(results)
    command = "update idlist set ip='{}' where ip='{}'".format('', ip)
    cur.execute(command)
    conn.commit()
    resp = make_response('delete')
    resp.set_cookie('result', value='ok')
    resp.set_cookie('ip', value='0', expires=0)
    return '{} logout'.format(results[0][0])


@app.route('/vailidate', methods=['POST', 'GET'])
def vailidate():
    ip = request.cookies.get('ip')
    print(ip)
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "SELECT * FROM idlist WHERE ip='{}'".format(ip)
    cur.execute(command)
    results = cur.fetchall()
    results = df(results)
    if len(results) == 0:
        print('請先登入  ')
        return "請先登入  "
    else:
        return '{} login'.format(results.iloc[0][0])


@app.route('/pageClick', methods=['POST', 'GET'])
def pageClick():
    name = request.get_json()
    print(name)
    ip = request.cookies.get('ip')
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "SELECT * FROM idlist WHERE ip='{}'".format(ip)
    cur.execute(command)
    results = cur.fetchall()
    results = df(results)
    if len(results) == 0:
        print('請先登入  ')
        return "請先登入  "
    else:
        command = "UPDATE idlist SET page='{}' where ip='{}'".format(
                                                        name['foodName'], ip)
        print(command)
        cur.execute(command)
        conn.commit()
        return 'update page finish'


@app.route('/pageInitial', methods=['POST', 'GET'])
def pageInitial():
    ip = request.cookies.get('ip')
    print('ip')
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "select page from idlist where ip='{}'".format(ip)
    print(ip)
    cur.execute(command)
    page = cur.fetchall()[0][0]
    print('目前進入{}頁面'.format(page))
    cur = conn.cursor()
    command = "select name,price,photo from sale where category='{}'".format(
                                                                        page)
    if page == 'dessert':
        page = '零食'
    elif page == 'fruit':
        page = '水果'
    elif page == 'softDrink':
        page = '汽水'
    elif page == 'juice':
        page = '果汁'
    dic = {"page": page}
    cur.execute(command)
    items = cur.fetchall()
    times = 0
    string = ""
    for item in items:
        if item == items[-1]:
            if times > 3:
                string += "|"
                string = string+item[0]+'='+item[1]+'='+item[2]
                times = 0
            else:
                string = string+item[0]+'='+item[1]+'='+item[2]
                times = 0
        elif times < 4:
            if times == 3:
                string = string+item[0]+'='+item[1]+'='+item[2]
                times += 1
            else:
                string = string+item[0]+'='+item[1]+'='+item[2]+'-'
                times += 1
        else:
            string += "|"
            string = string+item[0]+'='+item[1]+'='+item[2]+'-'
            times = 0
    string += ""
    print(string)
    print('2')
    dic["items"] = string
    return str(dic).replace("'", '"')


@app.route('/addCart', methods=['POST', 'GET'])
def addCart():
    data = request.get_json()
    ip = request.cookies.get('ip')
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "select cart from idlist where ip='{}'".format(ip)
    cur.execute(command)
    cartData = cur.fetchall()[0][0]
    name = data['name']
    price = data['price']
    times = data['times']
    if cartData == None:
        cartData = ''
    cartList = cartData.split('|')
    delete_item = ''
    if times == '1':
        for l in range(len(cartList)):
            if name in cartList[l]:
                temp = cartList[l].split(',')
                temp[2] = str(int(temp[2])+1)
                cartList[l] = ','.join(temp)
            else:
                pass
    elif times == '10':
        for l in range(len(cartList)):
            if name in cartList[l]:
                temp = cartList[l].split(',')
                temp[2] = str(int(temp[2])+10)
                cartList[l] = ','.join(temp)
            else:
                pass
    elif times == '-1':
        for l in range(len(cartList)):
            if name in cartList[l]:
                temp = cartList[l].split(',')
                temp[2] = str(int(temp[2])-1)
                if int(temp[2]) <= 0:
                    delete_item = cartList[l]
                else:
                    cartList[l] = ','.join(temp)
            else:
                pass
    elif times == '-10':
        for l in range(len(cartList)):
            if name in cartList[l]:
                temp = cartList[l].split(',')
                temp[2] = str(int(temp[2])-10)
                if int(temp[2]) <= 0:
                    delete_item = cartList[l]
                else:
                    cartList[l] = ','.join(temp)
            else:
                pass
    if delete_item != '':
        cartList.remove(delete_item)
    cartList = '|'.join(cartList)
    string = ''
    if name not in cartList and len(cartList) == 0 and delete_item == '':
        string = name+','+price+',1'
    elif name not in cartList and delete_item == '':
        string = cartList+'|'+name+','+price+',1'
    else:
        string = cartList
    command = "update idlist set cart='{}' where ip='{}' ".format(string, ip)
    cur.execute(command)
    conn.commit()
    cur = conn.cursor()
    command = "select cart from idlist where ip='{}'".format(ip)
    cur.execute(command)
    cartData = cur.fetchall()[0][0]
    dic = {"items": cartData}
    return str(dic).replace("'", '"')


@app.route('/addCheck', methods=['POST', 'GET'])
def addCheck():
    # data = request.get_json()
    ip = request.cookies.get('ip')
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "select cart from idlist where ip='{}'".format(ip)
    cur.execute(command)
    cartData = cur.fetchall()[0][0]
    now = datetime.now()
    today = ''.join(str(now).split(' ')[0].split('-'))
    time = ''.join(str(now).split(' ')[1].split('.')[0].split(':'))
    no = today+time
    checkData = no+'@'+cartData
    print(checkData)
    string = ''
    command = "select book from idlist where ip='{}'".format(ip)
    cur.execute(command)
    check = cur.fetchall()[0][0]
    if cartData != None or cartData != '':
        if check != '' and check != None:
            string = check+'-'+checkData
        else:
            string = checkData
        command = "update idlist set cart='' where ip='{}' ".format(ip)
        cur.execute(command)
        conn.commit()
        cur = conn.cursor()
        command = "update idlist set book='{}' where ip='{}' ".format(
                                                            string, ip)
        cur.execute(command)
        conn.commit()
        cur = conn.cursor()
        command = "select book from idlist where ip='{}'".format(ip)
        cur.execute(command)
        checkData = cur.fetchall()[0][0]
        dic = {"items": checkData}
    else:
        dic = {"items": 'no'}
    return str(dic).replace("'", '"')


@app.route('/deleteCheck', methods=['POST', 'GET'])
def deleteCheck():
    data = request.get_json()
    ip = request.cookies.get('ip')
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "select book from idlist where ip='{}'".format(ip)
    cur.execute(command)
    checkData = cur.fetchall()[0][0]
    checkData = checkData.split('-')
    for d in checkData:
        if data['no'] in d:
            checkData.remove(d)
    checkData = '-'.join(checkData)
    command = "update idlist set book='{}' where ip='{}' ".format(checkData,
                                                                  ip)
    cur.execute(command)
    conn.commit()
    dic = {"items": checkData}
    print(dic)
    return str(dic).replace("'", '"')


@app.route('/cartView', methods=['POST', 'GET'])
def cartView():
    ip = request.cookies.get('ip')
    print(ip)
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "select cart from idlist where ip='{}'".format(ip)
    cur.execute(command)
    cartData = cur.fetchall()[0][0]
    dic = {"items": cartData}
    return str(dic).replace("'", '"')


@app.route('/checkView', methods=['POST', 'GET'])
def checkView():
    ip = request.cookies.get('ip')
    print('@'+str(ip))
    now = datetime.now()
    today = ''.join(str(now).split(' ')[0].split('-'))
    time = ''.join(str(now).split(' ')[1].split('.')[0].split(':'))
    no = today+time
    conn = pymysql.connect(host='', port=,
                           user='', password='',
                           database='')
    cur = conn.cursor()
    command = "select book from idlist where ip='{}'".format(ip)
    cur.execute(command)
    cartData = cur.fetchall()[0][0]
    dic = {"items": cartData, "no": no}
    return str(dic).replace("'", '"')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8003)
