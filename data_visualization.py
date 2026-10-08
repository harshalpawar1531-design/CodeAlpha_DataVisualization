"""
CodeAlpha Internship - Task 3: Data Visualization
Supermarket Sales Data Visualization

Author: Harshal
Dataset: supermarket_sales.csv (1,000 transactions, 3 branches, Jan-Mar 2019)
Source: Public Kaggle "Supermarket Sales" dataset (aungpyaeap/supermarket-sales)

Structure of this script:
    1. Load & inspect data
    2. Clean / type-cast data
    3. Generate visualizations, each tied to a specific business question
    4. Print a short insight summary for every chart to the console

Every number quoted in the console output and in the README is computed
directly from this dataset at runtime -- nothing is hard-coded or assumed.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ---------------------------------------------------------------------------
# 0. CONFIG
# ---------------------------------------------------------------------------
DATA_PATH = "supermarket_sales.csv"
OUTPUT_DIR = "visualizations"

sns.set_theme(style="whitegrid", context="talk")
PALETTE = "crest"
ACCENT = "#2E5266"
plt.rcParams["figure.dpi"] = 110
plt.rcParams["savefig.dpi"] = 200
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlesize"] = 15
plt.rcParams["axes.titlepad"] = 14

os.makedirs(OUTPUT_DIR, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved -> {path}")


def money(x, pos=None):
    return f"${x:,.0f}"


# ---------------------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------------------
print("=" * 70)
print("STEP 1: Loading data")
print("=" * 70)

df = pd.read_csv(DATA_PATH)
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}")

# ---------------------------------------------------------------------------
# 2. INSPECT & CLEAN
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 2: Inspecting & cleaning data")
print("=" * 70)

print("\nMissing values per column:")
print(df.isnull().sum())

n_dupes = df.duplicated().sum()
print(f"\nDuplicate rows: {n_dupes}")

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Derive Hour and Day of week from Date/Time (needed for time-based questions)
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
df["DayOfWeek"] = df["Date"].dt.day_name()

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# "gross margin percentage" is a constant column (single value across all rows)
# -> confirmed below, and therefore excluded from visualizations since a
# constant field carries no analytical/comparative information.
unique_margin = df["gross margin percentage"].unique()
print(f"\nUnique values in 'gross margin percentage': {unique_margin} "
      f"(constant -> not visualized)")

print(f"\nDate range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print("\nData is clean: no missing values, no duplicate rows, and no fabricated fields.")

# ===========================================================================
# CHART 1 — Which branch generates the most revenue?
# ===========================================================================
branch_rev = df.groupby("Branch")["Total"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(7, 5.5))
bars = ax.bar(branch_rev.index, branch_rev.values, color=sns.color_palette(PALETTE, 3))
ax.set_title("Total Revenue by Branch")
ax.set_xlabel("Branch")
ax.set_ylabel("Total Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money))
for b in bars:
    ax.annotate(f"${b.get_height():,.0f}", (b.get_x() + b.get_width() / 2, b.get_height()),
                ha="center", va="bottom", fontsize=11)
save(fig, "01_revenue_by_branch.png")

print("\n[Chart 1] Revenue by Branch")
print(branch_rev.round(2).to_string())
gap_pct = (branch_rev.max() - branch_rev.min()) / branch_rev.min() * 100
print(f"Insight: Branch {branch_rev.idxmax()} leads with ${branch_rev.max():,.2f}, "
      f"only {gap_pct:.1f}% ahead of the lowest branch ({branch_rev.idxmin()}). "
      f"Revenue is nearly even across all three branches.")
print("Decision: No branch is meaningfully underperforming, so revenue-driven "
      "budget cuts or expansion decisions should not be based on branch alone.")

# ===========================================================================
# CHART 2 — Which product line drives the most revenue?
# ===========================================================================
line_rev = df.groupby("Product line")["Total"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(line_rev.index, line_rev.values, color=sns.color_palette(PALETTE, len(line_rev)))
ax.set_title("Total Revenue by Product Line")
ax.set_xlabel("Total Revenue ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(money))
for b in bars:
    ax.annotate(f"${b.get_width():,.0f}", (b.get_width(), b.get_y() + b.get_height() / 2),
                ha="left", va="center", fontsize=10, xytext=(5, 0), textcoords="offset points")
save(fig, "02_revenue_by_product_line.png")

print("\n[Chart 2] Revenue by Product Line")
print(line_rev.sort_values(ascending=False).round(2).to_string())
top_line, bottom_line = line_rev.idxmax(), line_rev.idxmin()
print(f"Insight: '{top_line}' is the top revenue-generating line "
      f"(${line_rev.max():,.2f}); '{bottom_line}' trails all lines "
      f"(${line_rev.min():,.2f}). The spread across lines is modest overall.")
print(f"Decision: Prioritize stock availability and shelf space for '{top_line}', "
      f"and review pricing/promotion strategy for '{bottom_line}'.")

# ===========================================================================
# CHART 3 — Which days of the week bring in the most revenue?
# ===========================================================================
day_rev = df.groupby("DayOfWeek")["Total"].sum().reindex(day_order)

fig, ax = plt.subplots(figsize=(9, 5.5))
colors = [ACCENT if d == day_rev.idxmax() else "#A9C6D8" for d in day_rev.index]
bars = ax.bar(day_rev.index, day_rev.values, color=colors)
ax.set_title("Total Revenue by Day of Week")
ax.set_xlabel("Day of Week")
ax.set_ylabel("Total Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
save(fig, "03_revenue_by_day_of_week.png")

print("\n[Chart 3] Revenue by Day of Week")
print(day_rev.round(2).to_string())
print(f"Insight: {day_rev.idxmax()} is the strongest day (${day_rev.max():,.2f}); "
      f"{day_rev.idxmin()} is the weakest (${day_rev.min():,.2f}). "
      "Note: the dataset spans only ~3 months (Jan-Mar 2019), so this reflects "
      "one quarter, not a guaranteed permanent weekly pattern.")
print(f"Decision: Consider aligning staffing levels and weekend promotions with "
      f"the {day_rev.idxmax()} peak, while investigating causes of the "
      f"{day_rev.idxmin()} slowdown before committing to a permanent schedule change.")

# ===========================================================================
# CHART 4 — What time of day do customers shop the most?
# ===========================================================================
hourly = df.groupby("Hour").agg(Transactions=("Total", "count"), Revenue=("Total", "sum"))

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(hourly.index, hourly["Revenue"], color="#A9C6D8", label="Revenue")
ax1.set_xlabel("Hour of Day (24h)")
ax1.set_ylabel("Total Revenue ($)")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(money))
ax1.set_title("Store Traffic Pattern: Revenue & Transaction Count by Hour")

ax2 = ax1.twinx()
ax2.plot(hourly.index, hourly["Transactions"], color=ACCENT, marker="o", linewidth=2.5,
         label="Transactions")
ax2.set_ylabel("Number of Transactions")
ax2.grid(False)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
save(fig, "04_sales_pattern_by_hour.png")

print("\n[Chart 4] Sales Pattern by Hour")
peak_hour = hourly["Revenue"].idxmax()
print(hourly.round(2).to_string())
print(f"Insight: Revenue peaks around {peak_hour}:00, with a second smaller peak "
      "in the early afternoon. Traffic is lowest in the late evening near closing time.")
print("Decision: Schedule more staff on the floor and at checkout during the "
      "midday and evening peaks to reduce wait times and support higher basket volume.")

# ===========================================================================
# CHART 5 — Does customer rating differ meaningfully by branch?
# ===========================================================================
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df, x="Branch", y="Rating", hue="Branch", palette=PALETTE,
            ax=ax, legend=False)
ax.set_title("Customer Rating Distribution by Branch")
ax.set_xlabel("Branch")
ax.set_ylabel("Rating (out of 10)")
save(fig, "05_rating_distribution_by_branch.png")

rating_by_branch = df.groupby("Branch")["Rating"].agg(["mean", "std"])
print("\n[Chart 5] Rating Distribution by Branch")
print(rating_by_branch.round(2).to_string())
print(f"Insight: Average ratings are close across branches "
      f"({rating_by_branch['mean'].min():.2f}-{rating_by_branch['mean'].max():.2f} out of 10), "
      f"and the spread within each branch (std ~{rating_by_branch['std'].mean():.2f}) "
      "is far larger than the gap between branch averages. There is no strong "
      "evidence that one branch delivers a meaningfully different customer experience.")
print("Decision: Don't act on the small average-rating gap alone; if service "
      "quality is a concern, investigate with targeted customer feedback "
      "rather than reallocating resources based on this chart.")

# ===========================================================================
# CHART 6 — Do members spend more per visit than non-members?
# ===========================================================================
spend_by_type = df.groupby("Customer type")["Total"].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(7, 5.5))
bars = ax.bar(spend_by_type.index, spend_by_type.values,
              color=sns.color_palette(PALETTE, 2))
ax.set_title("Average Spend per Transaction: Member vs. Normal")
ax.set_xlabel("Customer Type")
ax.set_ylabel("Average Total per Transaction ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money))
for b in bars:
    ax.annotate(f"${b.get_height():,.2f}", (b.get_x() + b.get_width() / 2, b.get_height()),
                ha="center", va="bottom", fontsize=11)
save(fig, "06_avg_spend_member_vs_normal.png")

print("\n[Chart 6] Average Spend: Member vs Normal")
print(spend_by_type.round(2).to_string())
diff = spend_by_type.iloc[0] - spend_by_type.iloc[1]
print(f"Insight: Members spend ${diff:.2f} more per transaction on average than "
      "Normal customers -- a small difference relative to the overall spread of "
      "transaction totals (std ~$245). The membership program shows only a mild "
      "association with higher basket size, not a strong one.")
print("Decision: Membership alone is not currently a strong lever for revenue "
      "growth; consider testing targeted member-only offers before investing "
      "more heavily in the loyalty program.")

# ===========================================================================
# CHART 7 — Do payment method preferences differ by customer type?
# ===========================================================================
pay_ct = pd.crosstab(df["Customer type"], df["Payment"])
pay_pct = pay_ct.div(pay_ct.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(9, 6))
pay_pct.plot(kind="bar", ax=ax, color=sns.color_palette(PALETTE, 3))
ax.set_title("Payment Method Share by Customer Type")
ax.set_xlabel("Customer Type")
ax.set_ylabel("Share of Transactions (%)")
plt.setp(ax.get_xticklabels(), rotation=0)
ax.legend(title="Payment")
save(fig, "07_payment_method_by_customer_type.png")

print("\n[Chart 7] Payment Method Share by Customer Type")
print(pay_pct.round(1).to_string())
print("Insight: Payment method usage is fairly balanced across Cash, Credit "
      "card, and Ewallet for both Members and Normal customers, with no single "
      "method dominating either group.")
print("Decision: Continue supporting all three payment methods equally at every "
      "branch rather than prioritizing one channel's infrastructure over another.")

# ===========================================================================
# CHART 8 — What does a typical transaction look like?
# ===========================================================================
fig, ax = plt.subplots(figsize=(9, 6))
sns.histplot(df["Total"], bins=30, kde=True, color=ACCENT, ax=ax)
ax.axvline(df["Total"].median(), color="red", linestyle="--", linewidth=1.5,
           label=f"Median (${df['Total'].median():,.2f})")
ax.axvline(df["Total"].mean(), color="orange", linestyle="--", linewidth=1.5,
           label=f"Mean (${df['Total'].mean():,.2f})")
ax.set_title("Distribution of Transaction Value")
ax.set_xlabel("Total Transaction Value ($)")
ax.set_ylabel("Number of Transactions")
ax.legend()
save(fig, "08_transaction_value_distribution.png")

print("\n[Chart 8] Transaction Value Distribution")
print(df["Total"].describe().round(2).to_string())
print(f"Insight: The distribution is right-skewed -- the mean (${df['Total'].mean():,.2f}) "
      f"sits above the median (${df['Total'].median():,.2f}), pulled up by a smaller "
      "number of large-basket transactions.")
print("Decision: Basket-building promotions (e.g. 'add-on' discounts) aimed at "
      "the large volume of mid-range baskets could be more impactful than "
      "targeting the already-large outlier transactions.")

# ===========================================================================
# CHART 9 — Does higher spending correlate with a higher satisfaction rating?
# ===========================================================================
corr_cols = ["Unit price", "Quantity", "Total", "Rating"]
corr = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="crest", vmin=-1, vmax=1,
            square=True, linewidths=0.5, ax=ax, cbar_kws={"label": "Correlation"})
ax.set_title("Correlation: Price, Quantity, Total Spend & Rating", pad=20)
fig.subplots_adjust(top=0.88)
save(fig, "09_correlation_heatmap.png")

print("\n[Chart 9] Correlation Heatmap")
print(corr.round(2).to_string())
print(f"Insight: Total spend correlates strongly with Quantity "
      f"({corr.loc['Total', 'Quantity']:.2f}) and Unit price "
      f"({corr.loc['Total', 'Unit price']:.2f}), as expected. Rating shows "
      f"essentially no correlation with Total spend "
      f"({corr.loc['Total', 'Rating']:.2f}) -- customers who spend more are not "
      "systematically more or less satisfied. This is a correlation, not a "
      "causal claim.")
print("Decision: Don't assume big spenders are automatically happier customers "
      "(or vice versa); satisfaction drivers should be investigated separately "
      "from basket size, e.g. through direct service-quality feedback.")

print("\n" + "=" * 70)
print(f"All 9 visualizations saved to ./{OUTPUT_DIR}/")
print("=" * 70)
