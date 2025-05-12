import pandas as pd
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("C:/Users/Rujuta/OneDrive/Desktop/Phishing_webapp/phishing_site_urls.csv")  # Make sure this file is in the same folder

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

# Generate features
data['url_length'] = data['URL'].apply(len)
data['has_at'] = data['URL'].apply(lambda x: 1 if '@' in x else 0)
data['has_ip'] = data['URL'].apply(lambda x: 1 if re.match(r"http[s]?://(\d{1,3}\.){3}\d{1,3}", x) else 0)
data['has_https'] = data['URL'].apply(lambda x: 1 if x.lower().startswith('https') else 0)
data['phishing_keywords'] = data['URL'].apply(contains_phishing_keywords)
data['suspicious_extension'] = data['URL'].apply(suspicious_extension)
data['subdomain_count'] = data['URL'].apply(subdomain_count)
data['uses_shortener'] = data['URL'].apply(has_shortener)
data['digit_letter_ratio'] = data['URL'].apply(digit_letter_ratio)

# Separate phishing and legitimate URLs
legitimate = data[data['Label'] == 'good']
phishing = data[data['Label'] == 'bad']

# Undersample legitimate URLs to match the number of phishing URLs
legitimate_undersampled = legitimate.sample(len(phishing))

# Concatenate the undersampled legitimate URLs with phishing URLs
balanced_data = pd.concat([legitimate_undersampled, phishing])

# Shuffle the data to ensure randomness
balanced_data = balanced_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Check the balance after under-sampling
print("Balanced dataset class distribution:")
print(balanced_data['Label'].value_counts())

# Prepare features (X) and labels (y) for the balanced dataset
X_balanced = balanced_data[['url_length', 'has_at', 'has_ip', 'has_https', 'phishing_keywords', 
                            'suspicious_extension', 'subdomain_count', 'uses_shortener', 'digit_letter_ratio']]
y_balanced = balanced_data['Label'].map({'good': 0, 'bad': 1})  # Convert 'good'/'bad' to 0/1

# Split the balanced dataset into training and testing sets (80% for training, 20% for testing)
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

# Train the RandomForestClassifier on the balanced dataset
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save the trained model and feature names to .pkl files
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(X_balanced.columns.tolist(), open('features.pkl', 'wb'))

print("Model and features saved to 'model.pkl' and 'features.pkl'")
