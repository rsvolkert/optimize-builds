import os
import hashlib
import requests
from datetime import datetime, timezone


class Connection:
    base_url = 'https://api.smitegame.com/smiteapi.svc/'

    def __init__(self):
        self.session_id = None

        self.create_session()

    @staticmethod
    def get_timestamp():
        dt = datetime.now(timezone.utc)

        return dt.strftime('%Y%m%d%H%M%S')

    @staticmethod
    def generate_signature(method, timestamp):
        str2hash = os.getenv('SMITE_DEV_ID') + method + os.getenv('SMITE_AUTH') + timestamp

        result = hashlib.md5(str2hash.encode())

        return result.hexdigest()

    def create_session(self):
        timestamp = self.get_timestamp()
        signature = self.generate_signature('createsession', timestamp)

        r = requests.get(self.base_url + 'createsessionjson/' + os.getenv('SMITE_DEV_ID') + '/' +
                         signature + '/' + timestamp)
        r.raise_for_status()

        self.session_id = r.json()['session_id']

        return self

    def check_session(self):
        timestamp = self.get_timestamp()
        signature = self.generate_signature('testsession', timestamp)

        r = requests.get(self.base_url + 'testsessionjson/' + os.getenv('SMITE_DEV_ID') + '/' +
                         signature + '/' + self.session_id + '/' + timestamp)
        r.raise_for_status()

        if 'Invalid' in r.json():
            self.create_session()

        return self
