from hindsight_client import Hindsight
from app.config import HINDSIGHT_URL, VECTORIZE_API_KEY

class VectorDBService:
    """
    Memory Layer: Manages persistence and retrieval of historical incidents.
    Powered by Hindsight (Vectorize.io) for semantic, graph, and keyword search.
    """
    
    def __init__(self, bank_id="sre-incidents"):
        self.client = Hindsight(base_url=HINDSIGHT_URL, api_key=VECTORIZE_API_KEY)
        self.bank_id = bank_id

    def retain_incident(self, incident_data):
        """
        Stores an incident in the memory bank.
        incident_data should be a string describing the incident or a dict.
        """
        if isinstance(incident_data, dict):
            content = f"Issue: {incident_data.get('issue')}\nRoot Cause: {incident_data.get('root_cause')}\nResolution: {incident_data.get('resolution')}"
        else:
            content = incident_data
            
        try:
            return self.client.retain(bank_id=self.bank_id, content=content)
        except Exception as e:
            print(f"Error retaining memory: {str(e)}")
            return None

    def recall_similar(self, query, top_n=3):
        """
        Recalls the most relevant past incidents based on a query.
        """
        try:
            results = self.client.recall(bank_id=self.bank_id, query=query)
            # Hindsight recall returns a list of results with content and relevance
            # We normalize this for the LLMService
            parsed_results = []
            for item in results[:top_n]:
                # In a real scenario, you might parse the retained string back into components
                parsed_results.append({
                    "issue": item.get("content", ""),
                    "relevance": item.get("relevance", 0)
                })
            return parsed_results
        except Exception as e:
            print(f"Error recalling memory: {str(e)}")
            return []
