# index.py
# Main application for python web server 
# Features - showing data collected from arduino
# MIT License

from flask import (
    Flask, make_response, Blueprint, flash, g, redirect, render_template, request, url_for
)
application = Flask(__name__)

#import thread
import traceback
import os
import sys

CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
if CURRENTDIR not in sys.path:
    sys.path.insert(0, CURRENTDIR)

from coreFunctions import DisplayCore

def displayErrorHTML(error):
    # Formats an error in HTML for debugging on web page
    err = "<p>PYTHON ERROR</p>"
    err += "<pre>" + error + "</pre>"
    return err

def backgroundLoop():
    core = DisplayCore()
    while True:
        core.getData()


@application.errorhandler(500)
def internalServerError(error):
    err = "<p>ERROR! 500</p>"
    err += "<pre>"+ str(error) + "</pre>"
    err += "<pre>"+ str(traceback.format_exc()) + "</pre>"
    return err

# Renders a simple html page with the data
@application.route('/', methods=['GET'])
def index():

    readval = 10
    # if we make a post request on the webpage aka press button then do stuff
    if request.method == 'POST':
        # if we press the turn on button
        if request.form['submit'] == 'Turn On':
            print 'TURN ON'

        # if we press the turn off button
        elif request.form['submit'] == 'Turn Off':
            print 'TURN OFF'
        else:
            pass

    return render_template('index.html', temp=100*(readval/1023.))

"""
    try:
	# The simple display core
        core = DisplayCore()
	core.getData()
        # Output the HTML
        response = make_response(core.webUpdate())
        return response
    except:
        # Error
        response = make_response(displayErrorHTML(traceback.format_exc()))
        response.headers['Content-Type'] = 'text/html'
        return response
"""
# Provides the data in JSON format to do some better things with
@application.route('/api/', methods=['GET'])
def json():
    core = DisplayCore()
    core.getData()
    response = make_response(core.retJSON())
    response.headers['Content-Type'] = 'application/json'
    return response

# Run the app
if __name__ == "__main__":
   # thread.start_new_thread(backgroundLoop());
    application.debug = True
    application.run()
