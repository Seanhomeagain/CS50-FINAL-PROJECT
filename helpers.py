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
            response = model.generate_content(["Give me one to three technical keywords of the sentence, if it's one or two words, give me the word.", term])
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
    

def google_search(keywords):
    try:
        load_dotenv()
        serpapi_key=os.environ["SERPAPI_KEY"]
        params = {
        "engine": "google_patents",
        "q": keywords,
        "num": 100,
        "api_key": serpapi_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # Extract total_results
        total_results = results.get("search_information", {}).get("total_results", 0)
        organic_results = results.get("organic_results", [])

        return total_results, organic_results
          
    except Exception as e:
        print(f"Error in search: {e}")
        return None, None



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