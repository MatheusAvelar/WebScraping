from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask
import re
import json
from flask import render_template
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/')
def index():
    return render_template('tutorial.html')


@app.route('/getLinguagens', defaults={'link': ''})
@app.route('/getLinguagens/<link>', methods=['GET'])
def getLinguagens(link):
    if not link:
        return render_template('page_not_found.html'), 404
    try:
        url = urlopen('https://github.com/MatheusAvelar/' + link)
        html = BeautifulSoup(url.read(), "html5lib")
        tag = html.select('li.d-inline > a > span')
        linguagem = []
        porcentagem = []
        i = 0
        v = 0
        value = ' \"valor\":\"'

        for x in tag:
            cabecalho = '\"code' + str(v) + '\": { \"nome\":\"'
            linguagem[len(linguagem):] = [x.text]

            if i % 2 == 0:
                result = cabecalho + linguagem[i] + '\"'
                porcentagem[len(linguagem):] = [result]
                v += 1

            else:
                result = value + linguagem[i] + '\"}'
                porcentagem[len(linguagem):] = [result]
            i += 1

        sub = re.sub('[\']', '', str(porcentagem))
        repl = sub.replace('[', '{').replace(']', '}')
        js = json.loads(repl)
        return json.dumps(js)
    except:
        return render_template('page_not_found.html'), 400


app.run(host='0.0.0.0', debug=True)
