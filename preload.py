import json
import os
import sys
from app.services.vector_db import VectorDBService

def preload_knowledge_base():
    """
    Iterates through incidents.json and ingests them into the Hindsight Memory Bank.
    """
    print("--- Initializing Knowledge Ingestion ---")
    
    # Ensure we can find the data file
    data_path = os.path.join("app", "data", "incidents.json")
    if not os.path.exists(data_path):
        print(f"Error: Could not find {data_path}")
        return

    try:
        with open(data_path, "r") as f:
            incidents = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {str(e)}")
        return

    vdb = VectorDBService(bank_id="sre-incidents")
    
    count = 0
    for inc in incidents:
        print(f"Indexing: {inc.get('issue', 'Unknown Incident')[:50]}...")
        success = vdb.retain_incident(inc)
        if success:
            count += 1
            print("Retained.")
        else:
            print("Failed to retain (check connection).")

    print(f"\nIngestion Complete! {count}/{len(incidents)} incidents indexed.")

if __name__ == "__main__":
    preload_knowledge_base()
