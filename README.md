# 📚 Gemini Quiz Grader Web App

This is a Flask-based web application that allows users to **upload handwritten quiz images**, which are then **analyzed and graded automatically** using **Google Gemini 1.5 Flash API**. The graded results are saved as `.txt` files that can be downloaded as a ZIP archive.

---

## 🚀 Features

* 📥 Upload multiple handwritten quiz images (`.jpg`, `.jpeg`, `.png`)
* 🧠 Automatic content extraction, brief analysis, improvement suggestions, and grading out of 10 using Gemini 1.5 Flash
* 📁 All results saved in `.txt` files inside the `output` folder
* 📦 Download all graded quizzes as a ZIP file
* 🌐 Simple and responsive web interface using HTML/CSS

---

## 🧾 Project Structure

```bash
.
├── app.py                     # Flask application logic
├── input/                    # Folder to store uploaded quiz images
├── output/                   # Folder to store Gemini-graded text files
├── static/
│   └── styles.css            # Custom CSS for UI
├── templates/
│   ├── index.html            # Upload form
│   ├── success.html          # Download results page
│   └── images/
│       └── background.jpg    # Background image for the app
```

---

## 🧠 Powered by Gemini

This app uses **Google's Gemini 1.5 Flash model** to analyze and grade the handwritten quizzes.

### 🔑 Get Your API Key

1. Visit: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account.
3. Click “Generate API Key”.
4. Copy and paste the key into the `app.py` file:

```python
genai.configure(api_key="your_api_key_here")
```

---

## 💻 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/quiz-grader-gemini.git
cd quiz-grader-gemini
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If you don't have a `requirements.txt`, here are the dependencies you can manually install:

```bash
pip install Flask Pillow google-generativeai
```

### 4. Add your Gemini API key

Edit the line in `app.py` and insert your API key:

```python
genai.configure(api_key="your_api_key_here")
```

### 5. Run the Flask app

```bash
python app.py
```

The app will be live at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📝 How to Use the App

1. Open the app in your browser.
2. Upload one or more handwritten quiz images (`.png`, `.jpg`, `.jpeg`).
3. Click "Submit".
4. The app will process each image using Gemini and generate a `.txt` file per quiz in the `output/` folder.
5. On the success page, click "Download Results" to get all graded files in a ZIP archive.

---
