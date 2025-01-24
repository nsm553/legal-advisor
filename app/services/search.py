import os
import traceback

from flask import current_app, jsonify, request
from ollama import Client
from app.services.search_court_rec import SearchCourtRecord

@current_app.route("/search", methods=["POST"])
def search():

    """
     aggregate_search results: court_records + other sources
    """
    results = f"{search_court_record()}"

    return jsonify(results)


def search_court_record():
    """
    Search for a message in the index.
    [POST] /search
    
    Request Body:
    {
        "search_string" (str): The string to search for.
        "search_tool" (str): The search tool to use.
    }
    
    Response:
    {
        "{search_string}": [.. results ..]
    }
    """
    input_data = request.get_json()
    print(f"Input data: {input_data}",  input_data)
    research = ""
    tool = ""

    if "search_string" not in input_data:
        return jsonify(error="Missing required parameter: search_string"), 400
    
    if "search_tool" not in input_data:
        return jsonify(error="Missing required parameter: search_tool"), 400

    research = str(input_data["search_string"]).strip()
    tool = str(input_data["search_tool"]).strip()

    try:
        rsrch = SearchCourtRecord.search_court_record(research)

        print(f"search results: {rsrch}")

    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(data=rsrch), 200