import os
import email
from email import policy
from email.parser import BytesParser

def extract_images_from_eml(eml_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    count = 0
    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition", "")).lower()
        content_id = part.get("Content-ID")

        if content_type.startswith("image/"):
            # appended image and image in text
            if "attachment" in content_disposition or "inline" in content_disposition or content_id:
                filename = part.get_filename()
                if not filename:
                    ext = content_type.split("/")[-1]
                    filename = f"image_{count + 1}.{ext}"

                filepath = os.path.join(output_folder, filename)
                with open(filepath, 'wb') as img_file:
                    img_file.write(part.get_payload(decode=True))
                count += 1

    return count