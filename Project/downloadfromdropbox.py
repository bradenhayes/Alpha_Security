import dropbox
dbx = dropbox.Dropbox('dLbnezFTykIAAAAAAAAAAbWNwp4-LRm3T00dhSgCTwjexlC0jIiHwIp6GeBLz7r4')
        # Check that the access token is valid
try:
            dbx.users_get_current_account()
except AuthError as err:
            sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")
with open("/home/pi/Desktop/Sysc3010/Project/Project1/file.mp3", "wb") as f:
            metadata, res = dbx.files_download(path="/Audio/file.mp3")
            f.write(res.content)
