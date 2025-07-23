# email_reader.py
import email
from email import policy
from email.parser import BytesParser
from enhanced_url_extractor import extract_urls, normalize_url_list
import re

#def extract_urls(text):
    #return re.findall(r'https?://[^\s]+', text)

def parse_eml_file(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    sender = msg['From']
    receiver = msg['To']
    subject = msg['Subject']

    if msg.is_multipart():
        parts = [part.get_payload(decode=True).decode(errors='ignore') for part in msg.walk()
                 if part.get_content_type() == 'text/plain']
        body = '\n'.join(parts)
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')

    raw_urls = extract_urls(body)           # different sources
    normalized_urls = normalize_url_list(raw_urls)  # standardize

    return {
        'From': sender,
        'To': receiver,
        'Subject': subject,
        'Body': body,
        'Raw_URLs': raw_urls,
        'Clean_URLs': normalized_urls
    }

# test
if __name__ == '__main__':
    result = parse_eml_file('phish_example.eml')
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:\n" + "\n".join(value) + f"\n{'-'*40}")
        else:
            print(f"{key}:\n{value}\n{'-'*40}")