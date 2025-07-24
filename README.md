# QR_aware_PhishShield
An email phishing detector with QR code awareness and VirusTotal integration.

1）Phishing Email Analysis: Parse `.eml` files and extract text, links, and attachments.
2）QR Code Awareness: Automatically decode QR codes from email attachments or embedded images.
3）Local Blacklist Checking: Identify and flag known bad domains or URLs using a customizable blacklist.
4）VirusTotal API Integration: Query real-time threat data from VirusTotal to evaluate link safety.
5）Structured Output: Save extracted results and threat decisions to CSV files for traceability.
6）Modular Architecture: Easy to extend, test, and integrate into larger systems.

## Structure
├── email_reader.py # Extracts email content, attachments, and metadata
├── image_extractor.py # Parses image attachments
├── qr_decoder.py # Decodes QR code content from images
├── enhanced_url_extractor.py # Extracts hyperlinks from text and HTML content
├── vt_checker.py # Communicates with VirusTotal API
├── blacklist_checker.py # Local CSV-based blacklist filtering
├── result_saver.py # Consolidates and exports results
├── main_controller.py # Main entry point for scanning workflow
├── config.json # Stores API key and settings
├── blacklist.csv # Local URL/domain blacklist
├── extracted_urls.csv # Output of scanned and decoded URLs
├── malicious_QR_example.png # Sample image containing a QR phishing link
├── README.md # Documentation
└── LICENSE # MIT License

## Environment Setup

This project runs on Python 3.8 or later.

Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate.bat  # On Windows

This project is for educational and research purposes only.
Do not use real phishing content in production environments.
The repository may contain test files with simulated malicious QR codes or URLs — please use with caution and at your own risk.

## VirusTotal API Key Setup
To enable VirusTotal scanning:

Go to https://www.virustotal.com/

Register and navigate to API Key

Copy your key and paste it into config.json:

json
{
  "virustotal_api_key": "YOUR_API_KEY_HERE"
}
Ensure this file is saved in the root project directory.

Developed by liyuanyuan-c, 2025
For academic and demo purposes in cybersecurity learning scenarios.



