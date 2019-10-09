import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)

from bottle import route, run, template,hook,post,request,response
import sys 
sys.path.append("./algorithm") 
from algorithm.train import process_news

@hook('before_request')
def validate():
    REQUEST_METHOD = request.environ.get('REQUEST_METHOD')

    HTTP_ACCESS_CONTROL_REQUEST_METHOD = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
    if REQUEST_METHOD == 'OPTIONS' and HTTP_ACCESS_CONTROL_REQUEST_METHOD:
        request.environ['REQUEST_METHOD'] = HTTP_ACCESS_CONTROL_REQUEST_METHOD

def enable_cors(fn):
    def _enable_cors_impl(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            return fn(*args, **kwargs)

    return _enable_cors_impl

@route('/')
def automaton():
    return template("automaton_page.tpl",{'title':'hello world'})

@hook('before_request')
def validate():
    """使用勾子处理页面或接口访问事件"""
    if request.method == 'POST' and request.POST.get('_method'):
        request.environ['REQUEST_METHOD'] = request.POST.get('_method', '').upper()
        if request.POST.get('_form'):
            request.environ['REQUEST_FORM'] = request.POST.get('_form', '')

@post('/automaton/viewpoint')
@enable_cors
def sign():
    lines =request.body.readlines()
    news = ''
    for line in lines:
        doc = str(line, encoding = "utf-8")
        news += doc
        print( doc )
    result = process_news(news)
    return {"viewpoint":[
        {"speaker": item[0],"content":item[1]} for item in result
    ]}

run(host='0.0.0.0', port=config['port'], debug=False)
