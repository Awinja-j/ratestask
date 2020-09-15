import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get():
    date_from=request.args.get('date_from')
    date_to=request.args.get('date_to')
    origin=request.args.get('origin')
    destination=request.args.get('destination')
    return jsonify({"date_from": date_from, "date_to": date_to, "origin": origin, "destination": destination})

@app.route('/rates', methods=['POST'])
def post():
    date_from=request.args.get('date_from')
    date_to=request.args.get('date_to')
    origin_code=request.args.get('origin_code')
    destination_code=request.args.get('destination_code')
    price=request.args.get('price')

    return jsonify({"date_from": date_from, "date_to": date_to, "origin_code": origin_code, "destination_code": destination_code})


if __name__ == '__main__':
    app.run(debug=True)