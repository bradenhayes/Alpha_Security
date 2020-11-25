import unittest
import json
import requests

from my_sum import read_trip_thingspeak()

class TripwireTest(unittest.testcase):
    def test_read_status(self):
        URL = 'https://api.thingspeak.com/channels/1150122/fields/1.json?api_keys='
        KEY = 'QEAI32EFVL4ZM7ZR'
        HEADER = '&results=1'
        NEW_URL = URL+KEY+HEADER
        get_data =requests.get(NEW_URL).json()

        data = []
        for x in get_data['feeds']:
            data.append(float(x['field1']))
            expected = 1
            result = read_sound_thingspeak()
            self.assertEqual(data[0], expected)
            
