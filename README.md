# 🏏 Virat Kohli - Cricket Performance Dashboard

A visually engaging and interactive Streamlit web app that provides deep insights into the cricket career of **Virat Kohli**. Explore match statistics, filter data, and predict scores based on historical patterns — all in one place.

![Dashboard Screenshot]


## 📁 Project Structure

```
├── data_for_streamlit.csv    # Dataset used for analytics
├── virat-kohli.png           # Image used in the About section
├── favicon.png               # Favicon icon for the app
├── app.py                    # Main Streamlit application file
└── README.md                 # Project documentation
```

## 🚀 Features

### 1. 🧮 **Cricket Performance Dashboard**
- View total runs, matches, strike rate, best score, centuries, and fifties.
- Filter insights by match type (Test, ODI, T20).
- Visualize yearly run trends with interactive charts.

### 2. 🔮 **Score Predictor**
- Predict the expected score based on match type, opposition, and ground.
- Uses historical averages for estimation.

### 3. 📊 **Interactive Data Table**
- Filter match records by:
  - Match type
  - Year range
  - Opposition team
- Sort by newest/oldest
- Download the filtered dataset as a CSV

### 4. ℹ️ **About Section**
- Detailed profile of Virat Kohli, highlighting:
  - Career achievements
  - Leadership impact
  - Contributions beyond cricket

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Data Visualization**: [Plotly](https://plotly.com/python/)
- **Data Handling**: [Pandas](https://pandas.pydata.org/)
- **Language**: Python 3

## 📦 Installation & Usage

### 🔧 Prerequisites
- Python 3.7 or higher
- `pip` installed

### 📥 Clone the repository
```bash
git clone https://github.com/yourusername/virat-kohli-dashboard.git
cd virat-kohli-dashboard
```

### 📦 Install dependencies
```bash
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install streamlit pandas plotly
```

### ▶️ Run the app
```bash
streamlit run app.py
```

## 📊 Dataset

The data used (`data_for_streamlit.csv`) includes:
- Match type (Test, ODI, T20)
- Opposition teams
- Grounds
- Runs, Strike Rate, Year, Date
- Other performance metrics

> ⚠️ Ensure your dataset includes the following fields: `Runs`, `Match Type`, `Opposition`, `Ground`, `Year`, `Start Date`, `SR`, `Inns`, `MOM_Won`, `Pos`.

## 📸 Screenshots



## 🙋‍♂️ Author

**Dhanush Devadiga**  
Student ID: 24238836  
Master’s in UXD, University College Dublin

## 📄 License

This project is for educational and non-commercial purposes.
