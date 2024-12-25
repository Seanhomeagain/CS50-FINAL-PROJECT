from serpapi import GoogleSearch

# Parameters for the query
params = {
    "engine": "google_patents",  # Specify the search engine
    "q": ["pump", "valve"],  # List of queries (each will become a separate "q" entry)
    "assignee": "Grundfos Holding As",
    "before": "priority:20211112",
    "after": "priority:20180101",
    "num": 100,  # Number of results
    "sort": "new",  # Sorting order
    "api_key": "ac046191ca23f702441997a3454b212c0d5077d79c75f3461793523ba72dc7be"
}

# Format multiple "q" entries for the query
query = "&".join([f"q={entry.replace(' ', '+')}" for entry in params.pop("q")])

# Construct the final parameters with the formatted query string
formatted_params = f"{query}&assignee={params['assignee'].replace(' ', '+')}&before={params['before']}&after={params['after']}&num={params['num']}&sort={params['sort']}"

# Perform the search
search = GoogleSearch({
    "engine": "google_patents",
    "q": formatted_params,
    "api_key": params["api_key"]
})
results = search.get_dict()
organic_results = results.get("organic_results", [])