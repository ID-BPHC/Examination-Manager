import base64
import os
import mimetypes
from email.mime.audio import *
from email.mime.base import *
from email.mime.image import *
from email.mime.multipart import *
from email.mime.text import *
from email import encoders

def create_message_with_attachment(to, subject, message_text, file):

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    main_type, sub_type = content_type.split('/', 1)

    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()

    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()

    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    
    elif main_type == "application" and sub_type == "zip":
        fp = open(file, 'rb')
        msg = MIMEBase('application', 'zip')
        msg.set_payload(fp.read())
        encoders.encode_base64(msg)

    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
