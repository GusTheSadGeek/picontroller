#!/usr/bin/python

# import os
# import tank_temp as temperature

import datetime
from flask import Flask, send_file, Response, request
import traceback

# import relay
import time
import os
import threading

app = Flask(__name__)

prog = None

timers=[]
relays=[]
temps=[]
dists=[]
current_path="/"

def view(ctrl=False):
    line = '<html>\n<head>\n<meta http-equiv="refresh" content="30; url={cp}" />\n'.format(cp=current_path)

    for t in temps:
        current_value = t.current_value
        name = t.name
        line += '<br><br><font size="7">'+name+":"+str(current_value)+' C</font><br><br>'

    for r in relays:
        current_value = r.current_pos()
        name = r.name
        toggle=""
        if ctrl:
            toggle = '<a href="{cp}/TR?r={r}">Toggle {r}</a>'.format(cp='/otocinclus',r=name)
        line += '<br><br><font size="7">'+name+":"+str(current_value)+'</font>{tog}<br><br>'.format(tog=toggle)

    for r in dists:
        current_value = r.current_pos()
        name = r.name
        line += '<br><br><font size="7">'+name+":"+str(current_value)+' cm</font><br><br>'

    for r in timers:
        next_change = r.next_change
        name = r.name
        line += '<br><br><font size="7">'+name+": next change @ "+str(next_change)+'</font><br><br>'

    return line

@app.route("/otocinclus/TR")
def toggle_relay():
    global current_path
    current_path = '/otocinclus'

    relay_name = request.args.get('r')
    for r in relays:
        if r.name == relay_name:
            r.toggle()
    return '<html>\n<head>\n<meta http-equiv="refresh" content="0; url=/otocinclus" />\n</head>\n<body></<body>\n'



@app.route("/")
def rootview():
    global current_path
    current_path = '/'
    return view(False)


@app.route("/otocinclus")
def control():
    global current_path
    current_path = '/otocinclus'
    return view(True)

# def start_server():
#     print "STARTING WEB SERVER"
#     WS().start()
#     print "WEB SERVER STOPPED"
#
# class WS (threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run (self):
#         app.run(host='0.0.0.0', port=5000)
#

if __name__ == "__main__":
    start_server()

from werkzeug.serving import make_server

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('0.0.0.0', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print "STARTING WEB SERVER"
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def start_server():
    global server
#    app = Flask(__name__)
    server = ServerThread(app)
    server.start()
    print "STARTEDD WEB SERVER"

def stop_server():
    global server
    server.shutdown()
    print "WEB SERVER STOPPED"


