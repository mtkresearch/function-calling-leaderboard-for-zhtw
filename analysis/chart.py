import argparse

import pandas as pd
import plotly.graph_objects as go
from matplotlib import cm
from matplotlib.colors import to_rgba

# Define the number of variables and categories
categories = [
    'Irrelevance Detection', 
    'Simple (AST)', 'Multiple (AST)', 'Parallel (AST)', 'Parallel Multiple (AST)', 
    'Simple (Exec)', 'Multiple (Exec)', 'Parallel (Exec)', 'Parallel Multiple (Exec)'
]
cols_of_score = [
    'Relevance Detection',
    'Simple Function AST', 'Multiple Functions AST', 'Parallel Functions AST', 'Parallel Multiple AST',
    'Simple Function Exec', 'Multiple Functions Exec', 'Parallel Functions Exec', 'Parallel Multiple Exec'
]

N = len(categories)

def generate_colors(num_colors):
    """
    Generate a list of distinct colors.
    Args:
        num_colors (int): Number of colors to generate.
    Returns:
        List of RGBA color strings.
    """
    colormap = cm.get_cmap('tab20', num_colors)  # 'tab20' is a colormap with 20 distinct colors
    colors = [to_rgba(colormap(i), alpha=0.5) for i in range(num_colors)]
    return ['rgba({:.0f}, {:.0f}, {:.0f}, {:.2f})'.format(r*255, g*255, b*255, a) for r, g, b, a in colors]

def create_radar_chart(models, model_names, out_png):
    """
    Create a radar chart from the provided model scores.
    Args:
        models (list): A list of model scores.
    """
    # Prepare the figure
    fig = go.Figure()

    num_models = len(models)
    colors = generate_colors(num_models)
    if not model_names:
        model_names = [f'Model {i+1}' for i in range(num_models)]

    for idx, model in enumerate(models):
        model += model[:1]  # Close the radar chart
        fig.add_trace(go.Scatterpolar(
            r=model,
            theta=categories + categories[:1],
            fill=None,
            name=model_names[idx],
            fillcolor=colors[idx]
        ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=10  # Set the interval to 10
            )),
        showlegend=True,
        width=1200,  # Increase the width
        height=800  # Increase the height
    )

    #fig.show()
    fig.write_image(out_png)
    print(f"{out_png} has been created and saved in your current directory")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--score_csv", type=str, default="./score/zhtw/data.csv")
    parser.add_argument("--out_chart", type=str, default='./score/zhtw/radar_chart.png')
    args = parser.parse_args()

    df = pd.read_csv(args.score_csv)
    models, model_names = [], []
    for _, row in df.sort_values('Model').iterrows():
        scores = [float(row[col].replace('%', '')) for col in cols_of_score]
        models.append(scores)
        model_names.append(row['Model'])

    create_radar_chart(models, model_names, out_png=args.out_chart)
