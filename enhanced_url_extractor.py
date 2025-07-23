import re

def extract_urls(text):
    """
    从文本中提取所有可能的钓鱼 URL，包括一些变体写法。
    """
    patterns = [
        r'https?://[^\s\'"<>]+',                   # 标准 URL
        r'hxxps?://[^\s\'"<>]+',                   # 变体写法 hxxp
        r'(?:www\.)?[a-zA-Z0-9\-\.]+\.(?:com|net|org|ru|cn|io|xyz|top)',  # 裸域名
        r'http[s]?://[a-zA-Z0-9\-\.]+@[^\s\'"<>]+', # 含 "@" 的欺骗形式
        r'[a-zA-Z0-9\-\.]+\[\.][a-z]{2,6}'          # 带 [.] 的域名绕过
    ]

    found_urls = set()
    for pattern in patterns:
        matches = re.findall(pattern, text)
        found_urls.update(matches)
    
    return list(found_urls)

def normalize_url(url):
    """
    将变体 URL 转换为标准形式（用于后续分析）
    """
    url = url.replace('hxxp', 'http')
    url = url.replace('[.]', '.')
    return url

def normalize_url_list(urls):
    """
    批量处理多个 URL 的规范化
    """
    return [normalize_url(u) for u in urls]

# 示例调用
if __name__ == '__main__':
    sample_text = '''
    Please verify your account here:
    hxxps://secure-login[.]com
    or http://user@bank.com
    or visit www.malicious-portal.xyz now.
    '''
    
    raw_urls = extract_urls(sample_text)
    cleaned_urls = normalize_url_list(raw_urls)

    print("提取到的原始URL：")
    print(raw_urls)
    print("\n规范化后的URL：")
    print(cleaned_urls)