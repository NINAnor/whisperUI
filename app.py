import base64
import os
import tempfile
from typing import Iterator, TextIO

import dash
import dash_bootstrap_components as dbc
import torch
import whisper
from dash import Input, Output, State, dcc, html

UPLOAD_FOLDER = tempfile.mkdtemp(dir=os.getcwd())

# Define instructions and error messages
instr = [
    [html.B("1. UPLOAD .MP3: "), "Click on the Drag and Drop box below"],
    [html.B("2. SELECT LANGUAGE: "), "Choose the source language of your audio file"],
    [
        html.B("3. ANALYZE: "),
        "Click 'Analyze'. You should see a spinner indicating that the file is being translated.",
    ],
    [
        html.B("4. DOWNLOAD: "),
        "Once the analysis is finished, click on the button 'Download transcription' or 'Download translation' to get the results as a .srt file.",
    ],
]

# Common languages supported by Whisper
SUPPORTED_LANGUAGES = [
    {"label": "Auto-detect", "value": None},
    {"label": "Afrikaans", "value": "af"},
    {"label": "Arabic", "value": "ar"},
    {"label": "Armenian", "value": "hy"},
    {"label": "Azerbaijani", "value": "az"},
    {"label": "Belarusian", "value": "be"},
    {"label": "Bosnian", "value": "bs"},
    {"label": "Bulgarian", "value": "bg"},
    {"label": "Catalan", "value": "ca"},
    {"label": "Chinese", "value": "zh"},
    {"label": "Croatian", "value": "hr"},
    {"label": "Czech", "value": "cs"},
    {"label": "Danish", "value": "da"},
    {"label": "Dutch", "value": "nl"},
    {"label": "English", "value": "en"},
    {"label": "Estonian", "value": "et"},
    {"label": "Finnish", "value": "fi"},
    {"label": "French", "value": "fr"},
    {"label": "Galician", "value": "gl"},
    {"label": "German", "value": "de"},
    {"label": "Greek", "value": "el"},
    {"label": "Hebrew", "value": "he"},
    {"label": "Hindi", "value": "hi"},
    {"label": "Hungarian", "value": "hu"},
    {"label": "Icelandic", "value": "is"},
    {"label": "Indonesian", "value": "id"},
    {"label": "Italian", "value": "it"},
    {"label": "Japanese", "value": "ja"},
    {"label": "Kannada", "value": "kn"},
    {"label": "Kazakh", "value": "kk"},
    {"label": "Korean", "value": "ko"},
    {"label": "Latvian", "value": "lv"},
    {"label": "Lithuanian", "value": "lt"},
    {"label": "Macedonian", "value": "mk"},
    {"label": "Malay", "value": "ms"},
    {"label": "Marathi", "value": "mr"},
    {"label": "Maori", "value": "mi"},
    {"label": "Nepali", "value": "ne"},
    {"label": "Norwegian", "value": "no"},
    {"label": "Persian", "value": "fa"},
    {"label": "Polish", "value": "pl"},
    {"label": "Portuguese", "value": "pt"},
    {"label": "Romanian", "value": "ro"},
    {"label": "Russian", "value": "ru"},
    {"label": "Serbian", "value": "sr"},
    {"label": "Slovak", "value": "sk"},
    {"label": "Slovenian", "value": "sl"},
    {"label": "Spanish", "value": "es"},
    {"label": "Swahili", "value": "sw"},
    {"label": "Swedish", "value": "sv"},
    {"label": "Tagalog", "value": "tl"},
    {"label": "Tamil", "value": "ta"},
    {"label": "Thai", "value": "th"},
    {"label": "Turkish", "value": "tr"},
    {"label": "Ukrainian", "value": "uk"},
    {"label": "Urdu", "value": "ur"},
    {"label": "Vietnamese", "value": "vi"},
    {"label": "Welsh", "value": "cy"},
]


# Save the uploaded file
def save_uploaded_file(contents, filename, folder=UPLOAD_FOLDER):
    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as f:
        f.write(decoded)
    return file_path


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
        count += 1
        print(
            f"{count}\n"
            f"{srt_format_timestamp(segment['start'])} --> {srt_format_timestamp(segment['end'])}\n"
            f"{segment['text'].replace('-->', '->').strip()}\n",
            file=file,
            flush=True,
        )


def translate_transcribe_file(file_path, language=None):
    try:
        model = whisper.load_model("medium")
    except torch.OutOfMemoryError:  # fallback
        model = whisper.load_model("tiny", device="cpu")
    
    # Use the selected language or let Whisper auto-detect
    if language:
        translation = model.transcribe(file_path, language=language, task="translate")
        transcription = model.transcribe(file_path, language=language)
    else:
        translation = model.transcribe(file_path, task="translate")
        transcription = model.transcribe(file_path)

    # Create temporary files for translation and transcription
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".srt", delete=False, encoding="utf-8"
    ) as translation_file:
        write_srt(translation["segments"], translation_file)
        translation_path = translation_file.name

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".srt", delete=False, encoding="utf-8"
    ) as transcription_file:
        write_srt(transcription["segments"], transcription_file)
        transcription_path = transcription_file.name

    return translation_path, transcription_path


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Whisper User Interface"

app.layout = html.Div(
    [
        html.H1("Whisper Translation Dashboard"),
        dbc.Alert(
            [
                html.Ul(
                    id="instructions",
                    children=[
                        html.P([html.B(instr[i][0]), instr[i][1]])
                        for i in range(len(instr))
                    ],
                    className="list-unstyled mb-0",
                )
            ],
            color="primary",
            className="mb-4",
        ),
        dcc.Upload(
            id="folder-upload",
            children=html.Div(["Drag and Drop or ", html.A("Select files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,
        ),
        html.Div([
            html.Label("Select Language:", className="form-label"),
            dcc.Dropdown(
                id="language-dropdown",
                options=SUPPORTED_LANGUAGES,
                value="no",  # Default to Norwegian as before
                placeholder="Choose source language",
                className="mb-3",
            ),
        ], className="mb-3"),
        dbc.Button(
            "Analyze",
            id="analyze-button",
            n_clicks=0,
            color="primary",
            className="mr-2",
        ),
        dbc.Button(
            "Download Translation",
            id="download-translation-button",
            n_clicks=0,
            color="success",
        ),
        dbc.Button(
            "Download Transcription",
            id="download-transcription-button",
            n_clicks=0,
            color="success",
            className="ml-2",
        ),
        dcc.Loading(
            id="loading",
            children=[html.Div(id="results-output")],
            type="cube",
            fullscreen=True,
        ),
        dcc.Download(id="download-txt"),
        html.Div(id="info-msg"),
        html.Div(id="alert-message-db"),
    ]
)


@app.callback(Output("folder-upload", "style"), Input("folder-upload", "contents"))
def update_upload_box_style(contents):
    if contents:
        # If a file is uploaded, change box color to green
        return {
            "width": "50%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
            "backgroundColor": "lightgreen",  # Or any color you prefer
        }
    else:
        # Default style without file
        return {
            "width": "50%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        }


# Callback Function Modification for File Handling
@app.callback(
    [
        Output("results-output", "children"),
        Output("info-msg", "children"),
        Output("results-output", "data-translation-path"),
        Output("results-output", "data-transcription-path"),
    ],
    [Input("analyze-button", "n_clicks")],
    [State("folder-upload", "contents"), State("folder-upload", "filename"), State("language-dropdown", "value")],
)
def analyze_file(n_clicks, content, filename, selected_language):
    if n_clicks > 0:
        if not filename or not content:
            return "", dbc.Alert("No file uploaded!", color="danger"), "", ""
        file_path = save_uploaded_file(content, filename)
        if os.path.exists(file_path):
            translation_path, transcription_path = translate_transcribe_file(file_path, selected_language)
            return (
                html.Div("File has been analyzed successfully!"),
                "",
                translation_path,
                transcription_path,
            )
        else:
            return (
                "",
                dbc.Alert(f"File not found at path: {file_path}", color="danger"),
                "",
                "",
            )
    return "", "", "", ""


@app.callback(
    [Output("download-txt", "data"), Output("alert-message-db", "children")],
    [
        Input("download-translation-button", "n_clicks"),
        Input("download-transcription-button", "n_clicks"),
    ],
    [
        State("results-output", "data-translation-path"),
        State("results-output", "data-transcription-path"),
    ],
)
def dl_files(
    translation_clicks, transcription_clicks, translation_path, transcription_path
):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "download-translation-button":
        if translation_path and os.path.exists(translation_path):
            return dcc.send_file(translation_path), ""
        else:
            return None, dbc.Alert("Translation file not found!", color="danger")

    elif triggered_id == "download-transcription-button":
        if transcription_path and os.path.exists(transcription_path):
            return dcc.send_file(transcription_path), ""
        else:
            return None, dbc.Alert("Transcription file not found!", color="danger")

    return None, ""


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8999, debug=True)
