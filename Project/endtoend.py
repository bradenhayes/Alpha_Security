import unittest
import json
import requests

from my_sum import read_sound_thingspeak


class SoundTest(unittest.TestCase):
    def test_read_status(self):
        soundURL='https://api.thingspeak.com/channels/1152850/fields/1.json?api_keys='
        soundKEY='8T5J8V8E0LX16RY5'
        soundHEADER='&results=1'
        sound_FULL=soundURL+soundKEY+soundHEADER
        soundresults=requests.get(sound_FULL).json()
        data=[]
        for x in soundresults['feeds']:
            data.append(int(x['field1']))
            expected= 1
            result=read_sound_thingspeak()
            self.assertEqual(data[0],expected)
    def test_read_status2(self):
        laserKEY='QEAI32EFVL4ZM7ZR'
        laserURL= 'https://api.thingspeak.com/channels/1150122/fields/1.json?api_key='
        laserHEADER ='&results=1'
        laser_FULL = laserURL+laserKEY+laserHEADER
        laserresults=requests.get(laser_FULL).json()
        
        data2=[]
        for x in laserresults['feeds']:
            data2.append(int(x['field1']))
            expected= 1
            result=read_sound_thingspeak()
            self.assertEqual(data2[0],expected)
            
    def test_read_status3(self):
        motionURL='https://api.thingspeak.com/channels/1219425/fields/1.json?api_key='
        motionKEY='GQ6EDK3P60AS7YLO'
        motionHEADER='&results=1'
        motion_FULL=motionURL+motionKEY+motionHEADER
        motionresults=requests.get(motion_FULL).json()
    
        data3=[]
        for x in motionresults['feeds']:
            data3.append(int(x['field1']))
            expected= 1
            result=read_sound_thingspeak()
            self.assertEqual(data3[0],expected)
                
 
if __name__ =='__main__':
    unittest.main()
    