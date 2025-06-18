import requests
import logging

url = "https://api.openmhz.com/wakesimul/calls"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://openmhz.com/",
    "Origin": "https://openmhz.com",
    "Connection": "keep-alive",
    "DNT": "1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

try:
    response = requests.get(url, headers=headers)
    logging.info(f"✅ Status code: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    logging.info(f"📥 Retrieved {len(data.get('calls', []))} calls")
except Exception as e:
    logging.error(f"❌ Error fetching calls: {e}")
