import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import tempfile
import os
import whisper  # Make sure whisper library is imported correctly

import base64
import io

UPLOAD_FOLDER = tempfile.mkdtemp(dir=os.getcwd())
OUTPUT_OBJECT = "translation.txt"

# Define instructions and error messages
instr = [
    [html.B("1. UPLOAD .MP3: "), "Click on the Drag and Drop box below"],
    [html.B("2. TRANSLATE: "), "Click 'Translate'. You should see a spinner indicating that the file is being translated."],
    [html.B("3. DOWNLOAD TRANSLATION: "), "Once the analysis is finished, click on the button 'Download' to get the results as a .txt file."]
]

# Save the uploaded file
def save_uploaded_file(contents, filename, folder=UPLOAD_FOLDER):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    file_path = os.path.join(folder, filename)
    with open(file_path, 'wb') as f:
        f.write(decoded)
    return file_path

def translate_file(file_path):
    model = whisper.load_model('medium')
    results = model.transcribe(file_path, language="no", task="translate")
    with open(OUTPUT_OBJECT, "w", encoding="utf-8") as txt:
        txt.write(results["text"])  # Make sure 'results' variable is used

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Whisper User Interface'

app.layout = html.Div([
    html.H1('Whisper Translation Dashboard'),
    dbc.Alert(
        [
            html.Ul(
                id="instructions",
                children=[html.P([html.B(instr[i][0]), instr[i][1]]) for i in range(len(instr))],
                className="list-unstyled mb-0",
            )
        ],
        color="primary",
        className="mb-4",
    ),
    dcc.Upload(
        id='folder-upload',
        children=html.Div(['Drag and Drop or ', html.A('Select files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
        },
        multiple=False
    ),
    dbc.Button('Translate', id='analyze-button', n_clicks=0, color="primary", className="mr-2"),
    dbc.Button('Download', id="download-button", n_clicks=0, color="success"),
    dcc.Loading(id="loading", children=[html.Div(id='results-output')], type="cube", fullscreen=True),
    dcc.Download(id="download-txt"),
    html.Div(id='info-msg'),
    html.Div(id='alert-message-db')
])

@app.callback(
    Output('folder-upload', 'style'),
    Input('folder-upload', 'contents')
)
def update_upload_box_style(contents):
    if contents:
        # If a file is uploaded, change box color to green
        return {
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'backgroundColor': 'lightgreen'   # Or any color you prefer
        }
    else:
        # Default style without file
        return {
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }

# Callback Function Modification for File Handling
@app.callback(
    [Output('results-output', 'children'),
     Output('info-msg', 'children')],
    [Input('analyze-button', 'n_clicks')],
    [State('folder-upload', 'contents'),
     State('folder-upload', 'filename')]
)
def analyze_file(n_clicks, content, filename):
    if n_clicks > 0:
        if not filename or not content:
            return "", dbc.Alert("No file uploaded!", color="danger")
        file_path = save_uploaded_file(content, filename)
        if os.path.exists(file_path):
            translate_file(file_path)
            return html.Div("File has been translated successfully!"), ""
        else:
            return "", dbc.Alert(f"File not found at path: {file_path}", color="danger")
    return "", ""

@app.callback(
    [Output('download-txt', 'data'),
     Output('alert-message-db', 'children')],
    [Input('download-button', 'n_clicks')]
)
def dl_txt(n_clicks):
    if n_clicks > 0:
        if os.path.exists(OUTPUT_OBJECT):
            return dcc.send_file(OUTPUT_OBJECT), ""
        else:
            return None, dbc.Alert("Translation file not found!", color="danger")
    return None, ""
    
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8999, debug=True)
