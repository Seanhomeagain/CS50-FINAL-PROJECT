import requests

from flask import redirect, render_template, session
from functools import wraps
from dotenv import load_dotenv
from serpapi import GoogleSearch
import google.generativeai as genai
import os


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def analysis(file_path=None, term=None):
    try:
        # Load environment variables from .env file
        load_dotenv()
        genai.configure(api_key=os.environ["API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")

        if term:
            response = model.generate_content(["Give me one to three technical keywords, without explaining, without preamble, without warning.", term])
        elif file_path:
            # Upload the file to the API
            uploaded_file = genai.upload_file(file_path)
            response = model.generate_content(["Give me one to three technical keywords, without explaining, without preamble, without warning.", uploaded_file])

        keywords = response.text.strip()
        return(keywords)
    
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None
    

def search(keywords):
    try:
        params = {
        "engine": "google_patents",
        "q": keywords,
        "api_key": "ac046191ca23f702441997a3454b212c0d5077d79c75f3461793523ba72dc7be"
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # Extract total_results
        total_results = results["search_information"].get("total_results", 0)

        organic_results = results.get("organic_results", [])

        return(total_results, organic_results)
          
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code