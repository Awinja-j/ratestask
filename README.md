# Rates

### Requirements
- python 3.5/python 3.6.
- Postgres | Postico

### Installation
Clone this repo using htts or ssh, depending on your preference.

ssh:

`$ git clone git@github.com:Awinja-j/ratestask.git`

http:

`$ git clone https://github.com/Awinja-j/ratestask.git`

cd into the created folder and install a virtual environment

`$ virtualenv venv`

Activate the virtual environment

`$ source venv/bin/activate`

Install all app requirements

`$ pip install -r requirements.txt`

Install environment variables

##### Use the sample .env file to fill in the environment variables required

`source .env`

All done! Now, start your server by running `python app.py`.

For best experience, use a GUI platform like postman to make requests to the api.



## Question 1:

Develop an HTTP-based API capable of handling the GET and POST requests described below in GET Request Task and POST Request Task. Our stack is based on Flask, but you are free to choose anything you like. All data returned is expected to be in JSON format. Please demonstrate your knowledge of SQL (as opposed to using ORM querying tools) in at least one part.

### GET Request Task

Part 1

Implement an API endpoint that takes the following parameters:

- date_from
- date_to
- origin
- destination

and returns a list with the average prices for each day on a route between port codes origin and destination.
Both the origin, destination params accept either port codes or region slugs, making it possible to query for average prices per day between geographic groups of ports.

Part 2

Make a second API endpoint return an empty value (JSON null) for days on which there are less than 3 prices in total.

### Endpoints

| Description                                                                                              | HTTP Method | URL     | Params                                                                             | Response w/o Payload | Response w/ Payload |
|----------------------------------------------------------------------------------------------------------|-------------|---------|------------------------------------------------------------------------------------|----------------------|---------------------|
| Returns a list with the average prices for each day on a route between port codes origin and destination | GET         | /rates  | date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main |                      |                     |
| Return an empty value (JSON null) for days on which there are less than 3 prices in total                | GET         | /rates_null | N/A                                                                                |                      |                     |
| health check                                                                                             | GET         | /       | N/A                                                                                |  {
  "heathcheck": "Everything is Fine, Houston"
}                    |                     |


https://github.com/Awinja-j/ratestask/blob/master/Screenshot%202020-09-21%20at%2005.33.53.png


### POST Request Task
Part 1
Implement an API endpoint where you can upload a price, including the following parameters:

- date_from
- date_to
- origin_code,
- destination_code
- price

Part 2

Extend that API endpoint so that it could accept prices in different currencies. Convert into USD before saving. https://openexchangerates.org/ provides a free API for retrieving currency exchange information.

### Endpoints

| Description    | HTTP Method | URL           | Params | Response w/o Payload | Response w/ Payload |
|----------------|-------------|---------------|--------|----------------------|---------------------|
| Upload a price | POST         | /rates |  date=2016-01-01&origin_code=china_east_main&destination_code=north_europe_main&price=2000      |                      |                     |


https://github.com/Awinja-j/ratestask/blob/master/Screenshot%202020-09-21%20at%2003.51.16.png


## Question 2:

Describe the system you would design for handling the Batch Processing Task.

Imagine you need to receive and update batches of tens of thousands of new prices, conforming to a similar format. Describe, using a couple of paragraphs, how you would design the system to be able to handle those requirements. Which factors do you need to take into consideration?