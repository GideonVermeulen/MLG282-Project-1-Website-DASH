import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import tensorflow as tf
import numpy as np
import dash_bootstrap_components as dbc
import os

# Load the model
model = tf.keras.models.load_model('my_model.keras')

# Grade class mapping
grade_mapping = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'F'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, '/static/css/styles.css'])
server = app.server  # for deployment (Gunicorn, etc.)

app.layout = html.Div([
    html.Header([
        html.H1("BrightPath Academy", className="header-title"),
        html.P("Empowering Every Learner’s Journey", className="header-tagline")
    ], className="site-header"),

    html.Section([
        html.Div([
            html.H2("Predict Grade Class", className="section-title"),
            dbc.Form([
                dbc.Row([
                    dbc.Col([dbc.Label("Study Time (Weekly Hours)"), dbc.Input(type="number", min=0, max=20, id="study-time", required=True)]),
                    dbc.Col([dbc.Label("Absences"), dbc.Input(type="number", min=0, max=30, id="absences", required=True)]),
                    dbc.Col([dbc.Label("Tutoring Status"), dcc.RadioItems(options=[{"label": "Yes", "value": "Yes"}, {"label": "No", "value": "No"}], id="tutoring-status", inline=True)])
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col([dbc.Label("Parental Involvement"), dcc.Dropdown(id="parental-involvement", options=[{"label": "None", "value": 0}, {"label": "Low", "value": 1}, {"label": "Moderate", "value": 2}, {"label": "High", "value": 3}, {"label": "Very High", "value": 4}], placeholder="Select level")]),
                    dbc.Col([dbc.Label("Extracurricular Activities?"), dcc.RadioItems(options=[{"label": "Yes", "value": "Yes"}, {"label": "No", "value": "No"}], id="extracurricular", inline=True)]),
                    dbc.Col([dbc.Label("Participating in Sports?"), dcc.RadioItems(options=[{"label": "Yes", "value": "Yes"}, {"label": "No", "value": "No"}], id="sport", inline=True)]),
                    dbc.Col([dbc.Label("Participating in Music?"), dcc.RadioItems(options=[{"label": "Yes", "value": "Yes"}, {"label": "No", "value": "No"}], id="music", inline=True)])
                ], className="mb-3"),

                dbc.Button("Predict GradeClass", id="predict-btn", color="primary", className="mt-3"),
            ]),

            html.Div(id="prediction-result", className="alert-box mt-4")
        ], className="card-container")
    ], className="section-container"),

    html.Footer([
        html.P("© 2025 BrightPath Academy. All rights reserved."),
        html.P("Contact us: info@brightpath.academy | +1 (555) 123-4567")
    ], className="site-footer")
])

@app.callback(
    Output("prediction-result", "children"),
    Input("predict-btn", "n_clicks"),
    State("study-time", "value"),
    State("absences", "value"),
    State("tutoring-status", "value"),
    State("parental-involvement", "value"),
    State("extracurricular", "value"),
    State("sport", "value"),
    State("music", "value"),
    prevent_initial_call=True
)
def make_prediction(n_clicks, study_time, absences, tutoring, parental, extracurricular, sport, music):
    try:
        tutoring = 1 if tutoring == "Yes" else 0
        extracurricular = 1 if extracurricular == "Yes" else 0
        sport = 1 if sport == "Yes" else 0
        music = 1 if music == "Yes" else 0

        input_data = np.array([[study_time, absences, tutoring, parental, extracurricular, sport, music]])
        result = model.predict(input_data)
        predicted_class = int(np.argmax(result, axis=1)[0])
        grade = grade_mapping.get(predicted_class, "Unknown")
        return dbc.Alert(f"Predicted Grade Class: {grade}", color="info")
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
