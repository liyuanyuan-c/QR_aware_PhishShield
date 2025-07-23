import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import policy
from email.generator import BytesGenerator

FROM = "security@apple.com"
TO = "victim@example.com"
SUBJECT = "Security Alert"

# link
malicious_link = "http://malicious-site.com/login"

# PATH
QR_IMAGE_PATH = "malicious_QR_example.png"

#  HTML 
html_content = f'''
<html>
  <body>
    <h2>Suspicious activity detected on your account</h2>
    <p>Please verify your credentials immediately:</p>
    <p><a href="{malicious_link}">Click Here to Secure Account</a></p>
    <p>The QR code for verification is attached in this email.</p>
  </body>
</html>
'''

# body
msg = MIMEMultipart()
msg["From"] = FROM
msg["To"] = TO
msg["Subject"] = SUBJECT

# HTML 
text_content = f"Security alert! Please verify: {malicious_link}"
msg.attach(MIMEText(text_content, "plain"))
msg.attach(MIMEText(html_content, "html"))

# attachment
with open(QR_IMAGE_PATH, "rb") as f:
    img_data = f.read()
    img = MIMEImage(img_data, name="malicious_qr.png")
    img.add_header('Content-Disposition', 'attachment', filename="malicious_qr.png")
    msg.attach(img)

#  .eml 
with open("sample_phishing_with_attachment.eml", "wb") as f:
    gen = BytesGenerator(f, policy=policy.default)
    gen.flatten(msg)

print("✅ phish_email：sample_phishing_with_attachment.eml")