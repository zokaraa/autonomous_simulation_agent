import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_interactive_plots(summary_csv, output_dir):
    """Generate interactive plots for further data analysis."""
    # Load the summary CSV file
    summary_df = pd.read_csv(summary_csv)
    
    # Extract the scaling exponent before modifying the DataFrame
    scaling_exponent_row = summary_df[summary_df['N'] == 'Scaling exponent v']
    if len(scaling_exponent_row) != 1:
        raise ValueError("Scaling exponent row is missing or duplicated in the summary CSV.")
    
    scaling_exponent = float(scaling_exponent_row['h2(N)'].values[0])
    
    # Remove the scaling exponent row from DataFrame
    summary_df = summary_df[summary_df['N'] != 'Scaling exponent v']
    
    # Convert 'N' column to numeric
    summary_df['N'] = pd.to_numeric(summary_df['N'])
    
    # Extracting necessary columns
    N_values = summary_df['N']
    h2_values = summary_df['h2(N)']

    # Interactive scatter plot for h2(N) vs N
    scatter_fig = px.scatter(
        summary_df, 
        x='N', 
        y='h2(N)', 
        title='Mean Squared End-to-End Distance (h2(N)) vs N',
        labels={'N': 'Number of Segments (N)', 'h2(N)': 'Mean Squared End-to-End Distance (h2(N))'}
    )
    scatter_fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
    scatter_fig.write_html(os.path.join(output_dir, 'h2_vs_N_interactive.html'))
    
    # Adding trendline
    trendline_fig = go.Figure(data=scatter_fig.data)
    trendline_fig.add_trace(go.Scatter(
        x=N_values, 
        y=N_values ** scaling_exponent,
        mode='lines',
        name=f'Trendline: h2(N) ~ N^{scaling_exponent:.4f}'
    ))
    trendline_fig.update_layout(title='h2(N) vs N with Scaling Exponent Trendline')
    trendline_fig.write_html(os.path.join(output_dir, 'h2_vs_N_with_trendline.html'))

    print(f"Interactive plots created at: {output_dir}")

def main():
    extracted_dir = 'extracted_results'
    summary_csv = os.path.join(extracted_dir, 'summary.csv')
    output_dir = 'interactive_plots'
    
    # Create output directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create interactive plots
    create_interactive_plots(summary_csv, output_dir)

if __name__ == "__main__":
    main()
