import base64
import bytes
import hashlib
import psycopg2
from flask import Flask, jsonify
from flask_restful import Api, Resource

import db

app = Flask(__name__)
api = Api()


def connect():
    cn = None
    cn = psycopg2.connect(user="postgres",
                          password="admin",
                          host="127.0.0.1",
                          port="5432",
                          database="PEBot")
    return cn


@app.route('/setphoto/<int:id>&<string:link1>', methods=['PUT'])
def setphoto(id, link1):
    link = base64.urlsafe_b64decode(link1)
    link = link.decode("utf-8")
    connection = connect()
    cursor = connection.cursor()
    update_query = f"""UPDATE public."Items" SET photo = '{link}' WHERE "id" = {id}"""
    cursor.execute(update_query)
    connection.commit()
    return getitems()


@app.route('/additem/<string:name>&<int:price>&<int:count>', methods=['POST'])
def additem(name, price, count):
    connection = connect()
    cur = connection.cursor()
    sql_query = f"""INSERT INTO public."Items" ("name", "price", "count") VALUES ('{name}',{price},{count}) """
    out = cur.execute(sql_query)
    connection.commit()
    return getitems()


@app.route('/deleteitem/<int:id>', methods=['DELETE'])
def deleteitem(id):
    connection = connect()
    cur = connection.cursor()
    sql_query = f"""DELETE FROM public."Items" WHERE "id" = {id} """
    cur.execute(sql_query)
    print(sql_query)
    connection.commit()
    return getitems()


@app.route('/getitems', methods=['GET'])
def getitems():
    connection = connect()
    cur = connection.cursor()
    sql_query = """SELECT json_agg(t)
from (SELECT * FROM public."Items") t """
    out = cur.execute(sql_query)
    print(sql_query)
    context_records = cur.fetchall()
    ContextRootKeys = []
    for row in context_records:
        ContextRootKeys.append(row)
    connection.commit()
    print(ContextRootKeys)
    return jsonify(ContextRootKeys)


@app.route('/getorders', methods=['GET'])
def getorders():
    connection = connect()
    cur = connection.cursor()
    sql_query = """SELECT json_agg(t)
from (SELECT * FROM public."orders") t """
    out = cur.execute(sql_query)
    print(sql_query)
    context_records = cur.fetchall()
    ContextRootKeys = []
    for row in context_records:
        ContextRootKeys.append(row)
    connection.commit()
    print(ContextRootKeys)
    return jsonify(ContextRootKeys)


@app.route('/setstatus/<int:id>&<int:stat>', methods=['PUT'])
def setstatus(id, stat):
    connection = connect()
    cursor = connection.cursor()
    update_query = f"""UPDATE public."orders" SET status = '{stat}' WHERE "id" = {id}"""
    cursor.execute(update_query)
    connection.commit()
    return getorders()


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
