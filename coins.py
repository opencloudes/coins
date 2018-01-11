#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from pprint import pprint
from subprocess import call

import cfscrape
from bs4 import BeautifulSoup

"""try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
"""
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'coins'

def getvalue():

    scraper = cfscrape.create_scraper()
    rawval = scraper.get("https://litebit.eu").content
    soup = BeautifulSoup(rawval, 'html.parser')
    coinvalue = [[0] * 4 for i in range(75)]
    for option in soup.find_all('option'):
        sentence = option.text
        coin = " ".join(sentence.split())
        index = int(option['value'])
        coinvalue[index][0] = float(option['data-buy'])
        coinvalue[index][1] = float(option['data-sell'])
        coinvalue[index][2] = coin
        coinvalue[index][3] = option['value']
    return coinvalue


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


    """
---- main()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '102gZu2gRkReD3f92TZbWsYV6Qe3OCZPG1a__83inYs4'
    rangeName = 'Coins!A1:I5'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s, %s, %s' % (row[0], row[2], row[5], row[7]))
    range_ = 'Coins!I2:I9'
    value_input_option = 'RAW'
    insert_data_option = ''
    coins = getvalue()
    value_range_body = {
	"values": [
	   [coins[67][0]],
           [coins[37][0]],
           [coins[6][0]],
           [coins[44][0]],
           [coins[51][0]],
           [coins[1][0]],
           [coins[21][0]],
           [coins[2][0]]
	]
    }
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    range_ = 'Coins!J2:J9'
    value_range_body = {
	"values": [
	   [coins[67][1]],
           [coins[37][1]],
           [coins[6][1]],
           [coins[44][1]],
           [coins[51][1]],
           [coins[1][1]],
           [coins[21][1]],
           [coins[2][1]]
	]
    }
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    """

