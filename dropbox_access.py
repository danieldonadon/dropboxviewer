#!/usr/bin/env python3

import dropbox, os.path
from dropbox import DropboxOAuth2FlowNoRedirect

DROPBOX_KEYS_FILENAME = 'dropbox.key'

# ----------------------------------------------------------------------------
def create_file_with_app_key():
    developers_url = 'https://dropbox.com/developers/apps'
    
    print('\nThis application must first be registered at Dropbox.')
    print('1. Goto to: ' + developers_url) 
    print('2. Create an app, requesting full access to files.')
    print('3. Once the app is registered, copy the app key.')
    app_key = input("\nEnter the app key here: ").strip()
    
    with open(DROPBOX_KEYS_FILENAME, 'w') as keyfile:
        print(app_key, file=keyfile)
    return app_key

# ----------------------------------------------------------------------------
def get_token_for_app_key(app_key):
    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, use_pkce=True, 
            token_access_type='offline')
    authorize_url = auth_flow.start()
    
    print('\nThis application must gain access to a Dropbox account.')
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first).')
    print('3. Copy the authorization code.')
    auth_code = input("\nEnter the authorization code here: ").strip()
    
    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print('\nError: %s' % (e,))
        exit(1)
    
    app_token = oauth_result.access_token
    with open(DROPBOX_KEYS_FILENAME, 'a') as keyfile:
        print(app_token, file=keyfile)
    return app_token 

# ----------------------------------------------------------------------------
print("Script for granting and testing access to Dropbox.")

app_key = None
app_token = None

if os.path.exists(DROPBOX_KEYS_FILENAME):
    with open(DROPBOX_KEYS_FILENAME) as keyfile:
        lines = keyfile.readlines()
        if len(lines) >= 1:
            app_key = lines[0].strip()
        if len(lines) >= 2:
            app_token = lines[1].strip()

if not app_key:
    app_key = create_file_with_app_key()
if not app_token:
    app_token = get_token_for_app_key(app_key)

try:
    with dropbox.Dropbox(app_token) as dbx:
        dbx.users_get_current_account()
        print('\nAccess to Dropbox successful!')
except Exception as e:
    print('\nError: %s' % (e,))

