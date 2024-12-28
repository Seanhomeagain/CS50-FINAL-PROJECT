# AI Patent Search
#### Video Demo:  https://youtu.be/DQgnEHrdX6Q
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

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up environment variables:
   Create a .env file in the root directory and add the following:
   ```bash
   API_KEY=<your_genai_api_key>
   SERPAPI_KEY=<your_serpapi_api_key>
   UPLOAD_FOLDER=./temp_uploads

 4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
```
 5. Run the application:
   ```bash
   flask run
```

## File Structure

```bash
.
├── app.py                  # Main application file
├── helpers.py              # Utility functions (e.g., analysis, search)
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates (search.html, result.html, etc.)
├── temp_uploads/           # Temporary storage for uploaded files
├── aps.db                  # SQLite database file
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .env                    # Environment variables

```
## How to Use
Log in:
Access the app by logging into your account. If you’re not registered, create an account.

Perform a Search:

Enter a keyword or upload a file on the search page.
The AI will analyze your input and extract keywords.
View results directly.

Click the "Home" tab or the LOGO to view past searches.
Use the "View" button to revisit results or redo a search.
Use the "Delete" button to delete a search result.

## Disclaimer
This project is intended solely for research and learning purposes. It is not designed for commercial use.

Ensure that your use of the application complies with applicable laws and regulations.
Protect your personal data and privacy when using this application, especially when uploading files or performing online searches.
The authors are not responsible for any misuse of this tool or any consequences arising from its use.

## Future Improvements
Add advanced search filters (e.g., by date, patent type, or region).
Implement user-friendly error handling and feedback.
Support other languages for search terms and results.
Provide detailed analysis of patents (e.g., assignees, inventors, classifications).

## Acknowledgments
Flask for the web framework
SerpAPI for Google Patents integration
GenAI for AI-powered keyword extraction
Bootstrap for front-end styling

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or feedback, feel free to reach out to:

Author: Xin Wang
Email: seansoochow@gmail.com


