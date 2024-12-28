import os
import sqlite3
import datetime
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import analysis, google_search, login_required, apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure upload folder
app.config["UPLOAD_FOLDER"] = "temp_uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show history of searches"""
    user_id = session.get("user_id")
    con = sqlite3.connect("aps.db")
    cur = con.cursor()

    # Fetch the search history for the logged-in user
    rows = cur.execute(
        "SELECT id, search_time, search_term, keywords, result FROM history WHERE user_id = ? ORDER BY search_time DESC",
        (user_id,),
    ).fetchall()
    con.close()

    return render_template("index.html", history=rows)



@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search patent"""
    user_id = session.get('user_id')
    if not user_id:
        return apology("User not logged in")

    if request.method == "POST":
        # Get the search term
        term = request.form.get("keyword")
        
        # Get the uploaded file
        file = request.files.get("file")

        # Initiate search history
        search_term = None
        keywords = None
        total_result = 0
        
        if not term and not file:
            return apology("Please input keyword or upload file")
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            print(f"File saved to {file_path}")
            search_term = f"File: {filename}"
            keywords = analysis(file_path=file_path, term=None)  # analysis keywords
        elif term:
            search_term = term
            keywords = analysis(term=term, file_path=None) # analysis keywords

        if keywords:
            print(f"Analyzed keywords: {keywords}")

            total_result, organic_results, pagination = google_search(keywords) # use google patent search
        else:
            return apology("Failed to analyze keywords")
        
        if not organic_results:
            return apology("No result")
        else:
            search_time = datetime.datetime.now()
            con = sqlite3.connect("aps.db")
            cur = con.cursor()
            cur.execute(
                "INSERT INTO history (user_id, search_time, search_term, keywords, result) VALUES (?, ?, ?, ?, ?)",
                (user_id, search_time, search_term, keywords, total_result),
            )
            con.commit()
            con.close()

            return render_template("result.html", results=organic_results, pagination=pagination)
    return render_template("search.html")


@app.route("/redo_search/<int:history_id>")
@login_required
def redo_search(history_id):
    """Redo a previous search using saved keywords"""
    user_id = session.get("user_id")
    if not user_id:
        return apology("User not logged in")

    con = sqlite3.connect("aps.db")
    cur = con.cursor()
    cur.execute("SELECT keywords FROM history WHERE id = ? AND user_id = ?", (history_id, user_id))
    keywords = cur.fetchone()
    con.close()

    if not keywords:
        return apology("History not found")
    total_result, organic_results = google_search(keywords)

    if not organic_results:
        return apology("No result found during re-search")
    return render_template("result.html", results=organic_results)


@app.route("/delete/<int:history_id>")
@login_required
def delete(history_id):
    """Delete a previous search"""
    user_id = session.get("user_id")
    if not user_id:
        return apology("User not logged in")

    if history_id:
        con = sqlite3.connect("aps.db")
        cur = con.cursor()
        cur.execute("DELETE FROM history WHERE id = ? AND user_id = ?", (history_id, user_id))
        con.commit()
        print(f"Delete the row {history_id} from user {user_id}")
        con.close()

    else:
        return apology("Delete failed!")
    
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        con = sqlite3.connect("aps.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        rows = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            con.close()
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        con.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        else:
            # Query database for username
            con = sqlite3.connect("aps.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            rows = cur.execute("SELECT * FROM users WHERE username = ?",(request.form.get("username"),)).fetchall()
            
            if rows:  # If user already exists
                con.close()
                return apology("username already exists")
            else:
                username = request.form.get("username")
                hash = generate_password_hash(request.form.get("password"))

                # Insert the username and password to the database
                cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
                con.commit()

                # Query database for the new user's ID
                user_row = cur.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()

                # Remember which user has logged in
                session["user_id"] = user_row["id"]
            
            con.close()

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")