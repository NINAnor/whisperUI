import base64
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import tempfile
import os
import whisper  
import torch
import io

UPLOAD_FOLDER = tempfile.mkdtemp(dir=os.getcwd())
OUTPUT_TRANSLATION_OBJECT = "translation.srt"
OUTPUT_TRANSCRIPTION_OBJECT = "transcription.srt"

# Define instructions and error messages
instr = [
    [html.B("1. UPLOAD .MP3: "), "Click on the Drag and Drop box below"],
    [html.B("2. ANALYZE: "), "Click 'Analyze'. You should see a spinner indicating that the file is being translated."],
    [html.B("3. DOWNLOAD: "), "Once the analysis is finished, click on the button 'Download transcription' or 'Download translation' to get the results as a .srt file."]
]

# Save the uploaded file
def save_uploaded_file(contents, filename, folder=UPLOAD_FOLDER):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    file_path = os.path.join(folder, filename)
    with open(file_path, 'wb') as f:
        f.write(decoded)
    return file_path

from typing import Iterator, TextIO

def srt_format_timestamp(seconds: float):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    return (f"{hours}:") + f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def write_srt(transcript: Iterator[dict], file: TextIO):
    count = 0
    for segment in transcript:
        count +=1
        print(
            f"{count}\n"
            f"{srt_format_timestamp(segment['start'])} --> {srt_format_timestamp(segment['end'])}\n"
            f"{segment['text'].replace('-->', '->').strip()}\n",
            file=file,
            flush=True,
        )


def translate_transcribe_file(file_path):

    model = whisper.load_model('medium', device="cuda" if torch.cuda.is_available() else "cpu")
    translation = model.transcribe(file_path, language="no", task="translate")
    transcription = model.transcribe(file_path, language="no")

    # Save translation
    with open(OUTPUT_TRANSLATION_OBJECT, "w", encoding="utf-8") as txt:
        #txt.write(translation["text"])
         write_srt(translation["segments"], txt)

    # Save transcription
    with open(OUTPUT_TRANSCRIPTION_OBJECT, "w", encoding="utf-8") as txt:
        #txt.write(transcription["text"])
        write_srt(transcription["segments"], txt)


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
    dbc.Button('Analyze', id='analyze-button', n_clicks=0, color="primary", className="mr-2"),
    dbc.Button('Download Translation', id="download-translation-button", n_clicks=0, color="success"),
    dbc.Button('Download Transcription', id="download-transcription-button", n_clicks=0, color="success", className="ml-2"),
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
            translate_transcribe_file(file_path)
            return html.Div("File has been analyzed successfully!"), ""
        else:
            return "", dbc.Alert(f"File not found at path: {file_path}", color="danger")
    return "", ""

@app.callback(
    [Output('download-txt', 'data'),
     Output('alert-message-db', 'children')],
    [Input('download-translation-button', 'n_clicks'),
     Input('download-transcription-button', 'n_clicks')]
)
def dl_files(translation_clicks, transcription_clicks):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'download-translation-button':
        if os.path.exists(OUTPUT_TRANSLATION_OBJECT):
            return dcc.send_file(OUTPUT_TRANSLATION_OBJECT), ""
        else:
            return None, dbc.Alert("Translation file not found!", color="danger")

    elif triggered_id == 'download-transcription-button':
        if os.path.exists(OUTPUT_TRANSCRIPTION_OBJECT):
            return dcc.send_file(OUTPUT_TRANSCRIPTION_OBJECT), ""
        else:
            return None, dbc.Alert("Transcription file not found!", color="danger")

    return None, ""
    
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8999, debug=True)
