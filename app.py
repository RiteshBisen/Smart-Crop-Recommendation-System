from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def predict_crop(features):
    """
    Rule-based crop prediction using agricultural science principles
    Returns: (crop_name, confidence_percentage)
    """
    n, p, k, temp, humidity, ph, rainfall = features
    crop_scores = {}
    
    # Rice: High N, moderate P&K, warm temp, high humidity, slightly acidic pH, high rainfall
    rice_score = 0
    if 80 <= n <= 120: rice_score += 20
    elif 60 <= n <= 140: rice_score += 15
    else: rice_score += 5
    
    if 40 <= p <= 60: rice_score += 15
    elif 30 <= p <= 80: rice_score += 10
    else: rice_score += 3
    
    if 40 <= k <= 50: rice_score += 15
    elif 30 <= k <= 70: rice_score += 10
    else: rice_score += 3
    
    if 20 <= temp <= 27: rice_score += 20
    elif 18 <= temp <= 30: rice_score += 15
    else: rice_score += 5
    
    if humidity >= 80: rice_score += 20
    elif humidity >= 70: rice_score += 15
    else: rice_score += 5
    
    if 5.5 <= ph <= 7.0: rice_score += 15
    elif 5.0 <= ph <= 7.5: rice_score += 10
    else: rice_score += 3
    
    if rainfall >= 200: rice_score += 15
    elif rainfall >= 150: rice_score += 10
    else: rice_score += 3
    
    crop_scores['Rice'] = min(rice_score, 100)
    
    # Wheat: Moderate N, P, K, cool temp, moderate humidity, neutral pH, moderate rainfall
    wheat_score = 0
    if 50 <= n <= 80: wheat_score += 20
    elif 30 <= n <= 100: wheat_score += 15
    else: wheat_score += 5
    
    if 40 <= p <= 70: wheat_score += 15
    elif 20 <= p <= 90: wheat_score += 10
    else: wheat_score += 3
    
    if 20 <= k <= 40: wheat_score += 15
    elif 10 <= k <= 60: wheat_score += 10
    else: wheat_score += 3
    
    if 15 <= temp <= 25: wheat_score += 20
    elif 12 <= temp <= 28: wheat_score += 15
    else: wheat_score += 5
    
    if 50 <= humidity <= 70: wheat_score += 20
    elif 40 <= humidity <= 80: wheat_score += 15
    else: wheat_score += 5
    
    if 6.0 <= ph <= 7.5: wheat_score += 15
    elif 5.5 <= ph <= 8.0: wheat_score += 10
    else: wheat_score += 3
    
    if 50 <= rainfall <= 100: wheat_score += 15
    elif 30 <= rainfall <= 120: wheat_score += 10
    else: wheat_score += 3
    
    crop_scores['Wheat'] = min(wheat_score, 100)
    
    # Cotton: High N, high P&K, hot temp, moderate humidity, slightly alkaline pH
    cotton_score = 0
    if 100 <= n <= 140: cotton_score += 20
    elif 80 <= n <= 145: cotton_score += 15
    else: cotton_score += 5
    
    if 60 <= p <= 80: cotton_score += 15
    elif 40 <= p <= 100: cotton_score += 10
    else: cotton_score += 3
    
    if 40 <= k <= 60: cotton_score += 15
    elif 30 <= k <= 80: cotton_score += 10
    else: cotton_score += 3
    
    if 25 <= temp <= 35: cotton_score += 20
    elif 22 <= temp <= 38: cotton_score += 15
    else: cotton_score += 5
    
    if 60 <= humidity <= 80: cotton_score += 20
    elif 50 <= humidity <= 85: cotton_score += 15
    else: cotton_score += 5
    
    if 5.8 <= ph <= 8.0: cotton_score += 15
    elif 5.5 <= ph <= 8.5: cotton_score += 10
    else: cotton_score += 3
    
    if 60 <= rainfall <= 120: cotton_score += 15
    elif 40 <= rainfall <= 150: cotton_score += 10
    else: cotton_score += 3
    
    crop_scores['Cotton'] = min(cotton_score, 100)
    
    # Maize: Moderate-high N, high P, moderate K, warm temp
    maize_score = 0
    if 70 <= n <= 100: maize_score += 20
    elif 50 <= n <= 120: maize_score += 15
    else: maize_score += 5
    
    if 50 <= p <= 80: maize_score += 15
    elif 30 <= p <= 100: maize_score += 10
    else: maize_score += 3
    
    if 30 <= k <= 50: maize_score += 15
    elif 20 <= k <= 70: maize_score += 10
    else: maize_score += 3
    
    if 18 <= temp <= 27: maize_score += 20
    elif 15 <= temp <= 30: maize_score += 15
    else: maize_score += 5
    
    if 55 <= humidity <= 75: maize_score += 20
    elif 45 <= humidity <= 85: maize_score += 15
    else: maize_score += 5
    
    if 5.8 <= ph <= 7.0: maize_score += 15
    elif 5.5 <= ph <= 7.5: maize_score += 10
    else: maize_score += 3
    
    if 80 <= rainfall <= 150: maize_score += 15
    elif 60 <= rainfall <= 180: maize_score += 10
    else: maize_score += 3
    
    crop_scores['Maize'] = min(maize_score, 100)
    
    # Find the best crop
    best_crop = max(crop_scores, key=crop_scores.get)
    confidence = crop_scores[best_crop]
    
    return best_crop, confidence

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        features = [
            float(data['nitrogen']),
            float(data['phosphorus']),
            float(data['potassium']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]
        
        crop, confidence = predict_crop(features)
        
        return jsonify({
            'success': True,
            'crop': crop,
            'confidence': confidence
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    
if __name__ == '__main__':
    app.run(debug=True)
