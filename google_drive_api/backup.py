"""
backup.py

Utility script for backing up files on Google Drive.
Requires Google API Python SDK. See requirements.txt.

USAGE:
0. Install the requirements: $ pip install -r requirements.txt
   Use of virtualenv is highly recommended.
1. Set GOOGLE_API_CLIENT_ID and CLIENT_SECRET environment variables.
2. Set backup folder name. It's assumed to be placed directly under root.
3. Implement create_file method.

Initial auth requires the user to manually type in the URL
into a browser and then copy&paste the verification code back into
the command line.
Once that's done, OAuth credentials are saved as a pickle file.

Note that the code assumes expiration is handled manually i.e. the credentials
file is deleted by hand.

"""
import httplib2
import os
import subprocess
import datetime
import cPickle as pickle

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

# Copy your credentials from the console
CLIENT_ID = os.getenv('GOOGLE_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_API_CLIENT_SECRET')

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

CRED_FILENAME = 'drive.credentials.pickle'
BACKUP_FOLDER = 'enter_your_folder_name_here'


def get_credentials():
    try:
        credentials = pickle.load(open(CRED_FILENAME, 'rb'))
    except Exception:
        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                                   redirect_uri=REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
        pickle.dump(credentials, open(CRED_FILENAME, 'wb'))
    return credentials


def create_file():
    ''' Returns filename to be uploaded
    '''
    # aggregate files into a zip archive here...
    return 'consolidated_filename'


def build_service(credentials):
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('drive', 'v2', http=http)


def get_folder_ids(service):
    files = service.files().list().execute()

    folder_id = None
    root_id = None

    for item in files['items']:
        if item['title'] == BACKUP_FOLDER:
            folder_id = item['id']
            for parent in item['parents']:
                if parent['isRoot']:
                    root_id = parent['id']
                    break
            break
    if not all((folder_id, root_id)):
        raise Exception
    return (folder_id, root_id)


def upload(service, fname, mimetype='application/octet-stream'):
    media_body = MediaFileUpload(fname, mimetype=mimetype, resumable=True)
    body = {
        'title': fname,
        'description': 'Backup file',
        'mimeType': mimetype
    }
    return service.files().insert(body=body, media_body=media_body).execute()


def copy2folder(service, file_id, folder_id):
    mv_body = {  # A reference to a folder's child.
        "kind": "drive#childReference",  # This is always drive#childReference.
        "id": file_id,  # The ID of the child.
    }
    return service.children().insert(folderId=folder_id, body=mv_body).execute()


def delete_from_folder(service, file_id, folder_id):
    return service.children().delete(
        folderId=folder_id, childId=file_id).execute()


def main():
    fname = create_file()
    print('Obtaining credentials...')
    cred = get_credentials()
    service = build_service(cred)
    print('Uploading %s to Drive...' % fname)
    f = upload(service, fname)
    print('Done.')
    print('Moving the file from root to %s.' % BACKUP_FOLDER)
    folder_id, root_id = get_folder_ids(service)
    copy2folder(service, f['id'], folder_id)
    delete_from_folder(service, f['id'], root_id)
    print('All done. (Hoozah!)')


if __name__ == '__main__':
    main()
