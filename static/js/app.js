document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const incidentInput = document.getElementById('incident-input');
    const loadingState = document.getElementById('loading-state');
    const resultsSection = document.getElementById('results-section');
    const analysisResult = document.getElementById('analysis-result');
    const matchBadge = document.getElementById('match-badge');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');

    const handleAnalyze = async () => {
        const text = incidentInput.value.trim();
        if (!text) {
            alert("Please provide incident details first.");
            return;
        }

        // UI Transition to Loading
        analyzeBtn.disabled = true;
        analyzeBtn.classList.add('opacity-50', 'cursor-not-allowed');
        loadingState.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ incident: text })
            });

            const result = await response.json();

            if (result.success) {
                // Render Markdown content
                analysisResult.innerHTML = marked.parse(result.data.analysis);
                
                // Update Badge
                const count = result.data.similar_incidents_count;
                matchBadge.textContent = count > 0 
                    ? `🔗 ${count} Vector Matches Found` 
                    : "⚡ Zero-Shot Expert Analysis";
                matchBadge.className = count > 0 
                    ? "px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold"
                    : "px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold";

                // Show Results
                resultsSection.classList.remove('hidden');
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            console.error("Analysis failed:", error);
            alert("Connection error: Ensure the Flask server is running.");
        } finally {
            loadingState.classList.add('hidden');
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    };

    analyzeBtn.addEventListener('click', handleAnalyze);
    
    newAnalysisBtn.addEventListener('click', () => {
        incidentInput.value = '';
        resultsSection.classList.add('hidden');
        incidentInput.focus();
    });

    // Ctrl+Enter support
    incidentInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleAnalyze();
        }
    });
});
