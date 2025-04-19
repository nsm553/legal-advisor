import os
import requests
from typing import Dict, List, Optional
from datetime import datetime
import html2text
from dataclasses import dataclass
from urllib.parse import urljoin
@dataclass
class CourtListenerConfig:
    """Configuration for Court Listener API"""
    API_BASE_URL: str = "https://www.courtlistener.com/api/rest/v4"
    MAX_RESULTS: int = 10
    API_TOKEN: str = os.getenv("COURT_LISTENER_TOKEN", "")

@dataclass
class SearchResult:
    """Data structure for search results based on v4 API"""
    id: str
    case_name: str
    court_id: str
    court_name: str
    absolute_url: str
    precedential_status: str
    date_filed: str
    docket_id: int = 0
    docket_number: str = ""
    citation_count: int = 0
    text: str = ""
    opinion_data: Dict = None
    docket_data: Dict = None
    cluster_id: str = ""
    combined_opinion: str = ""

class SearchCourtRecord:
    def __init__(self, config: CourtListenerConfig = None):
        self.config = config or CourtListenerConfig()
        self.session = requests.Session()
        if self.config.API_TOKEN:
            self.session.headers.update({
                "Authorization": f"Token {self.config.API_TOKEN}"
            })

    def search_cases(self, query: str, 
                    date_start: Optional[str] = None, 
                    date_end: Optional[str] = None) -> List[SearchResult]:
        """
        Search for cases matching the query using v4 API
        
        Args:
            query: Search query string
            date_start: Start date in YYYY-MM-DD format
            date_end: End date in YYYY-MM-DD format
            
        Returns:
            List of SearchResult objects
        """
        params = {
            "q": query,
            "type": "o",  # Search for opinions
            "order_by": "score desc",
            "format": "json"
        }
        
        if date_start:
            params["filed_after"] = date_start
        if date_end:
            params["filed_before"] = date_end

        results = []
        try:
            print(f"URL -- {self.config.API_BASE_URL}/search/{params}")
            response = self.session.get(
                f"{self.config.API_BASE_URL}/search/",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            for item in data.get("results", [])[:self.config.MAX_RESULTS]:
                # Extract cluster ID from the opinion URL if available
                cluster_id = ""
                if "cluster" in item:
                    cluster_url = item["cluster"]
                    cluster_parts = cluster_url.split("/")
                    if len(cluster_parts) > 2:
                        cluster_id = cluster_parts[-2]

                result = SearchResult(
                    id=str(item.get("id", "")),
                    case_name=item.get("caseName", ""),
                    court_id=str(item.get("court_id", "")),
                    court_name=str(item.get("court", "")),
                    absolute_url=item.get("absolute_url", ""),
                    precedential_status=item.get("precedentialStatus", ""),
                    date_filed=item.get("dateFiled", ""),
                    docket_id=item.get("docket_id", 0),
                    docket_number=item.get("docketNumber", ""),
                    citation_count=item.get("citationCount", 0),
                    cluster_id=cluster_id,
                    combined_opinion=html2text.html2text(item['opinions'][0]['snippet'], "")
                )
                
                # Fetch additional details
                if cluster_id:
                    result.opinion_data = self._fetch_opinion_cluster(cluster_id)

                result.docket_data = self._fetch_docket(result.docket_id)
                                
                results.append(result)

        except requests.RequestException as e:
            print(f"Error searching Court Listener: {str(e)}")
            return []

        return results

    def _fetch_opinion_cluster(self, cluster_id: str) -> Dict:
        """Fetch detailed opinion cluster data"""
        try:
            response = self.session.get(
                f"{self.config.API_BASE_URL}/clusters/{cluster_id}/",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching opinion cluster {cluster_id}: {str(e)}")
            return {}

    def _fetch_docket(self, docket_id: str) -> Dict:
        """Fetch detailed docket data"""
        try:
            response = self.session.get(
                f"{self.config.API_BASE_URL}/dockets/{docket_id}/",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching docket {docket_id}: {str(e)}")
            return {}

def main():
    # Example usage
    config = CourtListenerConfig(
        MAX_RESULTS=5  # Limit results for demonstration
    )
    
    api = SearchCourtRecord(config)
    
    # Example search with date range
    results = api.search_cases(
        query="patent infringement",
        date_start="2023-01-01",
        date_end="2024-03-31"
    )
    
    # Print results
    for idx, result in enumerate(results, 1):
        print(f"\nResult {idx}:")
        print(f"Case: {result.case_name}")
        print(f"Court: {result.court_name}")
        print(f"Date Filed: {result.date_filed}")
        print(f"URL: {result.absolute_url}")
        print(f"Docket Number: {result.docket_number}")
        print(f"Citation Count: {result.citation_count}")
        print(f"Precedential Status: {result.precedential_status}")
        print(f"Combined Opinions: {result.combined_opinion}")      
        # print(f"Docket Data: {result.docket_data}")  
        print("-" * 50)
        if result.text:
            print(f"Opinion excerpt: {result.text[:200]}...")
        print("=" * 80)

# Make sure to export the class
__all__ = ['SearchCourtRecord', 'CourtListenerConfig', 'SearchResult']

if __name__ == "__main__":
    main()