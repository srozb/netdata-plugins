# -*- coding: utf-8 -*-
# Description: Filebeat statistics
# Author: srozb
# SPDX-License-Identifier: MIT License

import os
import json

from bases.FrameworkServices.LogService import LogService

# default module values
# update_every = 4
priority = 90000
retries = 60

ORDER = ['bytes', 'events']
CHARTS = {
    'bytes': {
        'options': [None, 'bytes', 'bytes', 'filebeat', 'filebeat', 'line'],
        'lines': [
            ['read', 'Bytes read', 'absolute', 1, 1], 
            ['write',  'Bytes write', 'absolute', 1, 1],
        ]
    },
    'events': {
        'options': [None, 'events', 'events', 'filebeat', 'filebeat', 'line'],
        'lines': [
            ['acked', 'events', 'absolute', 1, 1]
        ]
    }
}

class Service(LogService):
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.log_path = self.configuration.get('log_path', '/var/log/filebeat/filebeat')
        self.data = dict()

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
                match = json.loads('{'+"{".join(row.split('{')[1:]))
                self.data['read'] = match['monitoring']['metrics']['libbeat']['output']['read']['bytes']
                self.data['write'] = match['monitoring']['metrics']['libbeat']['output']['write']['bytes']
                self.data['acked'] = match['monitoring']['metrics']['libbeat']['output']['events']['acked']
            except IndexError:
                pass
        return self.data
