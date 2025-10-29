# ALX Travel App

This is a Django-based application for managing travel listings and data.

## Key Features

* Property listings management
* Data seeding capabilities
* RESTful API endpoints (based on serializers and have been updated)
  * Listings: /api/listings/ (GET, POST, PUT, DELETE)
  * Bookings: /api/bookings/ (GET, POST, PUT, DELETE)

## Technology Stack

* Python 3.x
* Django framework
* Other dependencies as per requirements.txt

## Getting Started

1. Clone the repository
2. Install dependencies using `pip install -r requirements.txt`
3. Apply database migrations with `python manage.py migrate`
4. Run the development server with `python manage.py runserver`

## Usage/Examples

* Access the API at <http://localhost:8000/>
* Use the seed command to populate data: `python manage.py seed`
