import sys
import ast
import plotly.graph_objects as go
from matplotlib import cm
from matplotlib.colors import to_rgba

# Define the number of variables and categories
categories = ['Irelevance Detection', 'Simple (AST)', 'Multiple (AST)', 'Parallel (AST)', 
              'Parallel Multiple (AST)', 'Simple (Exec)', 'Multiple (Exec)', 'Parallel (Exec)', 'Parallel Multiple (Exec)']
N = len(categories)

def parse_input(args):
    """
    Parse the command line input to extract model scores.
    Args:
        args (list): List of command line arguments (scores).
    Returns:
        List of model scores.
    """
    models = []
    for arg in args[1:]:
        try:
            # Convert the string representation of the list to an actual list
            model_scores = ast.literal_eval(arg)
            if isinstance(model_scores, list) and len(model_scores) == N:
                models.append(model_scores)
            else:
                print(f"Warning: Invalid input format or incorrect number of scores for a model: {arg}")
        except (ValueError, SyntaxError) as e:
            print(f"Error: Failed to parse input for model scores: {arg}. {e}")
    return models

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

def create_radar_chart(models):
    """
    Create a radar chart from the provided model scores.
    Args:
        models (list): A list of model scores.
    """
    # Prepare the figure
    fig = go.Figure()

    num_models = len(models)
    colors = generate_colors(num_models)
    model_names = [f'Model {i+1}' for i in range(num_models)]

    for idx, model in enumerate(models):
        model += model[:1]  # Close the radar chart
        fig.add_trace(go.Scatterpolar(
            r=model,
            theta=categories + categories[:1],
            fill='toself',
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
        width=900,  # Increase the width
        height=900  # Increase the height
    )

    #fig.show()
    fig.write_image("radar_chart.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [Model 1 Scores] [Model 2 Scores] ...")
        print(f"Each model should have exactly {N} scores enclosed in a list.")
    else:
        models = parse_input(sys.argv)
        if models:
            create_radar_chart(models)
            print("radar_chart.png has been created and saved in your current directory")
