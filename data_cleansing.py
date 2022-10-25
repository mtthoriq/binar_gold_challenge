from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from unidecode import unidecode
import re
import pandas as pd
import sqlite3

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
info ={
    'title': LazyString(lambda: 'Binar  Gold Challenge'),
    'version': LazyString(lambda: '1'),
    'description': LazyString(lambda: 'Membuat API Cleansing Data'),
    },
    host = LazyString(lambda:request.host)
)
swagger_config = {
    'headers': [],
    'specs': [
        {
        'endpoint': 'docs',
        'route': '/docs.json',
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/docs/',
}
swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)

def get_db_connection():
    conn = sqlite3.connect('Challenge.db')
    conn.row_factory = sqlite3.Row
    return 

def _remove_punct(s):
    return re.sub(r"[^\w\d\s]+", "",s)

def replace_ascii(s):
    return unidecode

def remove_ascii2(s):
    return re.sub(r"\\x[A-Za-z0-9./]+","", unidecode(s))

def remove_byte(s):
    return bytes(s, 'utf-8').decode('utf-8', 'ignore')

def remove_newlines(s):
    return re.sub(r'\n', ' ',s)

def remove_morespace(s):
    return re.sub('  +', '',s)

@swag_from('swagger_config_post.yml', methods=['POST'])
@app.route("/clean_text/v1", methods=['POST'])
def remove_punct_poct():
    s = request.get_json()
        # return jsonify({"CleanText":non_punct})

    print(s['text'])
    result = remove_byte(s['text'])
    result = _remove_punct(result)
    conn = sqlite3.connect("Challenge.db")
    conn.execute("insert into Tweet (Dirt_Text, Clean_Text) values (?,?)", (s['text']), result)
    conn.commit()
    conn.close()
    return jsonify({"Clean_Text":result})

@swag_from('swagger_config_file.yml', methods=['POST'])
@app.route("/get_text/v1", methods=['GET'])
def return_text():
    CleanText_input = request.args.get('CleanText')
    return_text = {
        "text":f"hasil bersih{CleanText_input}"
    }
   
    return jsonify(return_text)

@swag_from('swagger_config_form.yml', methods=['POST'])
@app.route("/upload_csv/v1", methods=['POST'])
def post_file():
    file = request.files["file"]
    df = pd.read_csv(file, encoding='latin')
    df['gold_challenge_df'] = df.Tweet.apply(remove_ascii2)
    conn = sqlite3.connect("Challenge.db")
    gold_challenge_df.to_sql('Challenge_Data', con=conn, index=False, if_exists='append')
    conn.close()
    return jsonify({
        "text":"Successfully upload file"
    })

if __name__ == "__main__":
    app.run(port=1111, debug=True)
