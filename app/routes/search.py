from flask import current_app, jsonify, request, Blueprint
from app.services.search_court_rec import SearchCourtRecord

sr = Blueprint("search", __name__)

@sr.route("/search", methods=["POST"])
def search_court_record():
    """
    aggregate_search results: court_records + other sources
    Search for a message in the index.
    [POST] /search
    
    Request Body:
    {
        "search_string" (str): The string to search for.
        "search_format" (str): Format of the search string [Text | Prompt | URL].
    }
    
    Response:
    {
        "{search_string}": [.. results ..]
    }
    """

    input_data = request.get_json()
    print(f"Input data: {input_data}",  input_data)
    search_str = ""
    search_fmt = ""

    if "search_string" not in input_data:
        return jsonify(error="Missing required argument: search_string"), 400
    
    # if "search_tool" not in input_data:
    #     return jsonify(error="Missing required argument: search_tool"), 400

    search_str = str(input_data["search_string"]).strip()
    search_fmt = str(input_data["search_format"]).strip()

    print(f"search: {search_str}, format: {search_fmt}")
    try:
        scr = SearchCourtRecord()
        rsrch = scr.search_cases(search_str)

        print(f"search results: {rsrch}")

    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(data=rsrch), 200