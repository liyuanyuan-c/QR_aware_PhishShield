from PIL import Image
from pyzbar.pyzbar import decode
import os

def decode_qr_from_image(image_path):
    """
    get URL from images
    give back strs
    """
    try:
        img = Image.open(image_path)
        decoded_objs = decode(img)
        urls = []
        for obj in decoded_objs:
            data = obj.data.decode('utf-8')
            if data.startswith('http'):
                urls.append(data)
        return urls
    except Exception as e:
        print(f"[!] QR decode failed on {image_path}: {e}")
        return []

def decode_qr_from_folder(folder_path='images'):
    """
    Urls get to check
    """
    all_urls = []
    for filename in os.listdir(folder_path):
        if filename.startswith("._"):
            continue  #  macOS 
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder_path, filename)
            urls = decode_qr_from_image(path)
            all_urls.extend(urls)
    return all_urls

if __name__ == '__main__':
    qr_urls = decode_qr_from_folder('images')
    print("二维码中发现的 URL：")
    for url in qr_urls:
        print("-", url)