import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import validate_email, authenticate, extract_neo_info, get_neo
#configuring application
app = Flask(__name__)

#Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///db.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in"""

    #Forget any user_id
    session.clear()
    error = None

    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            #flash message
            error = "Enter your email"
            return render_template("login.html", error = error)

        # Ensure password was submitted
        elif not request.form.get("password"):

            #flash message
            #return redirect("/login")
            error = "Enter a valid password"
            #return Error ("Enter a password")
            return render_template("login.html", error = error)

        elif not validate_email(request.form.get("email")):
            error = "Enter a valid email address"
            return render_template("login.html", error = error)
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            #flash message
            error = "Fill in the credentials"
            return render_template("login.html", error = error)
    
        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]

        # Redirect user to home page
        return redirect("/")

        #User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register",  methods = ["GET", "POST"])
def register():
    error = None
    """Register user"""
    if request.method == "POST":
    
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not email or not password or not confirmation :
            error = "All fields are required"
            return render_template("register.html", error = error) 

        check_email = db.execute("SELECT email FROM users WHERE email = ? ", email)

        if not email:
            error = "Enter a email"
            return render_template("register.html", error = error)            
        elif len(check_email) == 1 :
            error = "Email is already registered"
            return render_template("register.html", error = error)
                        
        elif password != confirmation:
            error = "password and confirmation donot match"
            return render_template("register.html", error = error)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (email, hash) VALUES (?, ?)", email, hash)
        return redirect("/")
    
    return render_template("register.html", message = "signed up successful")


@app.route("/", methods = ["GET", "POST"])
@authenticate
def astroids():
   
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        current_date = datetime.now()
        # Date format validation
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        except ValueError:
            error = "Invalid date format. Please use YYYY-MM-DD."
            return render_template("astroids.html", error=error)
        
        difference = (end_date - start_date).days
        # Date range validation
        if start_date < datetime(2020, 1, 1) or end_date > current_date:
            error = "Date should be after 2020-01-01 and before the current date."
            return render_template("astroids.html", error=error)

        elif difference <= 0 :

            error = "start date should be before the ending date."
            return render_template("astroids.html", error = error)
        elif difference > 5:
            error = "dates cannot be more then 5 days apart"
            return render_template("astroids.html", error = error)
        
        data = get_neo(start_date,end_date)   # A list of dicts, key value pairs
        return render_template("astroids.html", data = data)     

    # Handle the c se when the request method is not POST
    return render_template("astroids.html")

    
if __name__ == "__main__":
    app.run(debug=True)