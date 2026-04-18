import os
from groq import Groq
from app.config import GROQ_API_KEY

class LLMService:
    """
    Intelligence Layer: Handles advanced incident analysis and resolution path generation.
    Uses Groq for ultra-fast response times.
    """
    
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "mixtral-8x7b-32768"

    def analyze_incident(self, current_incident, similar_incidents):
        """
        Generates a targeted resolution plan by combining current logs with historical grounding.
        """
        context = ""
        if similar_incidents:
            context = "\n### Historical Context (Past Similar Incidents):\n"
            for i, inc in enumerate(similar_incidents):
                context += f"{i+1}. Issue: {inc.get('issue')}\n   Root Cause: {inc.get('root_cause')}\n   Resolution: {inc.get('resolution')}\n\n"

        prompt = f"""
        You are an Expert SRE Incident Commander. Analyze the following incident and provide a recovery plan.
        
        {context}
        
        ### Current Incident:
        {current_incident}
        
        ### Instructions:
        1. Identify the likely Root Cause.
        2. Provide Immediate Actions.
        3. Recommend a Long-term Resolution.
        4. (Optional) Provide a confidence level based on historical context.
        
        Output in professional markdown format.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error in LLM analysis: {str(e)}"
