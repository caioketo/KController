#!/usr/bin/env python

from lirc.lirc import Lirc
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from canais import Canais
import time

BASE_URL = ''

app = Flask(__name__)

# Initialise the Lirc config parser
lircParse = Lirc('/etc/lirc/lircd.conf')


@app.route("/")
@app.route("/<canal>")
def index(canal=None):
    canais = []
    ccanais = Canais()
    for can in ccanais.getCanais():
        c = {'numero': can.numero, 'canal': can.canal,}
        canais.append(c)
    return render_template('canais.html', canais=canais)


@app.route("/canal/<numero>")
def clicked(numero=None):
    # Send message to Lirc to control the IR
    for c in numero:
        key = "KEY_" + c
        lircParse.send_once("gvt", key)
        time.sleep(1)
   
    lircParse.send_once("gvt", "KEY_OK")
    return ""



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')


