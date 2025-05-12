# Phishing URL Detection Tool

This is a web-based tool that uses machine learning to detect whether a given URL is safe or a phishing attempt. It is developed as part of a cybersecurity internship project.

---

## Problem Statement

Phishing is a major cybersecurity threat where attackers trick users into revealing sensitive information by using fake websites. This project aims to build an AI-powered system that detects phishing URLs based on key features extracted from the URL itself, helping users stay safe online.

---

## Features

- Input any URL to check if it's **safe** or **phishing**
- Uses a trained **machine learning model** for predictions
- **Feature extraction** from the URL structure
- Simple and responsive **web interface** using Flask

---

## Project Structure

```
phishing_webapp/
│
├── app.py                 # Flask web application
├── demo.mkv               # Video demo of tool working 
├── model.pkl              # Trained ML model
├── features.pkl              
├── templates/
│   └── index.html         # Frontend page
├── train_model.py         # Script to train the model  
├── testing_url.txt        # Sample urls for testing
├── phishing_site_urls.csv # Dataset used 
├── README.md              # Project overview and instructions
├── presentation.pdf       
└── research_paper.pdf 
```

---

## Setup Instructions

1. **Run the Flask App**:
    ```bash
    python app.py
    ```

2. **Open in Browser**:
    Go to http://127.0.0.1:5000/ in your browser.

---

## YouTube Demo Video

Watch the full demonstration here:  
https://youtu.be/9zEOElLJ94M
---

## License & Disclaimer
 
**Disclaimer:** This tool is built for **educational purposes only**. It is not intended for commercial or production use. Always use a multi-layered approach to cybersecurity.

---

## Author

Developed by Rujuta Shetkar and Pratiksha Swami as part of Digisuraksha Cybersecurity Internship Project.
