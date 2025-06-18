import requests
import logging

logging.basicConfig(level=logging.INFO)

FIRE_TGS = {47021, 46940}

def check_fire_calls():
    try:
        logging.info("🔥 Checking fire calls...")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

        response = requests.get("https://api.openmhz.com/wakesimul/calls", headers=headers)
        logging.info(f"✅ Status: {response.status_code}")
        response.raise_for_status()

        calls = response.json().get("calls", [])
        logging.info(f"📥 {len(calls)} calls received")

        for call in calls:
            tg = call.get("talkgroupNum")
            if tg in FIRE_TGS:
                logging.info(f"🚨 TG {tg} @ {call.get('time')}")
                logging.info(f"🔊 {call.get('url')}")
    except Exception as e:
        logging.error(f"❌ Error fetching calls: {e}")

if __name__ == "__main__":
    check_fire_calls()
