# Beyond Horizons: A WEB APP TO TRACK NEAR EARTH OBJECTS

## Video Demo:  <URL HERE>

## Description:

My project for CS50 Introduction to Computer Science is a web app to track near earth objects based on the dates that the users enter

### Routes with Templates:
##### Layout.html:
This the base template for the webb app front end, using bootstrap for styling, a navbar at the top has been added with Logo in the left corner.
The design is kept simple and very intuitive  
The web app has routes listed below
####  /register: 

git config --global user.name "Abu-bakkar-siddique"
Register() function is called on making http request to the /register route, a register.html is rendered as a result for a GET request, asking users for their credentials for registration, all  the corner cases such as re-registering the same user have been checked here.

#### /login:
This route is for login built on the same pattern as the registration page ensuring intuitive navigation and consistent design,
on http request to this route login.html is rendered asking for the email and password from the users, if the users meet all the cases to login, ie correct email and password, they are redirected to the homeoage route ("/astroids")

#### /astroids:
This is the home route where the actual functionality is implemented, astroids.html is rendered on GET http request, it asks the user for a start date end date to search for the NEOs(near earth objects) the dates are then passed to the api requests date paramters to render the data of the NEOs.

### Functions:

#### login:

The Login function logs in the users if they are already registered.It clears the existing session and checks the submitted email and password for validity. If the credentials are correct, the user is redirected to the home page, else, appropriate error messages are displayed.

#### register:

Handles user registration functionality. Validates the submitted email and password, checks for existing email addresses, and registers the user if all conditions are met. Redirects to the home page on successful registration.

####astroids

This function handles the main functionality of the project. On a POST request, it retrieves and validates start and end dates, queries asteroid from NASA api withen a specified range the data rendered is displayed on astroids.html template. Function handles corner cases such as date validity and date range.

### Helper Functions:
#### validate_email:
This function uses regular erpression to validate the user's email address.
the function takes an email that the user has entered and returns a boolean for valid or invalid 
which is in turn used tp display appropriate error messages.
Returns:

#### authenticate:

This is a decorator function that ensures that a user is logged in before accessing a route. If the user is not logged in it redirects the users to the login page.

#### extract_neo_info:
Extracts relevant information from a Near-Earth Object (NEO) dataset.
neo_data (list of dicts): List containing NEO data with key-value pairs.
A formatted list or dictionary with relevant NEO information.

#### get_neo:
This function takes two parameters start_date and end date and passes these dates to nasa's api to queries and retrieves NEO data within a date range.
It returns dictionaries containing NEO information within the specified date range.