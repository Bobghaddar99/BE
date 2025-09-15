import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import random
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to load the CSV data
def load_csv():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
    else:
        # If the CSV file doesn't exist, create a new one with headers
        df = pd.DataFrame(columns=['mpa name', 'room', 'pose'])
        df.to_csv('data.csv', index=False)
    return df

# Function to generate random data and save it to CSV
def generate_random_data(num_rooms=10):
    room_data = []
    for i in range(num_rooms):
        room_name = f"room{random.randint(1, 100)}"  # Random room name
        pose = f"({random.uniform(-10, 10):.2f}, {random.uniform(-10, 10):.2f}, {random.uniform(-10, 10):.2f})"  # Random pose
        room_data.append({
            'mpa name': f"map{random.randint(1, 5)}",  # Random map name (map1, map2, etc.)
            'room': room_name,
            'pose': pose
        })
    
    return room_data

# Layout of the app with buttons to load room data and add new room
app.layout = html.Div([
    html.Button("Load Room Data", id="load-button", n_clicks=0),
    html.Button("Add New Room", id="add-room-button", n_clicks=0),
    html.Div(id="room-buttons-container"),  # Container for dynamic room buttons
])

# Combined callback to update room buttons and handle adding new rooms
@app.callback(
    Output("room-buttons-container", "children"),
    Input("load-button", "n_clicks"),
    Input("add-room-button", "n_clicks"),
    prevent_initial_call=True
)
def update_room_buttons(load_clicks, add_clicks):
    # Load the current data from CSV
    df = load_csv()
    
    # Check which button was clicked using callback context
    ctx = dash.callback_context
    if not ctx.triggered:
        return []

    # If the "Add New Room" button was clicked
    if ctx.triggered[0]['prop_id'] == 'add-room-button.n_clicks':
        # Generate random room data and append to the CSV
        new_room = {
            'mpa name': f"map{random.randint(1, 5)}",
            'room': f"room{len(df) + 1}",
            'pose': f"({random.uniform(-10, 10):.2f}, {random.uniform(-10, 10):.2f}, {random.uniform(-10, 10):.2f})"
        }
        df = df.append(new_room, ignore_index=True)
        df.to_csv('data.csv', index=False)

    # Generate buttons for each room from the updated data
    room_buttons = [html.Button(f"Room: {row['room']}", id=f"room-button-{index}") for index, row in df.iterrows()]
    
    return room_buttons

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
