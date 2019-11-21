from glob import glob
import time
import os
import shutil

from googleapiclient.discovery import build
from algorithms.Mailer.mime_creator import *
from algorithms.Mailer.login import login_mail_account


def get_email_from_path(path):
    return ".".join(path.split(os.sep)[-1].split(".")[0:-1])

def zip_all_dirs(path):
    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            print(f"Zipping {_dir}")
            shutil.make_archive(os.path.join(path, _dir), 'zip', os.path.join(root, _dir))


def send_mails(subject, body, path):


    print("Starting...")

    zip_all_dirs(path)

    creds = login_mail_account()

    service = build('gmail', 'v1', credentials=creds)

    for root, d, files in os.walk(path):

        for _file in files:

            if "@" not in _file:
                continue

            email = get_email_from_path(_file)

            print(f"Sending {_file} to {email}")

            try:

                message = create_message_with_attachment(
                    email, subject, body, os.path.join(root, _file))

                # Call the Gmail API
                (service.users().messages().send(userId="me", body=message)
                 .execute())

            except:
                print(f"ERROR: Failed to send {_file} to {email}")

            time.sleep(2)

    print("**** Done ****")
