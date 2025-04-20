from flask import current_app, jsonify, request, Blueprint
from app.services.search_court_rec import SearchCourtRecord
import json

sr = Blueprint("search", __name__)

@sr.route("/search", methods=["POST"])
def search_court_record():
    """
    aggregate_search results: court_records + other sources
    Search for a message in the index.
    [POST] /search
    
    Request Body:
    {
        "message" (str): The text to search for.
        "search_format" (str): Format of the search string [Text | Prompt | URL].
    }
    
    Response:
    {
        "{message}": [.. results ..]
    }
    """

    input_data = request.get_json()
    print(f"Input data: {input_data}",  input_data)
    message = ""
    search_fmt = ""

    if "message" not in input_data:
        return jsonify(error="Missing required argument: message"), 400
    
    # if "search_tool" not in input_data:
    #     return jsonify(error="Missing required argument: search_tool"), 400

    # message = str(input_data["message"]).strip()
    # search_fmt = str(input_data["search_format"])
    message = input_data.get('message')
    history = input_data.get('history', [])

    print(f"search: {message}, format: {search_fmt}")
    try:
        scr = SearchCourtRecord()
        result = scr.search_cases(message)
        # result = '[{"name": "legal", "type": "advisor"}]'
        # result = [{"id": "", "case_name": "Omega Patents, LLC v. Calamp Corp.", "court_id": "cafc", "court_name": "Court of Appeals for the Federal Circuit", "absolute_url": "/opinion/5093381/omega-patents-llc-v-calamp-corp/", "precedential_status": "", "date_filed": "2021-09-14", "docket_id": 60382294, "docket_number": "20-1793", "citation_count": 0, "text": "", "opinion_data": null, "docket_data": null, "cluster_id": "", "combined_opinion": "Case: 20-1793 Document: 44 Page: 1 Filed: 09/14/2021 United States Court of\nAppeals for the Federal Circuit ______________________ OMEGA PATENTS, LLC,\nPlaintiff-Cross-Appellant v. CALAMP CORP., Defendant-Appellant\n______________________ 2020-1793, 2020-1794 ______________________ Appeals\nfrom\n\n"},{"id": "", "case_name": "Shea v. Patents", "court_id": "scotus", "court_name": "Supreme Court of the United States", "absolute_url": "/opinion/8414325/shea-v-patents/", "precedential_status": "", "date_filed": "2014-01-13", "docket_id": 65610089, "docket_number": "No. 13\u20137268.", "citation_count": 0, "text": "", "opinion_data": null, "docket_data": null, "cluster_id": "", "combined_opinion": "Case below, 508 Fed.Appx. 668.Petition for writ of certiorari to the United\nStates Court of Appeals for the Ninth Circuit denied.\n\n"}]
        # result = [{"id": "a1", "case_name": "ca001", "court": "cas", "absolute_url": "", "status": "compl", "date_filed": "2025-01-01", "docket_number": "d001", "text": "", "opinion_data": "", "docket_data": ""}, {"id": "a2", "case_name": "NY001", "court": "nys", "absolute_url": "", "status": "aaa", "date_filed": "2025-01-22", "docket_number": "d202", "text": "", "opinion_data": "", "docket_data": ""}]
        print(f"search results: {jsonify(result)}")

    except Exception as e:
        return jsonify(error=str(e)), 500

    # return jsonify(data=json.dumps(result)), 200
    return jsonify(result), 200