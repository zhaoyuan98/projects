# pylint: disable=no-member
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import numpy as np
import pandas as pd

data = pd.read_csv("06012022A Respiratory Responses.csv", index_col="Email", usecols=[i+1 for i in range(15)])
for row in range(len(data)):
    for col in range(len(data.iloc[0]) - 1):
        data.iloc[:, col+1].iloc[row] = int(data.iloc[:, col+1].iloc[row][0])
ctm_data = data.loc[data["I'm a[n]"] == "Care Team Member"].drop(["I'm a[n]"], axis=1)
obs_data = data.loc[data["I'm a[n]"] == "Observer"].drop(["I'm a[n]"], axis=1)
ins_data = data.loc[data["I'm a[n]"] == "Instructor"].drop(["I'm a[n]"], axis=1)

def calculate_avg(df):
    return [round(df.iloc[:, i].mean(), 3) for i in range(len(df.iloc[0]))]

def get_ctm_scores(email):
    return ctm_data.loc[email].values

ctm_avg = calculate_avg(ctm_data)
obs_avg = calculate_avg(obs_data)
ins_avg = calculate_avg(ins_data)

def area_scores(avg_score):
    sc1 = np.mean(avg_score[0:4])
    sc2 = np.mean(avg_score[4:6])
    sc3 = np.mean(avg_score[6:10])
    sc4 = np.mean(avg_score[10:14])
    return sc1, sc2, sc3, sc4


def plot_score_radar(email, ctm_avg, obs_avg, ins_avg):
    areas = ['Seeking information <br> from the patient', 'Seeking information <br>  from the team', 'Evaluating <br> information', 'Planning and <br> acting on decision']
    cur_scores = get_ctm_scores(email)
    cur_avg_scores = area_scores(cur_scores)
    ctm_avg_scores = area_scores(ctm_avg)
    obs_avg_scores = area_scores(obs_avg)
    ins_avg_scores = area_scores(ins_avg)
    legend = 'Scores of <b>' + email + ' in 4 areas as Care Team Memeber'
    fig = go.Figure()
    areas.append(areas[0])
    fig.add_trace(go.Scatterpolar(
        r=np.append(obs_avg_scores, obs_avg_scores[0]),
        theta=areas,
        fill='none',
        fillcolor='rgba(154, 51, 36, 1)',
        name='<b>Average Observers Score<b>',
    ))

    fig.add_trace(go.Scatterpolar(
        r=np.append(ins_avg_scores, ins_avg_scores[0]),
        theta=areas,
        fill='toself',
        fillcolor='rgba(255, 203, 5, 0.5)',
        name='<b>Instructor Score<b>'
    ))

    fig.add_trace(go.Scatterpolar(
        r=np.append(ctm_avg_scores, ctm_avg_scores[0]),
        theta=areas,
        fill='none',
        fillcolor='rgba(0, 39, 76, 1)',
        name='<b>Average Care Team Score<b>'
    ))

    fig.add_trace(go.Scatterpolar(
        r=np.append(cur_avg_scores, cur_avg_scores[0]),
        theta=areas,
        fill='none',
        fillcolor='rgba(117, 152, 141, 0.55)',
        name=legend
    ))

    fig.update_layout(
        title=legend,
        polar=dict(
        radialaxis=dict(
            visible=True,
            range=[1, 6],
            ),
        angularaxis = dict(
            rotation = 90,
            direction = "clockwise"
            )
        ),
        showlegend=True
    )
    return fig


def plot_response_radar(email, ctm_avg, obs_avg, ins_avg):
    questions = ['Question 1','Question 2','Question 3', 'Question 4', 
                'Question 5', 'Question 6', 'Question 7', 'Question 8', 
                'Question 9', 'Question 10', 'Question 11', 'Question 12', 'Question 13']
    questions.append(questions[0])
    cur_scores = get_ctm_scores(email)
    legend = 'Scores of <b>' + email + ' in 13 questions as Care Team Memeber'
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=np.append(obs_avg, obs_avg[0]),
        theta=questions,
        fill='none',
        fillcolor='rgba(154, 51, 36, 1)',
        name='<b>Average Observers Score<b>'
    ))

    fig.add_trace(go.Scatterpolar(
        r=np.append(ins_avg, ins_avg[0]),
        theta=questions,
        fill='toself',
        fillcolor='rgba(255, 203, 5, 0.5)',
        name='<b>Instructor Score<b>'
    ))

    fig.add_trace(go.Scatterpolar(
        r=np.append(ctm_avg, ctm_avg[0]),
        theta=questions,
        fill='none',
        fillcolor='rgba(117, 152, 141, 0.55)',
        name='<b>Average Care Team Score<b>'
    ))

    fig.add_trace(go.Scatterpolar(
        r=np.append(cur_scores, cur_scores[0]),
        theta=questions,
        fill='none',
        fillcolor='rgba(0, 39, 76, 0.5)',
        name=legend
    ))

    fig.update_layout(
        title=legend,
        polar=dict(
        radialaxis=dict(
            visible=True,
            range=[1, 6]
            ),
        angularaxis = dict(
            rotation = 90,
            direction = "clockwise"
            )
        ),
        showlegend=True
    )
    return fig


#----------------------------------------------------------------------------#
external_stylesheets = [
    {"href": "https://fonts.googleapis.com/css2?"
    "family=Lato:wght@400;700&display=swap",
    "rel": "stylesheet",
    },]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Pulmonary Physiology Case Study (Mr. Kaufmann Scary Extractions)"
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Pulmonary Physiology Case Study (Mr. Kaufmann Scary Extractions)", 
                className="header-title",),
                html.P(children="13 statements related to the care team's medical management of the outpatient with COPD in the simulation exercise that just finished.", 
                className="header-description") 
                ],
                className="header",
                ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Your Group", className="menu-title"),
                        dcc.RadioItems(
                            id = "group-filter",
                            options = ['A', 'B', 'C', 'D', 'E', 'F'],
                            value = 'A',
                            inline=True
                        ),

                        html.Div(children="Your Email", className="menu-title"),
                        dcc.Dropdown(
                            id="email-filter",
                            options=[
                                {"label":email, "value":email}
                                for email in ctm_data.index
                            ],
                            value=ctm_data.index[0],
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),

                html.Div(
                    children=dcc.Graph(
                        id="score-radar",
                        figure=plot_score_radar(ctm_data.index[0], ctm_avg, obs_avg, ins_avg),
                        ),
                        className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="response-radar",
                        figure=plot_response_radar(ctm_data.index[0], ctm_avg, obs_avg, ins_avg),
                        ),
                        className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("score-radar", "figure"), Output("response-radar", "figure")],
    [Input("email-filter", "value")],
)
def update_radar(email):
    new_score_radar = plot_score_radar(email, ctm_avg, obs_avg, ins_avg)
    new_response_radar = plot_response_radar(email, ctm_avg, obs_avg, ins_avg)
    return new_score_radar, new_response_radar

if __name__ == "__main__":
    app.run_server(debug=True)
    