# ecoenergy-agent
AI-powered assistant for purchasing renewable energy certificates.
# EcoEnergy Agent

**AI-powered assistant for purchasing renewable energy certificates.**

## Overview
EcoEnergy Agent is an intelligent agentic AI tool that automates the entire process of purchasing renewable energy certificates (EKOenergy, I-REC, GOO, etc.) for companies, SMEs, and individuals.  
It gathers the user’s energy needs and budget, searches global providers, compares prices and sustainability standards, and presents the best options.  
Upon approval, it initiates the purchase, securely stores the certificates, and sends renewal reminders.

## Key Features
- **Automated Research**: Finds and compares renewable energy certificate providers worldwide.
- **Sustainability Scoring**: Evaluates providers based on ESG and environmental impact.
- **Seamless Purchase Flow**: Initiates and manages certificate purchases with minimal user input.
- **Renewal Management**: Tracks expiration dates and sends proactive reminders.

## Why It Matters
EcoEnergy Agent simplifies and accelerates access to green energy, helping organizations achieve sustainability goals faster and more efficiently.

## Tech Stack (Planned)
- **Frontend**: React / Next.js
- **Backend**: Python (FastAPI or Flask)
- **AI Layer**: LLM-based decision making & RPA for automation
- **Database**: PostgreSQL or MongoDB

## License
MIT License


ecoenergy-agent/
│
├─ app.py
├─ mock_data.json
├─ requirements.txt
└─ templates/
    └─ index.html

[
  {
    "provider": "EKOenergy",
    "type": "Solar",
    "price_per_mwh": 50,
    "esg_score": 95
  },
  {
    "provider": "I-REC",
    "type": "Wind",
    "price_per_mwh": 45,
    "esg_score": 90
  },
  {
    "provider": "GOO",
    "type": "Hydro",
    "price_per_mwh": 40,
    "esg_score": 85
  }
]

from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Mock veri yükle
with open('mock_data.json', 'r') as f:
    providers = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    energy_need = float(request.form.get('energy'))
    budget = float(request.form.get('budget'))

    # Basit puanlama algoritması: fiyat + esg skoruna göre seçim
    scored = []
    for p in providers:
        score = p['esg_score'] - p['price_per_mwh']
        if p['price_per_mwh'] * energy_need <= budget:
            scored.append({**p, 'score': score})

    # Skora göre sırala ve en iyi 2 sonucu al
    top = sorted(scored, key=lambda x: x['score'], reverse=True)[:2]
    return jsonify(top)

if __name__ == '__main__':
    app.run(debug=True)

<!DOCTYPE html>
<html>
<head>
    <title>EcoEnergy Agent Demo</title>
</head>
<body>
    <h1>EcoEnergy Agent</h1>
    <form id="form">
        <label>Energy Need (MWh/year):</label>
        <input type="number" name="energy" required><br><br>

        <label>Budget (€):</label>
        <input type="number" name="budget" required><br><br>

        <button type="submit">Get Recommendations</button>
    </form>

    <h2>Top Recommendations:</h2>
    <ul id="results"></ul>

    <script>
        const form = document.getElementById('form');
        const results = document.getElementById('results');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            results.innerHTML = '';
            const formData = new FormData(form);
            const response = await fetch('/recommend', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.provider} - ${item.type} - €${item.price_per_mwh}/MWh - ESG: ${item.esg_score}`;
                results.appendChild(li);
            });
        });
    </script>
</body>
</html>


Flask==2.3.2




