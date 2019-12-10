import json
import bottle
import appcode


@bottle.route("/")
def handleRequestHTML():
    return bottle.static_file("index.html", root="")


@bottle.route("/index.js")
def handleRequestCode():
    return bottle.static_file("index.js", root="")


# Get the list of categories in the database and their number
@bottle.route('/getListData')
def handleRequestGetListData():
    return json.dumps(appcode.init_server_data())


# Querying Log Data
@bottle.route('/getLogData', method='POST')
def handleRequestGetLogData():
    # The data is the filtering parameters passed from the foreground
    data = json.loads(bottle.request.POST.get('data'))
    return json.dumps(appcode.getLogData(data))


bottle.run(host='0.0.0.0', port='5050', debug=True)
