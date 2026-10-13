# 🏏 IPL Analytics Dashboard & Winner Prediction

An interactive **IPL Analytics and Match Winner Prediction** web application built using Python, Pandas, Machine Learning, and Streamlit. This project explores historical IPL data, analyzes team performance, visualizes scoring trends, and generates experimental match-winner predictions.

## 🚀 Live Demo

🔗 **[Explore the Live IPL Analytics Dashboard](https://ipl-winner-prediction-ipl-data-analysis-eo4s47yg4rruvsmxyypqub.streamlit.app/)**

📂 **[View Source Code on GitHub](https://github.com/amankumardev/IPL-winner-prediction-IPL-Data-Analysis)**

---

## 📌 Project Overview

The IPL Analytics Dashboard provides an interactive way to explore historical Indian Premier League (IPL) match data. Users can analyze match statistics, compare team wins, explore venue trends, study season-wise scoring patterns, and experiment with machine-learning-based match winner predictions.

The application contains two main sections:

- **Analytics Dashboard:** Interactive visualizations and historical IPL performance analysis.
- **Winner Prediction:** An experimental prediction interface where users select teams, venue, toss winner, and toss decision.

## ✨ Key Features

### 📊 IPL Analytics Dashboard
- Interactive dashboard for exploring historical IPL statistics.
- Filter matches by season, team, and venue.
- Compare team wins using visual charts.
- Analyze the most frequently used venues.
- Visualize total runs across IPL seasons.
- Explore toss decisions and their distribution.
- Display key metrics such as total matches, seasons, teams, and runs.

### 🔮 IPL Winner Prediction
- Select two competing IPL teams.
- Choose the match venue.
- Select the toss winner and toss decision.
- Generate an experimental match-winner prediction.
- Display the predicted winner and estimated win probabilities.

### 📈 Data Visualization
- Bar charts for team and venue comparisons.
- Line charts for season-wise scoring trends.
- Interactive filters for exploring different subsets of the data.

## 🖥️ Project Screenshots

### 1. Analytics Dashboard

![IPL Analytics Dashboard](screnshot/Screenshot%202026-10-14%20012406.png)

### 2. Team Wins Comparison

![Team Wins Comparison](screenshots/team-wins-comparison.png)

### 3. Top Venues by Match Count

![Top Venues Analysis](screenshots/venue-analysis.png)

### 4. Season-wise Runs and Toss Analysis

![Season Runs and Toss Analysis](screenshots/season-runs-toss-analysis.png)

### 5. Winner Prediction Interface

![IPL Winner Prediction Form](screenshots/winner-prediction-form.png)

### 6. Prediction Result

![IPL Winner Prediction Result](screenshots/winner-prediction-result.png)

> **Note:** Create a folder named `screenshots` in your repository and place the corresponding image files inside it. Use the exact filenames referenced above.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing and analysis |
| Scikit-learn | Machine learning utilities |
| XGBoost | Machine learning model support |
| Joblib | Model loading and serialization |
| Streamlit | Interactive web application |
| Git & GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

## 📂 Project Structure

```text
IPL-winner-prediction-IPL-Data-Analysis/
│
├── app.py
├── requirements.txt
├── README.md
├── matches.csv
├── IPL_ball_by_ball_cleaned.csv
├── ipl_match_level.csv
├── ipl_winner_model.pkl
├── IPL-winner-prediction.ipynb
└── screenshots/
    ├── dashboard-overview.png
    ├── team-wins-comparison.png
    ├── venue-analysis.png
    ├── season-runs-toss-analysis.png
    ├── winner-prediction-form.png
    └── winner-prediction-result.png
```

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

- Python 3.9 or a compatible Python version for the listed dependencies.
- Git installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/amankumardev/IPL-winner-prediction-IPL-Data-Analysis.git
```

### 2. Navigate to the Project Directory

```bash
cd IPL-winner-prediction-IPL-Data-Analysis
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

### 5. Open the Dashboard

Streamlit will provide a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

## 📖 How to Use

1. Open the live application.
2. Explore the **Analytics Dashboard** to view historical IPL statistics.
3. Use the available filters to analyze seasons, teams, and venues.
4. Navigate to **Winner Prediction**.
5. Select the two teams, venue, toss winner, and toss decision.
6. Click **Predict Match Winner** to view the experimental prediction and estimated probabilities.

## ⚠️ Limitations and Disclaimer

The winner prediction feature is an **experimental machine-learning prototype**. Predictions depend on the trained model and the historical features used by the application; they are not guaranteed to match actual results.

The prediction should not be treated as a reliable betting forecast. Historical performance does not guarantee future outcomes.

## 🎯 Learning Outcomes

Through this project, I practiced:

- Data cleaning and preprocessing.
- Exploratory data analysis (EDA).
- Historical sports data analysis.
- Data visualization and dashboard development.
- Machine learning model integration.
- Building interactive applications with Streamlit.
- Deploying a Python application to the cloud.
- Managing project files using Git and GitHub.

## 👨‍💻 Author

**Aman Kumar**

- GitHub: [@amankumardev](https://github.com/amankumardev)
- Portfolio: [Visit My Portfolio](https://aman-portfolio-2.onrender.com/)
- LinkedIn: [Connect with Me](https://www.linkedin.com/in/aman-kumar-615b5a292/)

## 🌐 Project Links

- **Live Application:** https://ipl-winner-prediction-ipl-data-analysis-eo4s47yg4rruvsmxyypqub.streamlit.app/
- **GitHub Repository:** https://github.com/amankumardev/IPL-winner-prediction-IPL-Data-Analysis

---

⭐ If you find this project interesting, consider giving the repository a star!

*Built with Python, data analytics, machine learning, and a passion for cricket.* 🏏
