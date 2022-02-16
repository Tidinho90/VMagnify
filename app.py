import base64
from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_daq as daq
import dash_bootstrap_components as dbc
from vmagnify.vmagnify_picture import VMagnifyPicture

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
LOGO_FILENAME = "static/img/logo/VMagnify30.png"
DEFAULT_URL = "https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/images/input.png"
DEFAULT_FILENAME = "static/img/example/Lions_Family_Portrait_Masai_Mara.jpg"
logo_encoded = base64.b64encode(open(LOGO_FILENAME, 'rb').read())
vmagnify = VMagnifyPicture()

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


@app.callback(
    Output(component_id='displayed_picture', component_property='src'),
    Output(component_id='picture_infos', component_property='value'),
    Input(component_id='submit_url', component_property='n_clicks'),
    State(component_id='picture_url', component_property='value'),
    Input(component_id='picture_zoom', component_property='value'),
    Input(component_id='upload_picture', component_property='contents'),
    State(component_id='upload_picture', component_property='filename'),
    State(component_id='upload_picture', component_property='last_modified')
)
def process(submit_url, picture_url, picture_zoom, upload_picture_contents, upload_picture_filename, upload_picture_last_modified):
    """ process the inputs, because we use the same outputs, we have to use a shared callback """
    ctx = callback_context
    # ctx variable permits to know which input triggered
    if not ctx.triggered:
        return vmagnify.get_picture_data(picture_zoom-1)
    else:
        triggered_item = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_item == "submit_url":
        return vmagnify.process_url(picture_url)
    elif triggered_item == "picture_zoom":
        return vmagnify.get_picture_data(picture_zoom-1)
#    elif triggered_item == "upload_picture":
#        return vmagnify.process_uploaded_picture(upload_picture_contents, upload_picture_filename)


if __name__ == "__main__":
    app.run_server(debug=True)
