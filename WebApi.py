import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import base64
import datetime
import requests
from colorSq2ToSq2 import highlight_errors

# Đọc nội dung HTML từ tệp với mã hóa UTF-8
with open('recording.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

app = dash.Dash(__name__)

default_text = "Chào mừng bạn đến với Web chuẩn đoán lỗi phát âm trong tiếng Anh!"

app.layout = html.Div([
    html.H1("Chào mừng bạn đến với Web chuẩn đoán lỗi phát âm trong tiếng Anh!", style={'textAlign': 'center'}),

    html.Div([
        html.I(className="fa fa-volume-up", id="play-audio", style={"cursor": "pointer", "fontSize": "24px"}),
        html.Audio(id='audio-player', style={"display": "none"}, autoPlay=True),
    ]),

    html.Div(id='gray-box', style={'backgroundColor': '#f0f0f0', 'border': '2px solid #000', 'borderRadius': '10px',
                                   'padding': '20px', 'margin': '20px', 'height': '200px'},
             children=[
                 html.Div(id='output-container', children=default_text, style={'textAlign': 'center', 'fontSize': 20})
             ]),

    dcc.Input(id='input-box', type='text', placeholder='Enter text...',
              style={'display': 'block', 'width': '50%', 'margin': '10px auto'}),
    html.Div([
        html.Button('Xác nhận chuỗi', id='text-button', style={'display': 'inline-block', 'margin': '10px auto'}),
        html.Button('Kiểm tra phát âm', id='check-button', style={'display': 'inline-block', 'margin': '10px auto'}),
    ], style={'textAlign': 'center'}),

    html.H3("Import or Record Audio File", style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Iframe(
                    id='iframe',
                    srcDoc=html_content,
                    style={
                        'width': '100%',
                        'height': '200px',
                        'border': '1px solid #ccc',
                        'overflow': 'auto',
                        'margin': '10px auto'
                    }
                )
            ], style={'textAlign': 'center'}),
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
                    'display': 'inline-block'
                },
                multiple=False
            ),
            html.Audio(id='recorded-audio', controls=True, style={'display': 'none'}),
        ], style={'width': '60%', 'textAlign': 'center', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'textAlign': 'center', 'display': 'flex', 'justifyContent': 'space-around'}),
    html.Div(id='output-data-upload', style={'textAlign': 'center', 'marginTop': '20px'})
])

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

    if button_id == 'text-button':
        if text_clicks and input_text:
            response = requests.post("http://127.0.0.1:8000/convert-text-to-ipa", json={"text1": input_text,"text2":""})
            ipa_result = response.json().get('ipa', 'Error converting text to IPA')

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
            # Giải mã nội dung âm thanh từ base64
            content_type, content_string = uploaded_file_content.split(',')
            audio_bytes = base64.b64decode(content_string)

            # Lưu file âm thanh vào hệ thống
            with open('uploaded_audio.mp3', 'wb') as f:
                f.write(audio_bytes)

            # Gửi yêu cầu để chuyển đổi văn bản thành IPA
            response_ipa = requests.post("http://127.0.0.1:8000/convert-text-to-ipa",
                                         json={"text1": input_text, "text2":""})
            ipa_result = response_ipa.json().get('ipa', 'Error converting text to IPA')

            # Gửi file âm thanh đến API để chuyển đổi thành văn bản
            files = {'file': open('uploaded_audio.mp3', 'rb')}
            response = requests.post("http://127.0.0.1:8000/upload-audio", files=files)
            if response.status_code == 200:
                text_audio = response.json().get('text', 'Error converting audio to text')
            else:
                text_audio = 'Error converting audio to text'

            # Gửi văn bản và văn bản âm thanh đến API để so sánh
            response = requests.post("http://127.0.0.1:8000/check-button",
                                     json={"text1": input_text, "text2": text_audio})
            if response.status_code == 200:
                result = response.json()
                check_result = result.get('check_button', 'Error comparing words')
                score_result = result.get('score_result', 'Error retrieving score')
            else:
                check_result = 'Error comparing words'
                score_result = 'Error retrieving score'
            # Hiển thị kết quả trong giao diện
            # Chuyển đổi từng phần tử trong score_result thành chuỗi
            score_result_str = [str(score) for score in score_result]

            # Hiển thị kết quả trong giao diện
            highlighted_text = highlight_errors(input_text, text_audio)
            return html.Div([
                html.H3(highlighted_text),
                #html.Div(f"{ipa_result}"),
                html.Div(f"Score: {'/'.join(score_result_str)}"),  # Chuyển đổi score_result thành chuỗi
                html.Div(f"Các từ bị sai: {' '.join(check_result)}")  # Hiển thị danh sách từ khác biệt
            ])
        else:
            # Đường dẫn đến API mà bạn muốn gửi yêu cầu
            url = 'http://127.0.0.1:8000/get-temp-file-content'

            # Gửi yêu cầu GET để lấy nội dung tệp tạm
            response = requests.get(url)

            # Kiểm tra xem yêu cầu có thành công không và in ra kết quả
            if response.status_code == 200:
                result = response.json()
                text_record = result.get('text')
                print('Kết quả từ server:', result.get('text'))
                response = requests.post("http://127.0.0.1:8000/check-button",
                                         json={"text1": input_text, "text2": text_record})
                if response.status_code == 200:
                    result = response.json()
                    check_result = result.get('check_button', 'Error comparing words')
                    score_result = result.get('score_result', 'Error retrieving score')
                else:
                    check_result = 'Error comparing words'
                    score_result = 'Error retrieving score'
                # Hiển thị kết quả trong giao diện
                # Chuyển đổi từng phần tử trong score_result thành chuỗi
                score_result_str = [str(score) for score in score_result]

                # Hiển thị kết quả trong giao diện
                highlighted_text = highlight_errors(input_text, text_record)
                return html.Div([
                    html.H3(highlighted_text),
                    #html.Div(f"{text_record}"),
                    html.Div(f"Score: {'/'.join(score_result_str)}"),  # Chuyển đổi score_result thành chuỗi
                    html.Div(f"Các từ bị sai: {' '.join(check_result)}")  # Hiển thị danh sách từ khác biệt
                ])
            else:
                return html.Div([
                    html.Div('Lỗi khi gửi yêu cầu:', response.status_code, response.text)
                ])

        return default_text
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

if __name__ == '__main__':
    app.run_server(debug=True)
