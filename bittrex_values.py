#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
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
from bittrex.bittrex import *
import json

def bittrex_exchange( tckr ):
    #my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
    my_bittrex = Bittrex(None, None)
    markets=my_bittrex.get_markets()
    eth=my_bittrex.get_currencies()
    ltc=my_bittrex.get_ticker('BTC-LTC')
    if tckr :
        ticker = my_bittrex.get_ticker(tckr)
        ticker_json = json.dumps(ticker)
        parsed_json = json.loads(ticker_json)
        results = parsed_json['result']
        results_json = json.dumps(results)
        result_json = json.loads(results_json)
        return result_json
