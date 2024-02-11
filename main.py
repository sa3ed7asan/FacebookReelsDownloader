import requests
import json
import re
import asyncio
from flask import Flask, request, redirect 

# Function to extract text from JSON string
def clean_str(s):
    return json.loads('{"text": "' + s + '"}')['text']

# Function to extract download link from content based on regex pattern
def get_link(content, pattern):
    match = re.search(pattern, content)
    if match:
        return clean_str(match.group(1))
    return None

# Function to extract video ID from URL
def generate_id(url):
    if url.isdigit(): return url
    match = re.search(r"\/(?:t\.\d+\/)?(\d+)", url)
    if match: return match.group(1)
    return ''

# Function to extract video title from content
def get_title(content):
    match = re.search(r'<title>(.*?)<\/title>|title id="pageTitle">(.+?)<\/title>', content)
    if match:
        return match.group(1) or match.group(2)
    return None

# Function to make a request to Facebook and extract necessary information (main)
async def facebook(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,en-US;q=0.6',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'Authority': 'www.facebook.com',
        'Sec-Ch-Ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0'
    }
    try:
        response = await asyncio.to_thread(requests.get, url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e: return {'ok': False, 'message': str(e)}
    msg = {'ok': True}
    msg['id'] = generate_id(url)
    msg['title'] = clean_str(get_title(response.text))
    sd_link = get_link(response.text, r'browser_native_sd_url":"([^"]+)"')
    if sd_link: msg.setdefault('links', {})['sd_quality'] = sd_link + '&dl=1'
    hd_link = get_link(response.text, r'browser_native_hd_url":"([^"]+)"')
    if hd_link: msg.setdefault('links', {})['hd_quality'] = hd_link + '&dl=1'
    return msg


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index(): return redirect("https://da.gd/d8Gje")

# example.com/api/facebook/reel?url=facebook_reel_url
@app.route('/api/facebook/reel', methods = ["POST", "GET"])
def main():
    url = request.args.get("url")
    return asyncio.run(facebook(url))


if __name__ == "__main__": app.run(port = 8080, host = "0.0.0.0", debug = True)
# 𝗪𝗥𝗜𝗧𝗧𝗘𝗡 𝗕𝗬 : @DEV_BEN
# 𝗦𝗢𝗨𝗥𝗖𝗘 : @BENfiles on Telegram
