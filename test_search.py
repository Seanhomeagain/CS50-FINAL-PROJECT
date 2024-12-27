from helpers import google_search

if __name__ == "__main__":
    keywords = "test search"
    total_results, organic_results, pagination = google_search(keywords, start=0)
    print(f"Total Results: {total_results}")
    print(f"Organic Results: {len(organic_results)}")
    print(f"Pagination: {pagination}")

    # <a href="{{ url_for('save', patent_id=result.patent_id) }}" class="btn btn-primary">Save</a>