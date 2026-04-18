from flask import Flask, render_template, request, jsonify
from services.vector_db import VectorDBService
from services.llm import LLMService
from services.embedding import EmbeddingService
import os

# Application Entry Point
app = Flask(__name__)

class IncidentCommander:
    def __init__(self):
        self.vdb = VectorDBService(bank_id="sre-incidents")
        self.llm = LLMService()
        self.embed = EmbeddingService()

    def analyze(self, raw_logs):
        query = self.embed.normalize_text(raw_logs)
        similar_cases = self.vdb.recall_similar(query)
        recovery_plan = self.llm.analyze_incident(raw_logs, similar_cases)
        
        return {
            "analysis": recovery_plan,
            "similar_incidents_count": len(similar_cases)
        }

commander = IncidentCommander()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'incident' not in data:
            return jsonify({"success": False, "error": "No incident data provided"}), 400
        
        result = commander.analyze(data['incident'])
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
