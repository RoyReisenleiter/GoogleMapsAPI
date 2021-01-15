from bottle import route, run, response, static_file, request
from xml.dom import minidom

def enable_cors(func):
    def _enable_cors(*args, **kwargs):
        hds = response.headers
        hds['Access-Control-Allow-Origin'] = '*'
        hds['Access-Control-Allow-Methods'] = ', '.join(['PUT', 'GET', 'POST', 'DELETE', 'OPTIONS'])
        allow = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        hds['Access-Control-Allow-Headers'] = allow
        if request.method != 'OPTIONS':
            return func(*args, **kwargs)
    return _enable_cors

@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./')

@route('/saveRoute', method='POST')
@enable_cors
def saveRoute():
    xml = minidom.parseString(request.body.getvalue().decode('utf-8'))
    routeName = xml.getElementsByTagName("routeName")
    fileName = routeName[0].firstChild.nodeValue

    with open(fileName, 'w') as f:
        f.write(xml.toprettyxml())

    print('Route was saved as: ' + routeName[0].firstChild.nodeValue)

    return fileName.replace(".xml", "")

@route('/openRoute', method='POST')
@enable_cors
def openRoute():
    xml = minidom.parseString(request.body.getvalue().decode('utf-8'))
    routeName = xml.getElementsByTagName("routeName")
    fileName = routeName[0].firstChild.nodeValue

    fileXML = minidom.parse("./" + fileName + ".xml")

    return fileXML.toprettyxml()


run(host='localhost', port=8080, debug=True)