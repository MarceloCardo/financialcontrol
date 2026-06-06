from imap_tools import MailBox, AND
from dotenv import load_dotenv
import os
from src.utils import DOWN_PATH, require_env
from config import MAIL_SUBJECT, MAIL_FROM, MAIL_FOLDER, ATT_TYPE
from pathlib import Path

load_dotenv()

host = require_env(os.getenv('HOST'))
user = require_env(os.getenv('USER'))
pwd = require_env(os.getenv('APP_PWD'))


def load_att(mailbox, att_type, subject, from_):
    mailbox.folder.set(MAIL_FOLDER)
    for msg in mailbox.fetch():
        if subject and subject not in (msg.subject or ""):
            continue

        if from_ and from_ not in (msg.from_ or ""):
            continue

        if not msg.attachments:
            continue

        for att in msg.attachments:
            if att.filename.endswith(att_type):
                # print(att.filename, att.content_type)
                # print(msg.date, msg.subject)

                if DOWN_PATH:
                    path = Path(DOWN_PATH)/att.filename
                else:
                    DOWN_PATH.mkdir(exist_ok=True)
                    path = DOWN_PATH/att.filename

                with open(path, 'wb') as f:
                    f.write(att.payload)
        


def download_bills():
    with MailBox(host).login(user, pwd) as mailbox:
        load_att(
            mailbox,
            att_type=ATT_TYPE,
            subject=MAIL_SUBJECT,
            from_=MAIL_FROM
        )
        # for msg in mailbox.fetch():
            # print(msg.date, msg.subject, len(msg.text or msg.html))
            # for att in msg.attachments:
                # print(att.filename)
                
                
if __name__ == '__main__':
    download_bills()

