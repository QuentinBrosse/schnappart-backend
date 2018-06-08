#!/usr/bin/env bash

echo "Seting up database..."
django-admin localdb
sleep 3
echo "Apply migrations..."
django-admin migrate
echo "Load data..."
django-admin loaddata data/users.json
django-admin loaddata data/api.Project.json
django-admin loaddata data/api.ImmoSource.json
django-admin loaddata data/api.Search.json

echo "###########################"
echo " "
echo "ConsultPanel Demo Account: "
echo "Username: Quentin"
echo "Password: 123Soleil!"
