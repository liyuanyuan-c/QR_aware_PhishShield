import json
import csv
from email_reader import parse_eml_file
from image_extractor import extract_images_from_eml
from qr_decoder import decode_qr_from_folder
from result_saver import save_urls_to_csv
from blacklist_checker import load_blacklist, tag_urls, append_to_blacklist
from vt_checker import tag_urls_with_virustotal

#  config.json  API Key
def load_config(path="config.json"):
    with open(path, 'r') as f:
        return json.load(f)
    
#  CSV  URL
def load_urls_from_csv(path="extracted_urls.csv"):
    urls = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            urls.extend(row)
    return list(set(urls))  # differ

# set path and file name
eml_path = 'sample_phishing.eml'
output_image_folder = 'images'
output_csv_file = 'extracted_urls.csv'

def main():
    config = load_config()
    api_key = config.get("vt_api_key")

    print(" Step 1: Analyze email...")
    email_result = parse_eml_file(eml_path)
    body_urls = email_result.get('Clean_URLs', [])
    print(f" Get {len(body_urls)} URL from main body")

    print(" Step 2: Get images...")
    num_images = extract_images_from_eml(eml_path, output_image_folder)
    print(f"  Getted {num_images} images")

    print(" Step 3: Translate URL from QR-code ...")
    qr_urls = decode_qr_from_folder(output_image_folder)
    print(f" Getted {len(qr_urls)} URL from images")

    #  Step 4:  URLs together
    all_urls = list(set(body_urls + qr_urls))

    #  Step 5: use VirusTotal to check
    print(" Step 5: Use VirusTotal to check further...")
    tag_urls_with_virustotal(all_urls, api_key=api_key)

    #  Step 6: re blacklist（new balcklist）
    blacklist, source_map = load_blacklist()
    final_tagged = tag_urls(all_urls, blacklist)

    #  Step 7: save
    print(" Step 6: URL Test Results：")
    for idx, (url, is_blacklisted) in enumerate(final_tagged, start=1):
        status = "⚠️ hit by blacklist" if is_blacklisted else "safe"
        print(f"{idx}. {url} - {status}")

    save_urls_to_csv(
        [[url, "dangerous" if is_blacklisted else "safe"] for url, is_blacklisted in final_tagged],
        output_file=output_csv_file
    )
    print(f"[✔] Save the results to {output_csv_file}")

if __name__ == '__main__':
    main()