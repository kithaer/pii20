import psycopg2


def connect():
    cn = None
    cn = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="PEBot")
    return cn

def addItemToCart(uid,iid,count,price):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" INSERT INTO public."cart"("userid","itemid","count","price") VALUES ({uid},{iid},{count},{price}) """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def addorder(post,address,items,price,name):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" INSERT INTO public."orders"("post","address","items","price","name","status") VALUES ('{post}','{address}','{items}',{price},'{name}',1) """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()


def addUser(tid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" INSERT INTO public."users"("telegramid") VALUES ({tid}) """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def addfio(fio,tid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" UPDATE public.users SET "fio" = '{fio}' WHERE "telegramid" = {tid}"""
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def addaddress(ad,tid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" UPDATE public.users SET "address" = '{ad}' WHERE "telegramid" = {tid}"""
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def addpost(post,tid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" UPDATE public.users SET "postindex" = '{post}' WHERE "telegramid" = {tid}"""
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def getItem():
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" SELECT * FROM public."Items" """
        cursor.execute(querry)
        info = cursor.fetchall()
        print(info)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()
            return info

def getItemByID(id):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" SELECT * FROM public."Items" WHERE "id" = {id} """
        cursor.execute(querry)
        info = cursor.fetchall()
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()
            return info




def updCountCart(uid,iid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" UPDATE public.cart SET "count" = "count"+1 WHERE "userid" = {uid} AND "itemid" = {iid} """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def subCountCart(uid,iid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" UPDATE public.cart SET "count" = "count"-1 WHERE "userid" = {uid} AND "itemid" = {iid} """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def getcart(tID):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" SELECT * FROM public."cart" WHERE "userid" ={tID} """
        cursor.execute(querry)
        cart = cursor.fetchall()
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()
            return cart


def delcartID(tID,iid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" DELETE FROM public."cart" WHERE "userid" ={tID} AND "itemid" = {iid} """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def finalcart(tID):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" DELETE FROM public."cart" WHERE "userid" ={tID} """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def finalusers(tID):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" DELETE FROM public."users" WHERE "telegramid" ={tID} """
        cursor.execute(querry)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()


def getcartID(tID,iid):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" SELECT * FROM public."cart" WHERE "userid" ={tID} AND "itemid" = {iid} """
        cursor.execute(querry)
        cart = cursor.fetchall()
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()
            return cart


def getusers(tID):
    try:
        connection = connect()
        cursor = connection.cursor()
        querry = f""" SELECT * FROM public."users" WHERE "telegramid" ={tID} """
        cursor.execute(querry)
        cart = cursor.fetchall()
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()
            return cart
