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

    # Basit puanlama algoritması: fiyat + ESG skoruna göre seçim
    scored = []
    for p in providers:
        score = p['esg_score'] - p['price_per_mwh']
        if p['price_per_mwh'] * energy_need <= budget:
            scored.append({**p, 'score': score})

    # Skora göre sırala ve en iyi 2 sonucu al
    top = sorted(scored, key=lambda x: x['score'], reverse=True)[:2]
    return jsonify(top)

if __name__ == '__main__':
    print("EcoEnergy Agent is running...")
    app.run(debug=True)
