import sys
import os
from services.vector_db import VectorDBService
from services.llm import LLMService
from services.embedding import EmbeddingService

class IncidentCommander:
    """
    Core Application: Orchestrates the workflow from log ingestion to resolution.
    """
    
    def __init__(self):
        self.vdb = VectorDBService(bank_id="sre-incidents")
        self.llm = LLMService()
        self.embed = EmbeddingService()

    def handle_incident(self, raw_logs):
        """
        The full pipeline: Normalize -> Recall -> Analyze -> Resolve.
        """
        print("\n--- Incident Investigation Started ---")
        
        # 1. Normalize and summarize logs
        print("Normalizing logs...")
        query = self.embed.normalize_text(raw_logs)
        
        # 2. Recall similar historical incidents
        print("Recalling historical memory from Hindsight...")
        similar_cases = self.vdb.recall_similar(query)
        print(f"Found {len(similar_cases)} relevant past incidents.")
        
        # 3. Analyze with LLM + Grounding context
        print("Generating resolution plan using Groq...")
        recovery_plan = self.llm.analyze_incident(raw_logs, similar_cases)
        
        print("\n--- Recovery Plan Generated ---\n")
        print(recovery_plan)
        
        return recovery_plan

def main():
    commander = IncidentCommander()
    
    print("SRE Commander | Vectorized Incident Response Agent")
    print("Type your incident logs/description below (or 'exit' to quit):")
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'exit':
                break
            
            if not user_input.strip():
                continue
                
            commander.handle_incident(user_input)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
