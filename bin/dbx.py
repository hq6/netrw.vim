#!/usr/bin/python

"""Upload or download individual files from your Dropbox.  """

from __future__ import print_function

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata

if sys.version.startswith('2'):
    input = raw_input

import dropbox
from dropbox.files import FileMetadata, FolderMetadata

# OAuth2 access token.  Obtain this from the
# https://www.dropbox.com/developers/apps by creating an App and the clicking on
# Generate Access Token.
TOKEN = 'INSERT_TOKEN_HERE'

def main():
    """Main program.

    Update or download an individual file.
    """
    if len(sys.argv) < 3:
        usage()
    command = sys.argv[1]
    remote_path = sys.argv[2]

    if command == "up" or command == "down":
        if len(sys.argv) < 4:
            usage()
        local_path = sys.argv[3]

    dbx = dropbox.Dropbox(TOKEN)
    try:
        if command == "up":
           upload(dbx, remote_path, local_path)
        elif command == "down":
           download(dbx, remote_path, local_path)
        elif command == "list":
            list_folder(dbx, remote_path)
        else:
           usage() 
    except:
        pass

def list_folder(dbx, remote_path):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    if not remote_path.startswith("/"):
        remote_path = '/' + remote_path
    remote_path = remote_path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(remote_path)
    except dropbox.exceptions.ApiError as err:
#        print('Folder listing failed for', remote_path, '-- assumped empty:', err)
        return
    else:
        for entry in res.entries:
          if isinstance(entry, FolderMetadata):
            print(entry.name + "/")
          else:
            print(entry.name)



def usage():
    print("Usage: python dbx.py <up|down> <remote_path> [local_path]")
    sys.exit(1)


def download(dbx, remote_path, local_path):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    if not remote_path.startswith("/"):
        remote_path = '/' + remote_path
    with stopwatch('download'):
        try:
            dbx.files_download_to_file(local_path, remote_path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None

def upload(dbx, remote_path, local_path, overwrite=True):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    if not remote_path.startswith("/"):
        remote_path = '/' + remote_path
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(local_path)
    with open(local_path, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, remote_path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
#        print('Total elapsed time for %s: %.3f' % (message, t1 - t0), file=sys.stderr)

if __name__ == '__main__':
    main()

