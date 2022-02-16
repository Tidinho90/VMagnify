from dash import Dash, html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import base64

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
LOGO_FILENAME = "static/img/logo/VMagnify30.png"
DEFAULT_URL = "https://commons.wikimedia.org/wiki/File:Lions_Family_Portrait_Masai_Mara.jpg"
DEFAULT_FILENAME = "static/img/example/Lions_Family_Portrait_Masai_Mara.jpg"
logo_encoded = base64.b64encode(open(LOGO_FILENAME, 'rb').read())

app.layout = html.Div(
    [
        html.Img(
            src='data:image/png;base64,{}'.format(logo_encoded.decode()),
            style={
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
                "width": "15%",
                "height": "15%",
            }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            html.Div(
                                html.Label(
                                    "URL"
                                )
                            )
                        ),
                        dbc.Row(
                            html.Div(
                                dcc.Input(
                                    id="picture_url",
                                    type="url",
                                    size="100",
                                    value=DEFAULT_URL
                                )
                            )
                        ),
                        dbc.Row(
                            html.Div(
                                html.Button(
                                    "Submit URL",
                                    id="submit_url"
                                )
                            )
                        ),
                        dbc.Row(
                            html.Div(
                                dcc.Upload(
                                    id='upload_picture',
                                    children=html.Div(
                                        [
                                            'Drag and Drop picture or ',
                                            html.A('Select Files')
                                        ]
                                    ),
                                    style={
                                        'width': '100%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    },
                                )
                            )
                        ),
                        dbc.Row(
                            html.Div(
                                daq.Slider(
                                    id="picture_zoom",
                                    min=1,
                                    max=4,
                                    value=1,
                                    handleLabel={
                                        "showCurrentValue": True,
                                        "label": "UPSCALE"
                                    },
                                    step=1,
                                    labelPosition='bottom',
                                    marks={
                                        '1': '1x',
                                        '2': '2x',
                                        '3': '3x',
                                        '4': '4x'
                                    }
                                )
                            )
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            html.Div(
                                html.Img(
                                    id="displayed_picture",
                                    src=DEFAULT_FILENAME
                                )
                            )
                        ),
                        dbc.Row(
                            html.Div(
                                dcc.Input(
                                    id="picture_infos",
                                    type="text",
                                    readOnly=True
                                )
                            )
                        )
                    ]
                )
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
