import os
import requests
import re, json, html2text

COURT_LISTENER_MAX_RESULTS=4 # Adjust based on the model used for inference.
COURT_LISTENER_API_URL="https://www.courtlistener.com/api/rest/v3/"
COURT_LISTENER_BASE_URL="https://www.courtlistener.com"

class SearchCourtRecord():

    RESULTS_DATA_FORMAT = {
        "id": "",
        "case_name": "",
        "court": "",
        "absolute_url": "",
        "status": "",
        "date_filed": "",
        "text": "",  # Full opinion text
        "prompt_text": "",  # Line of text used as part of the RAG prompt to introduce sources.
        "ui_text": "",  # Line of text used as part of the UI to introduce this source.
        "ui_url": "",  # URL used to let users explore this source.
    }
    """
    Shape of the data for each individual entry of search_results.
    """
    @staticmethod
    def search_court_record(search_string: str):
        api_url = COURT_LISTENER_API_URL
        base_url = COURT_LISTENER_BASE_URL
        max_results = COURT_LISTENER_MAX_RESULTS

        results = []
        output = {}

        from_date = None
        to_date = None

        """
        Santize search string
        """
        if "dateFiled" in search_statement:
            from_date_r = r"dateFiled\:\[([0-9]{4}-[0-9]{2}-[0-9]{2}) TO"

            to_date_r = (
                r"dateFiled\:\[[0-9]{4}-[0-9]{2}-[0-9]{2} TO ([0-9]{4}-[0-9]{2}-[0-9]{2})\]"
            )
            try:
                from_date = re.findall(from_date_r, search_statement)[0]
                from_date = from_date.replace("-", "/")

                to_date = re.findall(to_date_r, search_statement)[0]
                to_date = to_date.replace("-", "/")
            except Exception:
                pass

        print(f"date range: {from_date} to {to_date}")

        search_url = (
            f"{api_url}search?q={search_statement}"
            f"&fromDate={from_date}"
            f"&toDate={to_date}"
            f"&sort=dateFiled"
        )
        print(f"search url: {search_url}")

        results = requests.get(f"{api_url}/search/",
            params ={
                "type": "o",
                "q": search_string,
                "order": "score desc",
                "filed_after": from_date,
                "filed_before": to_date,
            },
            timeout=10,
        ).json()

        print(f"search results: {results}")

        for i in range(0, max_results):

            record = dict(RESULTS_DATA_FORMAT)
            row = results["results"][i]

            record["id"] = row["id"]
            record["case_name"] = row["case_name"]
            record["court"] = row["court"]
            record["absolute_url"] = f"{base_url}{row['absolute_url']}"
            record["status"] = row["status"]
            record["date_filed"] = row["date_filed"]
            
            # Get detailed opnion
            try:
                opinion = requests.get(f"{api_url}/opinions/",
                    timeout=10,
                    params={
                        "id": record["id"]
                    },
                ).json()

                opinion = opinion["results"][0]
                opinion["text"] = html2text.html2text(opinion["html"]

            except Exception as e:
                print(f"Error getting opinion: {str(e)}")
            continue

            prompt_str = f"[{i+1}] {opinion["case_name"]} {opinion["date_filed"]} \
                {opinion["court"]} as assured from {opinion["absolute_url"]}"   
                             
            ui_text = f"[{i+1}] {opinion["case_name"]} {opinion["date_filed"]} \
                {opinion["court"]} as assured from {opinion["absolute_url"]}"   

            record["prompt_text"] = prompt_str
            record["ui_text"] = ui_text
            record["ui_url"] = opinion["absolute_url"]
            output.append(record)

        return output