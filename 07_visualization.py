import sqlite3
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.express as px

# Function to convert timestamps into numeric days ago
def convert_to_days_ago(timestamp, reference_date):
    num, unit = timestamp.split()[:2]
    num = int(num)
    if 'day' in unit:
        return num
    elif 'hour' in unit:
        return num / 24
    elif 'week' in unit:
        return num * 7
    elif 'month' in unit:
        return num * 30
    elif 'year' in unit:
        return num * 365
    return 0

# Number of intervals to divide the data into
number_of_intervals = 5

reference_date = datetime.now()

# Connect to the SQLite database
conn = sqlite3.connect('comments.db')
cursor = conn.cursor()

# Fetch all comments from the database
cursor.execute("SELECT timestamp, positive, negative, angry, spam, response_required FROM comments")
comments = cursor.fetchall()

conn.close()

# Convert timestamps to days ago and find the min and max to establish the range
days_ago_list = [convert_to_days_ago(comment[0], reference_date) for comment in comments]
min_days_ago, max_days_ago = min(days_ago_list), max(days_ago_list)

# Set interval size to 50 days
interval_size = 50

# Function to assign each comment to an interval
def assign_to_interval(days_ago, interval_size):
    return f"{int((days_ago // interval_size) * interval_size)}-{int((days_ago // interval_size) * interval_size + interval_size)} days ago"

# Aggregate comments into intervals and categories
data = {'Interval': [], 'Category': [], 'Count': []}
for comment in comments:
    days_ago = convert_to_days_ago(comment[0], reference_date)
    interval = assign_to_interval(days_ago, interval_size)
    for i, category in enumerate(['Positive', 'Negative', 'Angry', 'Spam', 'Response Required']):
        if comment[i + 1]:
            data['Interval'].append(interval)
            data['Category'].append(category)
            data['Count'].append(1)

df = pd.DataFrame(data)

# Aggregate and pivot the data
df_aggregated = df.groupby(['Interval', 'Category']).sum().reset_index()
df_pivoted = df_aggregated.pivot(index='Interval', columns='Category', values='Count').fillna(0)

# Convert the intervals to numeric values
df_pivoted.index = df_pivoted.index.map(lambda x: int(x.split('-')[0]))

# Sort the DataFrame by its index in ascending order
df_pivoted = df_pivoted.sort_index(ascending=True)

# Convert the intervals back to strings
df_pivoted.index = df_pivoted.index.map(lambda x: f"{x}-{x+50} days ago")

# Convert the pivoted DataFrame back to a long format for plotting with px.bar
df_long = df_pivoted.reset_index().melt(id_vars='Interval', var_name='Category', value_name='Count')

fig = go.Figure()
for category in df_aggregated['Category'].unique():
    fig.add_trace(go.Bar(
        x=df_pivoted.index,
        y=df_pivoted[category],
        name=category
    ))

fig = px.bar(df_long, 
             x='Interval', 
             y='Count', 
             color='Category', 
             title='Number of Comments by Category Over Time', 
             labels={'Count':'Number of Comments', 'Interval':'Time Interval'}, 
             color_discrete_sequence=px.colors.qualitative.Pastel1)

fig.update_layout(
    barmode='stack',
    legend_title='Comment Categories'
)

fig.show()