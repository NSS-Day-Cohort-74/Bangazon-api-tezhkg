#!/bin/bash

rm -rf bangazonapi/migrations
rm db.sqlite3
python3 manage.py makemigrations bangazonapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata customers
python3 manage.py loaddata product_category
python3 manage.py loaddata product
python3 manage.py loaddata productrating
python3 manage.py loaddata payment
python3 manage.py loaddata order
python3 manage.py loaddata order_product
python3 manage.py loaddata favoritesellers
