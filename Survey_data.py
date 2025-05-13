import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np  # Add this line to import numpy

# Load and inspect CSV
def load_and_inspect_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print("First few rows of the dataset:")
        print(df.head())
        print("\nData types of each column:")
        print(df.dtypes)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

# Load the file
file_path = r"C:\Users\abc\OneDrive\Desktop\PROJECT\xyz.csv"
df = load_and_inspect_csv(file_path)

# Preprocessing
df['Event Name'] = pd.to_numeric(df['Event Name'], errors='coerce')
df = df[df['Event Name'] != 2025].reset_index(drop=True)
years = sorted(df['Event Name'].dropna().unique())
yearly_data = {year: df[df['Event Name'] == year] for year in years}

# Helper: Bar Chart Plotter
def plot_bar(data, title, xlabel, ylabel, color='skyblue', rotate=45):
    plt.figure(figsize=(9, 5))
    data.plot(kind='bar', color=color, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotate, ha='right' if rotate else 'center')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    #plt.tight_layout()

# --- Plot Groups ---
participation_cols = [
    'participation_news', 'participation_google', 'participation_CAG',
    'participation_IIACC', 'participation_NA', 'participation_IIACC_to_others',
    'participation_interview', 'participation_focusgroups'
]

feedback_cols = [
    'workgroup', 'largegroup', 'overall_org', 'comm_to_meets', 'reg_process', 
    'meet_hours', 'meet_length', 'meet_topics', 'meet_format', 'facilitation_process', 'activities',
]
#Please rate your satisfaction with the communication formats available to IIACC and workgroup members:
news_feedback_cols = [
    'news_format', 'news_freq', 'news_content', 'gp_layout',
    'gp_accessibility', 'gp_content', 'gp_usability', 'padlet'
]

categorical_cols = ['representing_IIACC', 'chance_to_contribute']
role_cols = [
    'role_engaging_activities', 'primary_role', 'other_primary_role', 
    'med_role', 'other_role', 'primary_role_description', 'primary_role_term'
]
personal_info_col = ['gender', 'ethnicity', 'residence']
work_col = ['work_nw', 'work_ne', 'work_nc', 'work_c', 'work_e', 'work_se', 'work_sw', 'work_outsideindi']

# Create list to store all plot data
plots = []

# --- Participation ---
for year, year_df in yearly_data.items():
    if all(col in year_df.columns for col in participation_cols):
        counts = year_df[participation_cols].sum()
        plots.append(('Participation Counts for Year ' + str(year), counts, 'Participation Type', 'Number of Participants'))

# --- Feedback Columns ---
for col_set, color in [(feedback_cols, 'lightcoral'), (news_feedback_cols, 'cornflowerblue')]:
    for col in col_set:
        for year, year_df in yearly_data.items():
            if col in year_df.columns:
                data = year_df[col].dropna()
                try:
                    rating_counts = data.astype(int).value_counts().sort_index()
                    plots.append((f"{col.replace('_', ' ').title()} Ratings - {year}", rating_counts, 'Rating', 'Number of Responses'))
                except ValueError:
                    value_counts = data.astype(str).value_counts()
                    plots.append((f"{col.replace('_', ' ').title()} - {year}", value_counts, 'Response', 'Count'))

# --- Categorical Columns ---
for col in categorical_cols + role_cols + personal_info_col:
    for year, year_df in yearly_data.items():
        if col in year_df.columns:
            value_counts = year_df[col].dropna().astype(str).value_counts()
            plots.append((f"{col.replace('_', ' ').title()} - {year}", value_counts, 'Response', 'Count'))

# --- Work Region ---
for year, year_df in yearly_data.items():
    available_cols = [col for col in work_col if col in year_df.columns]
    if available_cols:
        region_counts = year_df[available_cols].apply(pd.to_numeric, errors='coerce').sum()
        plots.append((f"Work Region Participation - {year}", region_counts, 'Region', 'Number of Participants'))

# --- Describe Area ---
for year, year_df in yearly_data.items():
    if 'describe_area' in year_df.columns:
        area_counts = year_df['describe_area'].dropna().astype(str).value_counts()
        plots.append((f"Describe Area Responses - {year}", area_counts, 'Area Description', 'Count'))

# Plotting function with button
def plot_with_button():
    fig, ax = plt.subplots(figsize=(9, 5))
    plt.subplots_adjust(bottom=0.2)
    
    # Initialize plot index
    plot_index = [0]

    # Update function to cycle through plots
    def update_plot(event):
        plot_index[0] = (plot_index[0] + 1) % len(plots)
        ax.clear()
        ax.bar(plots[plot_index[0]][1].index, plots[plot_index[0]][1].values, color='skyblue', edgecolor='black')
        ax.set_title(plots[plot_index[0]][0])
        ax.set_xlabel(plots[plot_index[0]][2])
        ax.set_ylabel(plots[plot_index[0]][3])
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        fig.canvas.draw()

    # Create "Next" button
    ax_next = plt.axes([0.8, 0.01, 0.15, 0.075])
    btn_next = Button(ax_next, 'Next')
    btn_next.on_clicked(update_plot)

    # Show the first plot
    update_plot(None)
    
    # Display the plots
    plt.show()

# Call the function to start the interactive plot display
plot_with_button()

#------------------------------------------------------------------
# Prepare data for stacked bar plot
participation_data = {}

for year, year_df in yearly_data.items():
    participation_data[year] = year_df[participation_cols].sum()

# Convert the participation data into a DataFrame
participation_df = pd.DataFrame(participation_data).T

# Stacked Bar Plot
plt.figure(figsize=(10, 6))

# Plot the stacked bars
participation_df.plot(kind='bar', stacked=True, figsize=(10, 6), color=plt.cm.Paired.colors)

# Customization
plt.title("Stacked Participation Counts Per Year")
plt.xlabel("Year")
plt.ylabel("Count of Participants")
plt.xticks(rotation=45)
plt.legend(title="Participation Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Show the plot
plt.show()

import seaborn as sns

# Heatmap of participation counts per year
plt.figure(figsize=(10, 6))

# Create a heatmap for participation data
sns.heatmap(participation_df, annot=True, cmap='YlGnBu', cbar_kws={'label': 'Participation Count'}, fmt='d')

# Customization
plt.title("Participation Heatmap Per Year")
plt.xlabel("Participation Type")
plt.ylabel("Year")
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()

#---------------------------------------------------------------------------------
# Get unique years from 'Event Name' column
years = sorted(df['Event Name'].dropna().unique())

# Create a dictionary to store the average scores per year for each feedback question
feedback_avg_per_year = {year: {} for year in years}

# Compute the average score for each feedback column per year, excluding zeros
for year, year_df in df.groupby('Event Name'):
    for col in feedback_cols:
        if col in year_df.columns:
            # Filter out zeros and calculate mean for non-zero values
            filtered_data = year_df[col][year_df[col] != 0]
            feedback_avg_per_year[year][col] = filtered_data.mean()

# Convert the feedback_avg_per_year dictionary into a DataFrame for easier plotting
feedback_avg_per_year_df = pd.DataFrame(feedback_avg_per_year).T

# Plotting
plt.figure(figsize=(12, 8))

# Loop over each feedback column to plot
for i, col in enumerate(feedback_cols):
    if col in feedback_avg_per_year_df.columns:  # Only plot columns that exist
        plt.plot(feedback_avg_per_year_df.index, feedback_avg_per_year_df[col], 
                 label=col.replace('_', ' ').title(), marker='o')

# Customize the plot
plt.title("Average Feedback Scores Per Year (Excluding Zeros)")
plt.xlabel("Year")
plt.ylabel("Average Score")
plt.xticks(np.arange(min(feedback_avg_per_year_df.index), max(feedback_avg_per_year_df.index) + 1, 1))
plt.legend(title="Feedback Question", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

#------------------------------------------------------------------------------

def plot_stacked_bar(df, title, xlabel, ylabel):
    ax = df.T.plot(
        kind='bar',
        stacked=True,
        figsize=(10, 6),
        colormap='tab20c'
    )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# Create stacked bar plots across years
for col in ['representing_IIACC', 'chance_to_contribute']:
    col_counts = {}

    for year, year_df in yearly_data.items():
        if col in year_df.columns:
            counts = year_df[col].dropna().astype(str).value_counts()
            col_counts[year] = counts

    if col_counts:
        # Create combined DataFrame
        df_combined = pd.DataFrame(col_counts).fillna(0).astype(int)

        # Ensure consistent response order
        all_responses = sorted(set().union(*[
            df[col].dropna().astype(str).unique()
            for y, df in yearly_data.items()
            if col in df.columns
        ]))
        df_combined = df_combined.reindex(all_responses).fillna(0).astype(int)

        print(f"\n--- Stacked Bar Plot: {col.replace('_', ' ').title()} ---")
        print(df_combined)

        # Plot stacked count bar chart
        plot_stacked_bar(df_combined, f"{col.replace('_', ' ').title()} by Year", "Year", "Count")

        # Plot percentage-based version
        df_percent = df_combined.div(df_combined.sum(axis=0), axis=1) * 100
        plot_stacked_bar(df_percent, f"{col.replace('_', ' ').title()} by Year (Percentage)", "Year", "Percentage")
    else:
        print(f"No data available for column: {col}")
#------------------------------------------------------------------------------------------

# --- Analyze Role Columns ---
for col in role_cols:
    role_counts = {}

    for year, year_df in yearly_data.items():
        if col in year_df.columns:
            counts = year_df[col].dropna().astype(str).value_counts()
            role_counts[year] = counts

    if role_counts:
        # Combine into DataFrame
        df_role_combined = pd.DataFrame(role_counts).fillna(0).astype(int)

        # Standardize order of responses
        all_responses = sorted(set().union(*[df[col].dropna().astype(str).unique()
                                             for y, df in yearly_data.items() if col in df.columns]))
        df_role_combined = df_role_combined.reindex(all_responses).fillna(0).astype(int)

        print(f"\n--- Stacked Bar Plot: {col.replace('_', ' ').title()} ---")
        print(df_role_combined)

        # Stacked count plot
        plot_stacked_bar(df_role_combined, f"{col.replace('_', ' ').title()} by Year", "Year", "Count")

        # Percentage plot
        df_role_percent = df_role_combined.div(df_role_combined.sum(axis=0), axis=1) * 100
        plot_stacked_bar(df_role_percent, f"{col.replace('_', ' ').title()} by Year (Percentage)", "Year", "Percentage")
    else:
        print(f"No data available for column: {col}")
#----------------------------------------------------------------------

# Export the cleaned main dataset
df.to_csv("cleaned_IIACC_data.csv", index=False)

# Participation summary
participation_df.to_csv("participation_summary.csv")

# Feedback averages
feedback_avg_per_year_df.to_csv("feedback_averages.csv")

# Optional: Export categorical summaries
for col in categorical_cols + role_cols:
    col_counts = {}
    for year, year_df in yearly_data.items():
        if col in year_df.columns:
            counts = year_df[col].dropna().astype(str).value_counts()
            col_counts[year] = counts
    if col_counts:
        df_combined = pd.DataFrame(col_counts).fillna(0).astype(int)
        df_combined.to_csv(f"{col}_summary.csv")


