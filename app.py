import os
import requests
from flask import Flask, request, jsonify
import sqlalchemy
from sqlalchemy.sql import select




app = Flask(__name__)
engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
conn = engine.connect()

APP_ID = os.environ['APP_ID']

@app.route('/', methods=['GET', 'POST'])
def healthcheck():
    return jsonify({"heathcheck": "Everything is Fine, Houston"})


@app.route('/rates', methods=['GET'])
def rates():

    try:

        date_from=request.args.get('date_from')
        date_to=request.args.get('date_to')
        origin=request.args.get('origin')
        destination=request.args.get('destination')

        #get the origin
        query2 = " select code from ports where '{}' in (code, parent_slug)".format(origin)
        origin = engine.execute(query2).first()
        origin = ''.join(origin)

        #get the destination
        query3 = " select code from ports where '{}' in (code, parent_slug)".format(destination)
        destination = engine.execute(query3).first()
        destination = ''.join(destination)

        #get record between dates
        query = "select day, avg(cast(price as float)) as average_price from prices where orig_code = '{}' and dest_code = '{}' and day between '{}' and '{}' group by day;".format(origin, destination, date_from, date_to)
        result = engine.execute(query)
        return jsonify({"date_from": date_from, "date_to": date_to, "origin": origin, "destination": destination, "result": [dict(row) for row in result]})

    except:
        return jsonify({"Error": "Missing argument"})

@app.route('/rates_null', methods=['GET'])
def rates_null():
    try:

        date_from=request.args.get('date_from')
        date_to=request.args.get('date_to')
        origin=request.args.get('origin')
        destination=request.args.get('destination')

        #get the origin
        query2 = " select code from ports where '{}' in (code, parent_slug)".format(origin)
        origin = engine.execute(query2).first()
        origin = ''.join(origin)

        #get the destination
        query3 = " select code from ports where '{}' in (code, parent_slug)".format(destination)
        destination = engine.execute(query3).first()
        destination = ''.join(destination)

        #get record between dates
        query = "select day, avg(cast(price as float)) as average_price from prices where orig_code = '{}' and dest_code = '{}' and day between '{}' and '{}' group by day having count(*) >2;".format(origin, destination, date_from, date_to)
        result = engine.execute(query)

        return jsonify({"date_from": date_from, "date_to": date_to, "origin": origin, "destination": destination, "result": [dict(row) for row in result]})
    
    except:
        return jsonify({"Error": "Missing argument"})

@app.route('/rates', methods=['POST'])
def rates_post():
    try:
        date=request.args.get('date')
        origin_code=request.args.get('origin_code')
        destination_code=request.args.get('destination_code')
        price=request.args.get('price')


        payload = {"app_id": APP_ID}
        in_us_dollars = requests.get('https://openexchangerates.org/api/latest.json?', params=payload)
        in_us_dollars_json = in_us_dollars.json()
        usd = in_us_dollars_json['rates']['USD']
        price_in_usd = price * usd

        check_destination = "SELECT code FROM ports WHERE '{}' IN(code, parent_slug) limit 1;".format(destination_code)
        check_destination_result = engine.execute(check_destination)

        check_origin = "SELECT code FROM ports WHERE '{}' IN(code, parent_slug) limit 1;".format(origin_code)
        check_origin_result = engine.execute(check_origin)

        check_destination_result = [dict(row) for row in check_destination_result]
        check_origin_result = [dict(row) for row in check_origin_result]

        destination_code_result = (check_destination_result[0]['code'])
        origin_code_result = (check_origin_result[0]['code'])

        if len(check_destination_result[0]) == len(check_origin_result[0]) >0:
                insert_query = "INSERT INTO prices (orig_code, dest_code, day, price) VALUES ('{}', '{}', '{}', '{}')".format(origin_code_result, destination_code_result, date, price_in_usd)
                engine.execute(insert_query)
                return jsonify({"date": date,"origin_code": origin_code_result, "destination_code": destination_code_result, "price": price_in_usd})
        else:
            return jsonify({"Error": "Destination code or origin code does not exist"})

    except:
        return jsonify({"Error": "Missing argument"})


    

if __name__ == '__main__':
    app.run(debug=True)