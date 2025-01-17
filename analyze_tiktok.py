import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def analyze_tiktok_data(selected_metric='diggCount'):
    # Path to the dataset
    file_path = 'files/dataset_free-tiktok-scraper_2024-09-04_14-57-00-312.csv'

    # Read the CSV file
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # Ensure the necessary columns are present
    required_columns = ['createTimeISO', 'diggCount', 'commentCount', 'collectCount', 'playCount', 'shareCount']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("CSV file must contain 'createTimeISO', 'diggCount', 'commentCount', 'collectCount', 'playCount', and 'shareCount' columns.")
    
    # Convert 'createTimeISO' column to datetime
    df['date'] = pd.to_datetime(df['createTimeISO'])
    
    # Sort the data by date
    df = df.sort_values(by='date')
    
    # Compute cumulative sums for each metric
    for metric in ['diggCount', 'commentCount', 'collectCount', 'playCount', 'shareCount']:
        df[f'cumulative_{metric}'] = df[metric].cumsum()
    
    # Calculate cumulative total insights
    df['total_insights'] = (
        df['cumulative_diggCount'] +
        df['cumulative_commentCount'] +
        df['cumulative_collectCount'] +
        df['cumulative_playCount'] +
        df['cumulative_shareCount']
    )

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces for each metric
    metrics = {
        'cumulative_diggCount': {'name': 'Total Likes', 'color': 'blue'},
        'cumulative_commentCount': {'name': 'Total Commentsa', 'color': 'green'},
        'cumulative_collectCount': {'name': 'Total Saves', 'color': 'red'},
        'cumulative_playCount': {'name': 'Total Plays', 'color': 'orange'},
        'cumulative_shareCount': {'name': 'Total Shares', 'color': 'purple'},
        'total_insights': {'name': 'Total Insights', 'color': 'red'}
    }
    
    for metric, info in metrics.items():
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df[metric],
            mode='lines+markers',  # Ensure lines are connected
            name=info['name'],
            line=dict(color=info['color'])
        ))

    # Update layout with range slider and dropdown for y-axis selection
    fig.update_layout(
        title={
            'text': "Cumulative TikTok Engagement Growth Over Time",
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        xaxis_title='Date',
        yaxis_title='Cumulative Counts',
        xaxis=dict(
            tickformat='%b %d, %Y',
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=6, label='6m', step='month', stepmode='backward'),
                    dict(count=1, label='YTD', step='year', stepmode='todate'),
                    dict(label='All', step='all')
                ])
            ),
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(
            title='Cumulative Counts',
            rangemode='tozero'  # This ensures that the y-axis starts at zero
        ),
        template='plotly_dark'
    )

    # Set default view to the selected metric
    fig.update_traces(visible='legendonly')  # Hide all traces by default
    if f'cumulative_{selected_metric}' in metrics:
        fig.update_traces(selector=dict(name=metrics[f'cumulative_{selected_metric}']['name']), visible=True)

    # Save the plot to a file or return the figure to display in your application
    fig.write_html('tiktok_engagement.html')
    return fig