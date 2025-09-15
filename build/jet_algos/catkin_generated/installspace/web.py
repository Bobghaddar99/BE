#!/usr/bin/env python3

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import rospy
from std_msgs.msg import String
import threading

cmd = 0

# Initialize the Dash app
app = dash.Dash(__name__)

# Initialize ROS node
rospy.init_node('dash_button_node', anonymous=True)
# Create a publisher to the 'button_clicks' topic
pub = rospy.Publisher('button_clicks', String, queue_size=10)

# Function to call when Button 1 is pressed
def button_1_function():
    global cmd
    if cmd % 2 == 0:
        rospy.set_param("joystick", 1)
        rospy.loginfo("Joystick set to 1 (on)")
    else:
        rospy.set_param("joystick", 0)
        rospy.loginfo("Joystick set to 0 (off)")
    cmd += 1
    return f"Joystick {'on' if cmd % 2 == 1 else 'off'}"

# Function to call when Button 2 is pressed
def button_2_function():
    msg = "Automapping started"
    rospy.loginfo(msg)
    pub.publish(msg)
    return msg

# Function to call when Lifting Option 1 is pressed
def lifting_button_1_function():
    msg = "Lifting Option 1 pressed"
    rospy.loginfo(msg)
    pub.publish(msg)
    return msg

# Function to call when Lifting Option 2 is pressed
def lifting_button_2_function():
    msg = "Lifting Option 2 pressed"
    rospy.loginfo(msg)
    pub.publish(msg)
    return msg

# App layout
app.layout = html.Div([
    html.H1("Dash with ROS Integration", style={'textAlign': 'center', 'color': 'teal'}),

    # Main buttons with background images
    html.Div([
        html.Button("", id="button-1", n_clicks=0, style={
            'backgroundImage': 'url("/static/joystick.png")',  # Set background image
            'backgroundSize': 'contain',  # Ensure the entire image is visible
            'backgroundPosition': 'center',  # Center the image
            'backgroundRepeat': 'no-repeat',  # Don't repeat the image
            'color': 'white', 'padding': '10px 20px', 
            'border': 'none', 'borderRadius': '5px', 'fontSize': '16px', 
            'cursor': 'pointer', 'margin': '5px', 'height': '150px', 'width': '200px'}),

        html.Button("", id="button-2", n_clicks=0, style={
            'backgroundImage': 'url("/static/robot.png")',  # Set background image
            'backgroundSize': 'contain',  # Ensure the entire image is visible
            'backgroundPosition': 'center',  # Center the image
            'backgroundRepeat': 'no-repeat',  # Don't repeat the image
            'color': 'white', 'padding': '10px 20px', 
            'border': 'none', 'borderRadius': '5px', 'fontSize': '16px', 
            'cursor': 'pointer', 'margin': '5px', 'height': '150px', 'width': '200px'}),

        # Lifting button as a picture
        html.Button("", id="lifting-button", n_clicks=0, style={
            'backgroundImage': 'url("/static/lifting.png")',  # Set background image
            'backgroundSize': 'contain',  # Ensure the entire image is visible
            'backgroundPosition': 'center',  # Center the image
            'backgroundRepeat': 'no-repeat',  # Don't repeat the image
            'color': 'white', 'padding': '10px 20px', 
            'border': 'none', 'borderRadius': '5px', 'fontSize': '16px', 
            'cursor': 'pointer', 'margin': '5px', 'height': '150px', 'width': '200px'})
    ], style={'textAlign': 'center', 'marginBottom': '50px'}),

    # New buttons that appear only when "Lifting" is pressed
    html.Div(id="lifting-buttons", children=[
        html.Button("", id="lifting-button-1", n_clicks=0, style={
            'backgroundImage': 'url("/static/up.png")',  # Set background image
            'backgroundSize': 'contain',  # Ensure the entire image is visible
            'backgroundPosition': 'center',  # Center the image
            'backgroundRepeat': 'no-repeat',  # Don't repeat the image
            'color': 'white', 'padding': '10px 20px', 
            'border': 'none', 'borderRadius': '5px', 'fontSize': '16px', 
            'cursor': 'pointer', 'margin': '5px', 'height': '150px', 'width': '200px'}),
        html.Button("", id="lifting-button-2", n_clicks=0, style={
            'backgroundImage': 'url("/static/down.png")',  # Set background image
            'backgroundSize': 'contain',  # Ensure the entire image is visible
            'backgroundPosition': 'center',  # Center the image
            'backgroundRepeat': 'no-repeat',  # Don't repeat the image
            'color': 'white', 'padding': '10px 20px', 
            'border': 'none', 'borderRadius': '5px', 'fontSize': '16px', 
            'cursor': 'pointer', 'margin': '5px', 'height': '150px', 'width': '200px'})
    ], style={'textAlign': 'center', 'display': 'none'}),  # Initially hidden

    # Output area
    html.Div(id="output", style={'marginTop': '20px', 'textAlign': 'center'})
])

# Callback to toggle the visibility of the additional buttons when "Lifting" is pressed
@app.callback(
    Output("lifting-buttons", "style"),
    [Input("lifting-button", "n_clicks")],
    [State("lifting-buttons", "style")]
)
def toggle_lifting_buttons(n_clicks, style):
    if n_clicks % 2 == 1:  # Show additional buttons
        return {'textAlign': 'center', 'display': 'block'}
    else:  # Hide additional buttons
        return {'textAlign': 'center', 'display': 'none'}

# Callback to update the output based on button clicks
@app.callback(
    Output("output", "children"),
    [Input("button-1", "joy"),
     Input("button-2", "doc"),
     Input("lifting-button-1", "up"),
     Input("lifting-button-2", "down")]
)
def update_output(n_clicks1, n_clicks2, lifting_button1, lifting_button2):
    if n_clicks1 > 0:
        return button_1_function()
    elif n_clicks2 > 0:
        return button_2_function()
    elif lifting_button1 > 0:
        return lifting_button_1_function()
    elif lifting_button2 > 0:
        return lifting_button_2_function()
    return "No button clicked yet."

# Run the app and allow access from the local network
if __name__ == '__main__':
    def run_dash():
        app.run_server(host='0.0.0.0', port=8050, debug=True, use_reloader=False)

    def run_ros():
        rospy.spin()

    threading.Thread(target=run_dash).start()
    threading.Thread(target=run_ros).start()
