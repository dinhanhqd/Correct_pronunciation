import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import base64
import datetime
from flask import Flask, request, jsonify, send_file

import spToText
from engToIpa import convert_text_to_ipa_json
from spToText import sp_to_tx
import os
from colorSq2ToSq2 import compare_words

# Khởi tạo ứng dụng Flask và Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Chuỗi sẵn để hiển thị
default_text = "Chào mừng bạn đến với Web chuẩn đoán lỗi phát âm trong triêng anh!"

# Định nghĩa giao diện
app.layout = html.Div([
    html.H1("Chào mừng bạn đến với Web chuẩn đoán lỗi phát âm trong tiếng Anh!", style={'textAlign': 'center'}),

    # Khung hiển thị chuỗi đã nhập
    html.Div(id='gray-box', style={'background-color': '#f0f0f0', 'border': '2px solid #000', 'border-radius': '10px',
                                   'padding': '20px', 'margin': '20px', 'height': '200px'},
             children=[
                 html.Div(id='output-container', children=default_text, style={'textAlign': 'center', 'fontSize': 20})
             ]),

    # Khung nhập liệu và nút button
    dcc.Input(id='input-box', type='text', placeholder='Enter text...',
              style={'display': 'block', 'width': '50%', 'margin': '10px auto'}),
    html.Div([
        html.Button('Xác nhận chuỗi', id='text-button', style={'display': 'inline-block', 'margin': '10px auto'}),
        html.Button('Kiểm tra phát âm', id='check-button', style={'display': 'inline-block', 'margin': '10px auto'}),
    ], style={'textAlign': 'center'}),

    # Phần tải lên tệp âm thanh và ghi âm
    html.H3("Import or Record Audio File", style={'textAlign': 'center'}),
    html.Div([

        html.Div([
            html.Div([
                html.A(html.Button('Record', id='record-button', n_clicks=0,
                                   style={'fontSize': '20px', 'padding': '20px 90px', 'marginRight': '10px',
                                          'display': 'inline-block'}), href='/record'),
                html.Button('Stop', id='stop-button', n_clicks=0,
                            style={'display': 'none', 'fontSize': '20px', 'padding': '20px 90px',
                                   'display': 'inline-block'}),
            ], style={'display': 'inline-block'}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '85%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'display': 'inline-block'  # Để nút Import File nằm cạnh nút Record
                },
                multiple=False  # Cho phép tải lên một tệp
            ),
            html.Audio(id='recorded-audio', controls=True, style={'display': 'none'}),
        ], style={'width': '60%', 'textAlign': 'center', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'textAlign': 'center', 'display': 'flex', 'justifyContent': 'space-around'}),
    html.Div(id='output-data-upload', style={'textAlign': 'center', 'marginTop': '20px'})
])


# Định nghĩa callback để cập nhật kết quả
@app.callback(
    Output('output-container', 'children'),
    [Input('text-button', 'n_clicks'), Input('check-button', 'n_clicks')],
    [State('input-box', 'value'), State('upload-data', 'contents')]
)
def update_output(text_clicks, check_clicks, input_text, uploaded_file_content):
    ctx = dash.callback_context

    if not ctx.triggered:
        return default_text
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    ipa_result = convert_text_to_ipa_json(input_text)

    if button_id == 'text-button':
        if text_clicks and input_text:

            return html.Div([
                html.H3(input_text),
                html.Div(ipa_result)
            ])
        else:
            return html.Div([
                html.H3('XIN CHÀO'),
                html.Div('Vui lòng nhập văn bản và nhấn "Xác nhận chuỗi" để chuẩn đoán phát âm.'),
            ])

    elif button_id == 'check-button':
        if check_clicks and uploaded_file_content:
            content_type, content_string = uploaded_file_content.split(',')
            audio_bytes = base64.b64decode(content_string)
            with open('uploaded_audio.mp3', 'wb') as f:
                f.write(audio_bytes)
            text_audio = spToText.sp_to_tx('uploaded_audio.mp3')
            text = compare_words(input_text,text_audio)
            return html.Div([
                html.H3(text),
                html.Div(ipa_result),
                html.Div(text_audio)
            ])
        else:
            return html.Div([
                html.H3('XIN CHÀO'),
                html.Div('Vui lòng file âm thanh và nhấn "Kiểm tra phát âm" để chuẩn đoán phát âm.'),
            ])

    return default_text


# Callback để xử lý tệp âm thanh tải lên
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output_upload(uploaded_file_content, uploaded_file_name, uploaded_file_date):
    if uploaded_file_content is not None:
        content_type, content_string = uploaded_file_content.split(',')
        decoded = base64.b64decode(content_string)
        return html.Div([
            html.H5(uploaded_file_name),
            html.H6(datetime.datetime.fromtimestamp(uploaded_file_date)),
            html.Audio(src=uploaded_file_content, controls=True)
        ])


# Endpoint để nhận và lưu dữ liệu âm thanh
@server.route('/upload-audio', methods=['POST'])
def upload_audio():
    data = request.json
    audio_data = data['audio']
    audio_bytes = base64.b64decode(audio_data)
    with open('recorded_audio.wav', 'wb') as f:
        f.write(audio_bytes)
    return jsonify({'message': 'Audio received successfully'}), 200


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
