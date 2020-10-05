import http.client
import urllib.parse
key = "54CDA6FJF4RCJ92C"
def writeData():
    email = "Drakemcgillivray@cmail.carleton.ca"
    labSection = "L2-M-12"
    iD = "D"
    params = urllib.parse.urlencode({'field1': email , 'field2':labSection, 'field3': iD, 'key': key})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print (email, labSection, iD)
        print (response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print ("connection failed")
if __name__ == "__main__":
    writeData()
