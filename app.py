import os
import requests
from flask import Flask, request, jsonify
import sqlalchemy
from sqlalchemy.sql import select




app = Flask(__name__)
engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'], echo=True)
conn = engine.connect()

APP_ID = os.environ['APP_ID']


@app.route('/rates', methods=['GET'])
def get():
    date_from=request.args.get('date_from')
    date_to=request.args.get('date_to')
    origin=request.args.get('origin')
    destination=request.args.get('destination')
    # query = "select price from prices where orig_code = '{}' and dest_code = '{}'".format(origin, destination)

    #get the origin
    query2 = " select code from ports where '{}' in (code, parent_slug)".format(origin)
    print(query2)
    origin = engine.execute(query2).first()
    origin = ''.join(origin)

    #get the destination
    query3 = " select code from ports where '{}' in (code, parent_slug)".format(destination)
    print(query3)
    destination = engine.execute(query3).first()
    destination = ''.join(destination)

    #get record between dates
    query = "select * from prices where day between '{}' and '{}' and orig_code='{}' and dest_code='{}' ".format(date_from, date_to, origin, destination)
    print(query)
    result = engine.execute(query)


    return jsonify({"date_from": date_from, "date_to": date_to, "origin": origin, "destination": destination, "result": [dict(row) for row in result]})

@app.route('/rates', methods=['POST'])
def post():
    date=request.args.get('date')
    origin_code=request.args.get('origin_code')
    destination_code=request.args.get('destination_code')
    price=request.args.get('price')


    payload = {"app_id": APP_ID}
    in_us_dollars = requests.get('https://openexchangerates.org/api/latest.json?', params=payload)
    in_us_dollars_json = in_us_dollars.json()
    usd = in_us_dollars_json['rates']['USD']
    price_in_usd = price * usd

    insert_query = " "

    return jsonify({"date": date,"origin_code": origin_code, "destination_code": destination_code, "price": price_in_usd})


if __name__ == '__main__':
    app.run(debug=True)