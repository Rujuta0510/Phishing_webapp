from flask import Flask, request, render_template
import pandas as pd
import re
import pickle

# Load trained model and feature names (make sure the path is correct)
model = pickle.load(open('model.pkl', 'rb'))  # Make sure this path is correct
features_list = pickle.load(open('features.pkl', 'rb'))  # Make sure this path is correct

app = Flask(__name__)

# Feature extraction functions
def contains_phishing_keywords(url):
    keywords = ['login', 'update', 'verify', 'banking', 'secure', 'account', 'ebay', 'paypal']
    return 1 if any(k in url.lower() for k in keywords) else 0

def suspicious_extension(url):
    return 1 if any(ext in url for ext in ['.xyz', '.top', '.club', '.tk', '.ga', '.ml']) else 0

def subdomain_count(url):
    try:
        domain = url.split('/')[2]
        return domain.count('.') - 1
    except:
        return 0

def has_shortener(url):
    shorteners = ['bit.ly', 'goo.gl', 'tinyurl', 't.co', 'ow.ly', 'is.gd']
    return 1 if any(s in url.lower() for s in shorteners) else 0

def digit_letter_ratio(url):
    try:
        domain = url.split('/')[2]
        digits = sum(c.isdigit() for c in domain)
        letters = sum(c.isalpha() for c in domain)
        return digits / (letters + 1e-5)
    except:
        return 0

def extract_features(url):
    features = {
        'url_length': len(url),
        'has_at': 1 if '@' in url else 0,
        'has_ip': 1 if re.match(r"http[s]?://(\d{1,3}\.){3}\d{1,3}", url) else 0,
        'has_https': 1 if url.lower().startswith('https') else 0,
        'phishing_keywords': contains_phishing_keywords(url),
        'suspicious_extension': suspicious_extension(url),
        'subdomain_count': subdomain_count(url),
        'uses_shortener': has_shortener(url),
        'digit_letter_ratio': digit_letter_ratio(url)
    }
    return pd.DataFrame([[features[col] for col in features_list]], columns=features_list)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']
    features = extract_features(url)
    prediction = model.predict(features)[0]
    
    if prediction == 1:
        result = "⚠️ This URL is likely PHISHING."
    else:
        result = "✅ This URL appears LEGITIMATE."
    
    return render_template('index.html', result=result, url=url)

if __name__ == '__main__':
    app.run(debug=True)
