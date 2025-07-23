import requests
import json
import os
import time
import csv
import base64
from blacklist_checker import append_to_blacklist  # ✅ 引入黑名单写入模块

# PATH
CACHE_FILE = 'vt_cache.json'
BLACKLIST_CSV = 'blacklist.csv'

# load local cache
def load_cache(cache_file=CACHE_FILE):
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {}

# save cache
def save_cache(cache, cache_file=CACHE_FILE):
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)

# base64 without =
def url_to_id(url):
    url_bytes = url.encode("utf-8")
    return base64.urlsafe_b64encode(url_bytes).decode("utf-8").strip("=")

# submit URL for analysis ID
def submit_url_to_vt(url, api_key):
    vt_base = "https://www.virustotal.com/api/v3/urls"
    headers = {"x-apikey": api_key}
    data = {"url": url}
    response = requests.post(vt_base, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["data"]["id"]
    else:
        print(f"[!] Wrong: {response.status_code}, content: {response.text}")
        return None

#  encoded URL id
def query_vt_report(encoded_url_id, api_key):
    report_url = f"https://www.virustotal.com/api/v3/urls/{encoded_url_id}"
    headers = {"x-apikey": api_key}
    response = requests.get(report_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[!] Wrong: {response.status_code}")
        return None

# get report
def query_virustotal(url, api_key):
    encoded_url_id = url_to_id(url)
    analysis_id = submit_url_to_vt(url, api_key)
    if not analysis_id:
        return None

    print(f"[ID] submit successfully，analysis ID: {analysis_id}")
    print(f"[⏳] waiting for analyzing...")

    # ten times
    for i in range(10):
        result = query_vt_report(encoded_url_id, api_key)
        try:
            status = result['data']['attributes']['last_analysis_stats']
            if status:
                print(f"[✅] analyze successfully, in the {i+1} time")
                return result
        except:
            pass  # not already

        time.sleep(3)  # retry
    print("[!] Wrong")
    return None

# （malicious/suspicious > 0）
def parse_vt_result(vt_result):
    try:
        stats = vt_result['data']['attributes']['last_analysis_stats']
        if stats['malicious'] > 0 or stats['suspicious'] > 0:
            print(f"[⚠️] Risk ! malicious: {stats['malicious']}, suspicious: {stats['suspicious']}")
            return True
    except Exception as e:
        print(f"[!]Something wrong with VT ：{e}")
    return False

# check + blacklist
def tag_urls_with_virustotal(urls, api_key, cache_file=CACHE_FILE):
    cache = load_cache(cache_file)
    tagged = []
    new_blacklist = []

    for url in urls:
        if url in cache:
            status = cache[url]
            print(f"[💾] hit the cache: {url} → {'dagerous' if status else 'safe'}")
        else:
            print(f"[🔍] Getting information from VirusTotal: {url}")
            vt_result = query_virustotal(url, api_key)
            status = parse_vt_result(vt_result) if vt_result else False
            cache[url] = status
            save_cache(cache, cache_file)

        if status:
            new_blacklist.append(url)
        tagged.append((url, status))

    if new_blacklist:
        append_to_blacklist(new_blacklist, source='virustotal', path=BLACKLIST_CSV)

    return tagged

