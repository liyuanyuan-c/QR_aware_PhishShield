# phishing_generator.py


import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import policy
from email.generator import BytesGenerator

FROM = "security@apple.com"
TO = "victim@example.com"
SUBJECT = "Security Alert"

#  link
malicious_link = "http://malicious-site.com/login"

#   base64
QR_IMAGE_PATH = "malicious_QR_example.png" 
with open(QR_IMAGE_PATH, "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode("utf-8")

#  HTML 
html_content = f'''
<html>
  <body>
    <h2>Suspicious activity detected on your account</h2>
    <p>Please verify your credentials immediately:</p>
    <p><a href="{malicious_link}">Click Here to Secure Account</a></p>
    <p>Or scan the QR code below:</p>
    <img src="data:image/png;base64,{b64_img}" alt="QR Code" />
  </body>
</html>
'''

#  MIME 
msg = MIMEMultipart("alternative")
msg["From"] = FROM
msg["To"] = TO
msg["Subject"] = SUBJECT

# text
text_content = f"Security alert! Please verify: {malicious_link}"
msg.attach(MIMEText(text_content, "plain"))
msg.attach(MIMEText(html_content, "html"))

# EML 
with open("sample_phishing.eml", "wb") as f:
    gen = BytesGenerator(f, policy=policy.default)
    gen.flatten(msg)

print(" phishing ：sample_phishing.eml")
