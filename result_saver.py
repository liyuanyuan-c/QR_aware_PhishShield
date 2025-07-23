import csv

def save_urls_to_csv(urls, output_file='extracted_urls.csv'):
    try:
        unique_urls = list(set(tuple(row) for row in urls))
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Rating'])  # head
            writer.writerows(urls)
        print(f"[✓] Save {len(urls)} URL to {output_file} successfully")
    except Exception as e:
        print(f"[!] Wrnong: {e}")