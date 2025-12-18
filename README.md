# 🛡️ SpamShield - AI Email & SMS Spam Classifier

An intelligent, modern web application that uses Machine Learning to detect spam in emails and SMS messages. Built with Streamlit and scikit-learn.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![ML](https://img.shields.io/badge/ML-Naive%20Bayes-green)

## ✨ Features

- 🔍 **Real-time Spam Detection** - Instantly analyze emails and SMS messages
- 🤖 **AI-Powered Analysis** - Uses Multinomial Naive Bayes classifier
- 📊 **Interactive Dashboard** - Track your analysis history and statistics
- 🎨 **Modern UI** - Beautiful, responsive design with smooth animations
- 📱 **Mobile Friendly** - Works seamlessly on all devices
- 📜 **Message History** - Keep track of all analyzed messages

## 🚀 Live Demo

[View Live Demo](https://your-app-url.streamlit.app)

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/campusx-official/sms-spam-classifier.git
   cd sms-spam-classifier
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:8501`

## 📦 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and select your repository
4. Set the main file path to `app.py`
5. Click "Deploy"

### Deploy to Heroku

1. Install Heroku CLI and login
   ```bash
   heroku login
   ```

2. Create a new Heroku app
   ```bash
   heroku create your-app-name
   ```

3. Deploy
   ```bash
   git push heroku main
   ```

### Deploy to Railway

1. Connect your GitHub repository to [Railway](https://railway.app/)
2. Railway will auto-detect the Procfile and deploy

## 📁 Project Structure

```
sms-spam-classifier/
├── app.py                 # Main Streamlit application
├── model.pkl              # Trained ML model
├── vectorizer.pkl         # TF-IDF vectorizer
├── spam.csv               # Training dataset
├── requirements.txt       # Python dependencies
├── Procfile               # Heroku deployment config
├── setup.sh               # Setup script for deployment
├── runtime.txt            # Python version specification
├── nltk.txt               # NLTK data requirements
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── README.md              # This file
```

## 🧠 How It Works

1. **Text Preprocessing**
   - Convert to lowercase
   - Tokenization
   - Remove special characters
   - Remove stopwords and punctuation
   - Apply Porter Stemming

2. **Feature Extraction**
   - TF-IDF Vectorization with max 3000 features

3. **Classification**
   - Multinomial Naive Bayes classifier
   - Trained on 5,572 SMS messages

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | ~97% |
| Precision | ~100% |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- Dataset: [SMS Spam Collection](https://www.kaggle.com/uciml/sms-spam-collection-dataset)
- Original project by [CampusX](https://github.com/campusx-official)

