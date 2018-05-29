#!/usr/bin/python

import json
from os.path import exists

class State(dict):
    """ domain name record """

    FILENAME = '/opt/scripts/domain.json'

    def __init__(self):
        self.state_file = State.FILENAME
        d = {}
        if exists(self.state_file):
            with open(self.state_file) as f:
                d = json.load(f)
        dict.__init__(self, d)

    def save(self):
        with open(self.state_file, 'w') as f:
            json.dump(self, f)

    def __enter__(self):
        return self

    def __exit__(self):
        self.save()


