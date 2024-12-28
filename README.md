# AI Patent Search
#### Video Demo:  <URL HERE>
#### Description:

This is a Flask-based web application that allows users to search for patents by putting some description or by uploading files. It uses AI to extract technical keywords and integrates with Google Patents to fetch search results. The application also includes a history feature to track previous searches and view the search results again.

---

## Features

- **Search Patents**  
  - Enter keywords or upload a file to analyze technical keywords for patent searches.
  - Fetch results from Google Patents using SerpAPI.

- **AI Keyword Extraction**  
  - Automatically analyzes uploaded files or search terms to generate relevant technical keywords.

- **Search History**  
  - Tracks all user searches, including:
    - Search number
    - Time of search
    - Search term (keywords or file name)
    - Extracted AI keywords
    - Total number of results
  - Includes a "View" button to revisit search results.

- **Pagination**  
  - Supports navigating through multiple pages of search results.

---

## Prerequisites

- **Python**: Version 3.8 or higher
- **Flask**: A Python web framework
- **SQLite**: A lightweight database
- **SerpAPI**: Used for fetching Google Patents data
- **GenAI API**: Used for AI-powered keyword extraction

---

## Installation

1. Clone the repository:  
   ```bash
   git clone <repository-url>
   cd <repository-folder>

