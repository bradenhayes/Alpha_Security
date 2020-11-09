import dropbox

dbx = dropbox.Dropbox('8WNB4VteJFUAAAAAAAAAAQkkCfn_aeDYNxNuE2p8sIRNh5fWyWuZhLSqwXT5UZ2p')
dbx.users_get_current_account()

f = open('lol.mp3','rb')
dbx.files_upload(bytes(f.read()), '/Audio')
