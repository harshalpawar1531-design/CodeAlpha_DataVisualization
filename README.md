# Supermarket Sales — Data Visualization

**CodeAlpha Internship — Task 3: Data Visualization**

Turning 1,000 real supermarket transactions into a set of business-ready charts, each answering a specific question and pointing to a specific decision. Built with Python, Pandas, Matplotlib, and Seaborn.

---

## 1. Objective

Transform raw transactional data into clear, professional visuals that reveal genuine insights and support decision-making — not just "more charts." Every chart in this project follows one structure:

> **Question → Visualization → Insight → Decision**

No statistic in this README or in the script's output is assumed or fabricated — every number is computed live from `supermarket_sales.csv` when `data_visualization.py` runs.

## 2. Dataset

- **File:** `supermarket_sales.csv`
- **Size:** 1,000 rows × 17 columns
- **Coverage:** 3 supermarket branches (A/Yangon, B/Mandalay, C/Naypyitaw), January 1 – March 30, 2019
- **Quality:** 0 missing values, 0 duplicate rows (verified in-script, not assumed)

| Column | Description |
|---|---|
| Invoice ID | Unique transaction identifier |
| Branch / City | Store location (3 branches, 1 city each) |
| Customer type | Member / Normal |
| Gender | Customer gender |
| Product line | 6 product categories |
| Unit price, Quantity | Price per item, items purchased |
| Tax 5%, Total | Tax amount, total transaction value (incl. tax) |
| Date, Time | Purchase date and time |
| Payment | Cash / Credit card / Ewallet |
| cogs | Cost of goods sold |
| gross margin percentage | Constant (4.761905%) across all rows — see note below |
| gross income | Profit on the transaction |
| Rating | Customer satisfaction rating, 1–10 |

**Note on excluded field:** `gross margin percentage` is a single constant value across all 1,000 rows. A constant field carries no comparative information, so — per the "don't create random charts" requirement — it is confirmed programmatically and deliberately **not** visualized.

## 3. Data Preparation

Handled in `data_visualization.py` before any chart is built:
1. Load the CSV and confirm shape/columns.
2. Check for missing values and duplicate rows (both are 0).
3. Convert `Date` to `datetime`.
4. Derive `Hour` (from `Time`) and `DayOfWeek` (from `Date`) for time-based analysis.
5. Confirm `gross margin percentage` is constant and exclude it from visual analysis.

## 4. Visualizations

All 9 charts are saved as high-resolution PNGs in `visualizations/`.

### 01 — Total Revenue by Branch
- **Question:** Which branch generates the most revenue?
- **Insight:** Branch C leads ($110,568.71), only ~4% ahead of the lowest branch. Revenue is nearly even across all three branches.
- **Decision:** No branch is meaningfully underperforming — don't base expansion or budget-cut decisions on branch revenue alone.

### 02 — Total Revenue by Product Line
- **Question:** Which product line drives the most revenue?
- **Insight:** "Food and beverages" leads ($56,144.84); "Health and beauty" trails ($49,193.74). The spread is modest.
- **Decision:** Prioritize stock and shelf space for Food and beverages; review pricing/promotions for Health and beauty.

### 03 — Total Revenue by Day of Week
- **Question:** Which days bring in the most revenue?
- **Insight:** Saturday is strongest ($56,120.81); Monday is weakest ($37,899.08). The dataset covers only ~3 months, so this is a quarter-level pattern, not a guaranteed permanent trend.
- **Decision:** Align staffing and weekend promotions with the Saturday peak; investigate the Monday slowdown before locking in a permanent schedule change.

### 04 — Sales Pattern by Hour (Revenue & Transaction Count)
- **Question:** What times of day do customers shop most?
- **Insight:** Revenue peaks around 7 PM, with a secondary early-afternoon peak; traffic dips in the late evening.
- **Decision:** Schedule more floor/checkout staff during the midday and evening peaks.

### 05 — Rating Distribution by Branch (Boxplot)
- **Question:** Does customer satisfaction differ meaningfully by branch?
- **Insight:** Average ratings are close (6.82–7.07 / 10), and the within-branch spread is far larger than the gap between branch averages.
- **Decision:** Don't act on this small average gap alone — if service quality is a concern, gather targeted feedback rather than reallocating resources based on this chart.

### 06 — Average Spend: Member vs. Normal
- **Question:** Do members spend more per visit than non-members?
- **Insight:** Members spend $9.67 more per transaction on average — small relative to the overall spread (std ≈ $245).
- **Decision:** Membership status alone is not a strong revenue lever; test targeted member offers before expanding the loyalty program further.

### 07 — Payment Method Share by Customer Type
- **Question:** Do payment preferences differ by membership status?
- **Insight:** Cash, Credit card, and Ewallet usage is fairly balanced for both Members and Normal customers — no method dominates either group.
- **Decision:** Keep investing equally in all three payment channels at every branch.

### 08 — Transaction Value Distribution
- **Question:** What does a typical transaction look like?
- **Insight:** Right-skewed distribution — the mean ($322.97) sits above the median ($253.85), pulled up by a smaller number of large baskets.
- **Decision:** Basket-building promotions aimed at the large volume of mid-range baskets may have more impact than targeting already-large outlier purchases.

### 09 — Correlation Heatmap (Price, Quantity, Total, Rating)
- **Question:** Does higher spending correlate with higher satisfaction?
- **Insight:** Total spend correlates strongly with Quantity (0.71) and Unit price (0.63), as expected by construction. Rating shows essentially no correlation with Total spend (-0.04).
- **Decision:** Don't assume big spenders are happier customers — satisfaction drivers should be studied separately from basket size. *(Correlation is not causation — no causal claim is made anywhere in this project.)*

## 5. Tech Stack

- Python 3
- Pandas — data loading, cleaning, aggregation
- Matplotlib — chart rendering and custom styling
- Seaborn — statistical plots (boxplot, heatmap) and theming

All free and open source.

## 6. Project Structure

```text
Task3_Data_Visualization/
│
├── data_visualization.py     # Main script: load → clean → visualize → print insights
├── supermarket_sales.csv     # Dataset (1,000 rows, 17 columns)
├── requirements.txt
├── README.md
├── .gitignore
└── visualizations/           # 9 generated PNG charts
    ├── 01_revenue_by_branch.png
    ├── 02_revenue_by_product_line.png
    ├── 03_revenue_by_day_of_week.png
    ├── 04_sales_pattern_by_hour.png
    ├── 05_rating_distribution_by_branch.png
    ├── 06_avg_spend_member_vs_normal.png
    ├── 07_payment_method_by_customer_type.png
    ├── 08_transaction_value_distribution.png
    └── 09_correlation_heatmap.png
```

## 7. How to Run

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Task3_Data_Visualization

# 2. Install dependencies (free, open source)
pip install -r requirements.txt

# 3. Run the script
python data_visualization.py
```

The script prints the underlying numbers and insight for every chart to the console, and saves all 9 charts to `visualizations/`.

## 8. Limitations

- The dataset spans only ~3 months (Jan–Mar 2019) from one country's supermarket chain — patterns (e.g. day-of-week trends) reflect this specific quarter, not a guaranteed long-term trend.
- `cogs` is effectively the pre-tax transaction total rather than a true wholesale cost, and `gross margin percentage` is a fixed constant — both are acknowledged limitations of the source data, not this analysis.
- All relationships reported (e.g. spend vs. rating) are correlational; no causal claims are made.

## 9. Author

**Harshal** — B.Tech CSE (Data Science / AI-ML), DBATU
CodeAlpha Data Science Internship — Task 3

---
*This project is part of the CodeAlpha Internship program. Dataset originally published on Kaggle as "Supermarket Sales" (aungpyaeap/supermarket-sales).*
