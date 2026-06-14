from imap_tools import MailBox

from pathlib import Path


def load_att(mailbox, config):
    mailbox.folder.set(config.email_folder)
    for msg in mailbox.fetch():
        if config.email_subject and config.email_subject not in (msg.subject or ""):
            continue

        if config.email_from and config.email_from not in (msg.from_ or ""):
            continue

        if not msg.attachments:
            continue

        for att in msg.attachments:
            if att.filename.endswith(config.file_type):
                if config.file_path:
                    path = Path(config.file_path)/att.filename
                else:
                    config.file_path.mkdir(exist_ok=True)
                    path = config.file_path/att.filename

                with open(path, 'wb') as f:
                    f.write(att.payload)
        
def download_bills(config, host, user, pwd):
    with MailBox(host).login(user, pwd) as mailbox:
        load_att(
            mailbox,
            config.file_path,
            config.file_type,
            config.email_folder,
            config.email_subject,
            config.email_from
        )
 
                
if __name__ == '__main__':
    download_bills('C:/Users/Marcelo Cardoso/OneDrive/programming/portfolio/FinancialControl 0.1v/data/raw','.ofx', "FinancialControl", "Extrato da fatura do Cartão Nubank", "todomundo@nubank.com.br")

