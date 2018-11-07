# -*- coding: utf-8 -*-
# Description: Kolide fleet statistics
# Author: srozb
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import json

from bases.FrameworkServices.LogService import LogService

# default module values
# update_every = 4
priority = 90000
retries = 60

ORDER = ['method', 'online']
CHARTS = {
    'method': {
        'options': [None, 'client requests', 'reqs', 'fleet', 'fleet', 'stacked'],
        'lines': [
            ['AuthenticateHost', 'AuthenticateHost', 'incremental', 1, 1], 
            ['GetClientConfig',  'GetClientConfig', 'incremental', 1, 1],
            ['GetDistributedQueries',  'GetDistributedQueries', 'incremental', 1, 1],
            ['IngestFunc',  'IngestFunc', 'incremental', 1, 1],
            ['SubmitDistributedQueryResults',  'SubmitDistributedQueryResults', 'incremental', 1, 1], 
            ['SubmitResultLogs',  'SubmitResultLogs', 'incremental', 1, 1],
            ['SubmitStatusLogs', 'SubmitStatusLogs', 'incremental', 1, 1] 
        ]
    },
    'online': {
        'options': [None, 'clients online', 'online', 'fleet', 'fleet', 'line'],
        'lines': [
            ['GetClientConfig', 'Clients online', 'incremental', 10, 1]
        ]
    }
}

class Service(LogService):
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.log_path = self.configuration.get('log_path', '/var/log/fleet.log')
        self.data = dict()
        self.create_keys()

    def create_keys(self):
        for item in CHARTS['method']['lines']:
            self.data[item[0]] = 0

    def check(self):
        if not os.access(self.log_path, os.R_OK):
            self.error('{0} is not readable'.format(self.log_path))
            return False
        return True

    def get_data(self):
        raw = self._get_raw_data()
        if not raw:
            return None if raw is None else self.data
        for row in raw:
            try:
                match = json.loads('{'+"".join(row.split('{')[1:]))
                self.data[match['method']] += 1
            except:
                pass
        return self.data
