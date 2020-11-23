import unittest
from Audio_Files import testusbmic
from Audio_Files import playaudio
from Audio_Files import callback
from Audio_Files import pin
class TestAudio(unittest.TestCase):
    def test_soundsensor(self):
        playaudio()
        self.assertEqual(callback(pin),1)
        
    def test_usbmic(self):
        self.assertEqual(testusbmic(),1)
        
if __name__ == '__main__':
    unittest.main()
