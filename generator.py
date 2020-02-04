"""
generates a flask service in server.py based on the serverless.yaml file
"""

import yaml
import json

import_lines = ['from flask import Flask, request\n', 'from flask_cors import CORS\n', 'import logging\n\n']

code_lines = ['\n\n', 'api = Flask(__name__)\n', 'CORS(api)\n\n', '''
def get_auth_header(r):
    try:
        return str(r.headers['Authorization']).replace('"', '')
    except Exception as e:
        logging.debug(e)
        return ''


def build_event_with_path_params(r, param_name, param_value):
    return {
        'body': str(r.json).replace("'", '"').replace('True', 'true').replace('False', 'false'),
        'headers': {
            'Authorization': get_auth_header(r)
        },
        'pathParameters': {
            param_name: param_value
        }
    }


def build_event(r):
    return {
        'body': str(r.json).replace("'", '"').replace('True', 'true').replace('False', 'false'),
        'headers': {
            'Authorization': get_auth_header(r)
        },
    }
''']


def handle_functions(input):
    json_str = str(input).replace("'", '"').lower()
    funcs = json.loads(json_str)
    #logging.debug(str(funcs).replace("'", '"').lower())

    for func in funcs:
        #logging.debug(funcs[func])
        build_function(func, funcs[func])

    code_lines.append('\n\n')
    code_lines.append("if __name__ == '__main__':\n")
    code_lines.append('    api.run(debug=True)\n')
    write_file(import_lines, code_lines)


def sanitize_path(p):
    p = p.replace('{', '<')
    p = p.replace('}', '>')
    return '/{}'.format(p)


def import_handler(data):
    handler, method_to_call = str(data).rsplit('/', maxsplit=1)
    i = 'from {} import {}\n'.format(str(handler).replace('/', '.'), method_to_call.split('.')[0])
    if i not in import_lines:
        import_lines.append(i)
    return method_to_call


def build_function(name, data):
    m = import_handler(data['handler'])
    code_lines.append('\n\n')
    http_event = data['events'][0]['http']
    path = sanitize_path(str(http_event['path']))
    code_lines.append("@api.route('{}', methods=['{}'])\n".format(path, str(http_event['method']).upper()))
    if '<' in path:
        path_param = path.split('>')[0].split('<')[-1]
        code_lines.append('def {}({}):\n'.format(name, path_param))
        code_lines.append("    event = build_event_with_path_params(request, '{}', {})\n".format(path_param, path_param))
        code_lines.append('    logging.debug(event)\n')
        code_lines.append('    res = {}(event, None)\n'.format(m))
        code_lines.append("    return res['body'], res['statusCode']\n")
    else:
        code_lines.append('def {}():\n'.format(name))
        code_lines.append('    event = build_event(request)\n')
        code_lines.append('    logging.debug(event)\n')
        code_lines.append('    res = {}(event, None)\n'.format(m))
        code_lines.append("    return res['body'], res['statusCode']\n")


def write_file(imports, code):
    f = open("server.py", "w")
    for i in imports:
        f.write(i)

    for c in code:
        f.write(c)
    f.close()


with open(r'./serverless.yml') as file:
    documents = yaml.load(file, yaml.FullLoader)
    for item, doc in documents.items():
        if item == 'functions':
            handle_functions(doc)
            break



