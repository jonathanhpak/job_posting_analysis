import pandas as pd
import matplotlib
from pathlib import Path

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


# Load job postings data
data_path = Path("data/postings.csv")
if not data_path.exists():
    data_path = Path("archive/postings.csv")

df = pd.read_csv(
    data_path,
    usecols=["normalized_salary", "formatted_experience_level"],
)

# Filter to comparable annual salaries and trim extreme outliers
df_salary = df[
    df["normalized_salary"].notna()
    & df["formatted_experience_level"].notna()
].copy()

# Remove extreme values to reduce the impact of data-entry errors
lower_salary, upper_salary = df_salary["normalized_salary"].quantile([0.05, 0.99])
df_salary = df_salary[
    df_salary["normalized_salary"].between(lower_salary, upper_salary)
].copy()

level_order = [
    "Internship",
    "Entry level",
    "Associate",
    "Mid-Senior level",
    "Director",
    "Executive",
]


# Box plot for annual salary distribution
fig, ax = plt.subplots(figsize=(11, 6))

sns.boxplot(
    data=df_salary,
    x="formatted_experience_level",
    y="normalized_salary",
    order=level_order,
    ax=ax,
    showfliers=False,
    color="#8ecae6",
)

sample_size = min(len(df_salary), 3000)
sns.stripplot(
    data=df_salary.sample(sample_size, random_state=42),
    x="formatted_experience_level",
    y="normalized_salary",
    order=level_order,
    ax=ax,
    color="black",
    alpha=0.15,
    size=2,
)

ax.set_title("Annual Salary Distribution by Experience Level", fontsize=16, fontweight="bold")
ax.set_xlabel("Experience Level", fontsize=12)
ax.set_ylabel("Normalized Annual Salary", fontsize=12)
ax.yaxis.set_major_formatter("${x:,.0f}")
ax.tick_params(axis="x", rotation=30)

fig.tight_layout()
plt.savefig("salary_boxplot.png", dpi=300, bbox_inches="tight")
print("Saved visualization to salary_boxplot.png")
plt.close(fig)
