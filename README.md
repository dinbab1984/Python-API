# Python-API

# Demo API developed by using FastAPI

#### This API consists of  3 routes such as Users, Login and Customers

1. Users: http://localhost:8000/users - to create, list and update, delete users
2. Login: http://localhost:8000/login - to login as a user
3. Customers : http://localhost:8000/customers - to create , list , update , delete customers ( only works if logged in as a user)

# You can easily run this locally on your local docker engine, please follow the steps below:

1. Clone this repository locally
2. Install docker locally
3. Start docker engine locally
4. Go to the cloned repository directory i.e. Python-API
5. Run docker build as follows : ````docker build -t python-api .````
6. Run container as follows: ````docker-compose -f docker-compose.yml up````
7. Test the routes using POSTMAN tool or other equivalent tools.
8. Please refer the automatic API documentation in the URL: http://localhost:8000/docs
9. Stop and remove container as follows: ````docker-compose -f docker-compose.yml down -v````



