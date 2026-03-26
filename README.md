# 📊 SuperStore Sales Analysis

An interactive data analysis dashboard exploring key business questions using the SuperStore dataset.

---

## Project Purpose

This project was built as a **portfolio piece** targeting internships in:
- **Data Analytics**
- **Information Technology**
- **Finance**

---

##  Business Questions Answered

1. **Which category makes the most profit?** (Technology, Furniture, or Office Supplies)
2. **Which region sells the most but makes the least profit?** (East, West, Central, South)
3. **Does giving bigger discounts hurt profit?** (Correlation analysis)
4. **What are the top 5 and bottom 5 products by profit margin?**
5. **What does the monthly sales trend look like?** (Seasonal patterns, Q4 holiday effect)

---

## Quick Start
https://superstoreanalysis-m3wwy6bumyzuouwgmiz5xd.streamlit.app/

### Option 1: Run Locally

```bash
# Clone the repository
git clone https://github.com/iraherrera01/SuperStoreAnalysis.git
cd SuperStoreAnalysis

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

### Option 2: View Notebook

Open `SuperStoreAnalysis.ipynb` in Jupyter Notebook or JupyterLab to see the full analysis journey.

---

## 📁 Project Structure

```
SuperStoreAnalysis/
├── app.py                      # Streamlit web application
├── SuperStoreAnalysis.ipynb    # Jupyter notebook analysis
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── data/
    └── superstore_data.csv     # Dataset (Kaggle)
```

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Programming language |
| **Pandas** | Data manipulation & analysis |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Web application framework |
| **Jupyter** | Exploratory data analysis |

---

## Key Findings

### Q1: Category Profit
- **Technology** leads with $145,454.95 profit
- Office Supplies: $122,490.80
- Furniture: $18,451.27
**interpretation**: Reallocate inventory investment from Furniture to Technology and Office Supplies. Consider discontinuing low-margin furniture lines or renegotiating supplier costs.

### Q2: Region Analysis
- **West** highest sales volume AND profit margin 14.98% - our strongest market 
- **East** follows closely with strong sales and a healthy, 13.48% margin
- **South** has lowest sales volume but a decent 11.93% margin, growth oppurtunity here.
- **Central** $73,352 sales but only 7.92% margin - profitability issue despite good volume

### Q3: Discount Impact
- **Correlation: -0.22** (negative correlation)
- Each 1% increase in discount reduces profit by approximately .22%
- Recommendation: Keep discounts under 20%, implement discount scale (5%, 10%, 15%).

### Q4: Product Margins
- **Best:** Canon imageCLASS MF7460 (+50% margin), consider featuring these **prominently** in marketing
- **Worst:** Eureka Disposable Bags (-275% margin due to 80% discount), unsustainable, likely a clearance item. 

### Q5: Monthly Trend
- **Peak:** November, Black Friday/Cyber Monday effect, drives B2C sales. Ensure inventory is built with high margin/popular items leading up to November.
- **Drop:** December, B2B holiday shutdown pattern, pattern suggests B2B focus (companies pause purchasing for year end). Create promotions targeting B2B budgets, i.e. bulk buying discounts. 

---



## Author

**Ira Herrera**  
Computer Information Systems Student  
*www.linkedin.com/in/iraherrera000/* | *iraherrera000@gmail.com*

---

## License

This project is for educational/portfolio purposes.

---

## Acknowledgments

- Dataset: [SuperStore Dataset on Kaggle](https://www.kaggle.com/)
- Inspired by real-world business analytics scenarios
