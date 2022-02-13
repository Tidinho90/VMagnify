from dash import Dash, html, dcc
import base64

app = Dash(__name__)
LOGO_FILENAME = "static/img/logo/VMagnify30.png"
DEFAULT_URL = "https://commons.wikimedia.org/wiki/File:Lions_Family_Portrait_Masai_Mara.jpg"
encoded_image = base64.b64encode(open(LOGO_FILENAME, 'rb').read())

app.layout = html.Div(
    children=[
        html.Img(
            src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style={
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
                "width": "15%",
                "height": "15%",
            }
        ),
        html.Label("URL"),
        dcc.Input(
            id="picture_url",
            type="url",
            size="100",
            value=DEFAULT_URL
        ),
        html.Button(
            "Submit URL",
            id="submit_url"
        ),
        dcc.Upload(
            "Submit Picture",
            id="submit_picture",
            multiple=False
        ),
        dcc.Slider(
            id="picture_zoom",
            min=1,
            value=1,
            max=4,
            step=1
        ),
        html.Img(
            id="displayed_picture"
        ),
        dcc.Input(
            id="picture_infos",
            type="text",
            readOnly=True
        )
    ]
)
if __name__ == "__main__":
    app.run_server(debug=True)
