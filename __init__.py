#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Prerequisites
#
# Python Modules:
#    cfscrape
#    requests
#    PyExecJS
#    beautifulsoup4
#    google-api-python-client
#    python-bittrex
#
# Ubuntu's 'json package
#
# Author: Luis Ramirez - luis.rmirez@opencloud.es
# Release_ 0.1
#
# Copyright (C) 2017,2018 Luis Ramirez, http://www.opencloud.es
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# Copyright (C) [2016-18] [Luis Ramirez - OpenCloudES]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##

import os
import sys
import time
import logging
import argparse
import json
from coins import *
from bittrex_values import *
import auxiliary_module
from pydaemon import Daemon

def values(service, logger):
    spreadsheetId = '102gZu2gRkReD3f92TZbWsYV6Qe3OCZPG1a__83inYs4'
    rangeName = 'Coins!A1:I5'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    range_ = 'Coins!I2:I10'
    value_input_option = 'RAW'
    insert_data_option = ''

    changes = ['BTC-UBQ','BTC-XMY','BTC-DOGE','BTC-RDD','BTC-ABY','BTC-XRP','BTC-XLM','BTC-ADA','BTC-BTC','BTC-ETH','BTC-LTC']
    x = 1
    for i in range(len(changes)):
        x = x+1
        if changes[i] != 'BTC-BTC':
            btc_change = bittrex_exchange(changes[i])
        else:
            btc_change_json = json.dumps({"Ask": 1,"Bid": 1,"Last": 1})
            btc_change = json.loads(btc_change_json)
        logger.info('Recogido Ticker '+changes[i])
        range_ = 'Coins!K'+str(x)+':K'+str(x)
        ticker_json = json.dumps(btc_change)
        parsed_json = json.loads(ticker_json)
        logger.info('Tratado json para ticker '+changes[i])
        try:
            conv = parsed_json['Last']
            logger.info('Last value for '+changes[i])
        except ValueError:
            conv = 0
            logger.info('ERROR - No hay datos para el ticker '+changes[i])
        value_range_body = {
	"values": [
	   [conv]
	]
        }
        request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=range_, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()

class MyDaemon(Daemon):
    def run(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
        # create logger with 'CPI - Cloud Privado de Indra'
        logger = logging.getLogger('Coins')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('/home/overload/dev/coins/coins/coins.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.info('Demonio arrancado')
        #a = auxiliary_module.Auxiliary()
        #a.do_something()
        #auxiliary_module.some_function()
        while True:
            logger.info('Todo listo para recoger valores')
            values(service, logger)
            logger.info('Valores almacenados correctamente')
            time.sleep(60)


def main():
    """
    The application entry point
    """
    parser = argparse.ArgumentParser(
        #prog='PROG',
        description='Daemon runner',
        epilog="That's all folks"
    )

    parser.add_argument('operation',
                    metavar='OPERATION',
                    type=str,
                    help='Operation accepts any of these values: start, stop, restart, status',
                    choices=['start', 'stop', 'restart', 'status'])

    args = parser.parse_args()
    operation = args.operation

    # Daemon
    daemon = MyDaemon('/home/overload/dev/coins/coins/python.pid',
    )

    if operation == 'start':
        print("Starting daemon")
        daemon.start()
        print(pid)
        pid = daemon.get_pid()
        print(pid)
        if not pid:
            print("Unable run daemon")
        else:
            print("Daemon is running [PID=%d]" % pid)

    elif operation == 'stop':
        print("Stoping daemon")
        daemon.stop()

    elif operation == 'restart':
        print("Restarting daemon")
        daemon.restart()
    elif operation == 'status':
        print("Viewing daemon status")
        pid = daemon.get_pid()

        if not pid:
            print("Daemon isn't running ;)")
        else:
            print("Daemon is running [PID=%d]" % pid)

    sys.exit(0)

if __name__ == '__main__':
    main()