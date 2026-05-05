import kagglehub
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load job postings data
df = pd.read_csv("data/postings.csv")

# Filter to only rows with salary data and experience level
df_salary = df[
    (df['med_salary'].notna()) & 
    (df['formatted_experience_level'].notna())
].copy()

# Create figure with violin plot for median salary
fig, ax = plt.subplots(figsize=(10, 6))

# Violin plot for median salary
sns.violinplot(data=df_salary, x='formatted_experience_level', y='med_salary', ax=ax)
ax.set_title('Median Salary by Experience Level', fontsize=14, fontweight='bold')
ax.set_xlabel('Experience Level', fontsize=12)
ax.set_ylabel('Median Salary ($)', fontsize=12)
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('salary_violin_plots.png', dpi=300, bbox_inches='tight')
print("Saved visualization to salary_violin_plots.png")
plt.show()
