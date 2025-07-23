import csv
import os
BLACKLIST_CSV_PATH = 'blacklist.csv'

def load_blacklist(path=BLACKLIST_CSV_PATH):
    """
    blacklist_set and source_map。
    """
    blacklist = set()
    source_map = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row['URL'].strip().lower()
                source = row.get('Source', 'unknown').strip().lower()
                if url:
                    blacklist.add(url)
                    source_map[url] = source
    except FileNotFoundError:
        print(f"[⛔] Haven't find : {path}")
    return blacklist, source_map


def check_url_blacklist(url, blacklist):
    """
    if
    """
    url = url.lower()
    return any(keyword in url for keyword in blacklist)


def tag_urls(url_list, blacklist):
    """
    back
    """
    return [(url, check_url_blacklist(url, blacklist)) for url in url_list]


def append_to_blacklist(urls, source='manual', path='blacklist.csv'):
    existing_urls = set()

    # blackist
    if os.path.exists(path):
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    existing_urls.add(row[0].strip())

    new_entries = []
    for url in urls:
        if url not in existing_urls:
            new_entries.append([url, source])
            existing_urls.add(url)  

    if new_entries:
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(new_entries)
        print(f"[✔] Added {len(new_entries)} url to blacklist {path}")
    else:
        print("[ℹ] All malicious URLs are in blacklist")

if __name__ == "__main__":
    test_urls = ['http://example.com/phishing', 'https://google.com']
    bl, src_map = load_blacklist()
    results = tag_urls(test_urls, bl)
    for url, is_blacklisted in results:
        print(f"{url} -> {'⚠️ hitted by blacklist' if is_blacklisted else ' safe'}")