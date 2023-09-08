

import plotly.graph_objects as go
import pandas as pd

def read_all_files(file_list, columns):
    all_data = []
    
    for file_path in file_list:
        df = pd.read_csv(file_path, usecols=columns)
        all_data.append(df)
    
    return all_data


file_list = ['finalresults-1.csv', 'finalresults-2.csv', 'finalresults-3.csv',
'finalresults-4.csv', 'finalresults-5.csv', 'finalresults-6.csv',
'finalresults-7.csv', 'finalresults-8.csv', 'finalresults-7.csv',
'finalresults-10.csv']
columns = ['yield_mz','yield_sb','yield_wh']
all_data = read_all_files(file_list, columns)

# ...

# Create a figure
fig = go.Figure()

# Create frames for the animation, each showing only one dataset
frames = [go.Frame(
    data=[go.Scatter3d(
        x=data['yield_mz'],
        y=data['yield_sb'],
        z=data['yield_wh'],
        mode='markers',
        marker=dict(
            size=5,
            color=index,  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
        )
    )]) for index, data in enumerate(all_data)
]

# Adding frames to the figure
fig.frames = frames

# Adding data for the first frame
fig.add_trace(go.Scatter3d(
    x=all_data[0]['yield_mz'],
    y=all_data[0]['yield_sb'],
    z=all_data[0]['yield_wh'],
    mode='markers',
    marker=dict(
        size=5,
        color=0,  # set color to an array/list of desired values
        colorscale='Viridis',  # choose a colorscale
        opacity=0.8
    )
))

# Define the animation settings
animation_settings = {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True, "transition": {"duration": 300}}

# Define the play and pause buttons
play_button = {
    "label": "Play",
    "method": "animate",
    "args": [None, animation_settings]
}

pause_button = {
    "label": "Pause",
    "method": "animate",
    "args": [
        [None], 
        {
            "frame": {"duration": 0, "redraw": False}, 
            "mode": "immediate", 
            "transition": {"duration": 0}
        }
    ]
}

# Update the layout to include the animation controls
fig.update_layout(
    updatemenus=[
        {
            "type": "buttons",
            "x": 1.05,
            "y": 1.2,
            "buttons": [play_button, pause_button],
        }
    ],
)

# Set the titles and labels
fig.update_layout(scene=dict(xaxis_title='Yield MZ', yaxis_title='Yield SB', zaxis_title='Yield WH'),
                  title="3D Scatter Plot Animation")

# Show the plot
fig.show()
