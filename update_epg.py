import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = "385560" 
LEAGUE_IDS = ["4380", "4391", "4424", "4387", "4346", "4442", "4443"]
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# --- THE MASTER MAP ---
channel_map = {
    "TSN 1": "CA ★ TSN 1 HD",
    "RDS": "CA ★ RDS HD",
    "RDS 2": "CA ★ RDS 2 HD",
    "TVA Sports": "CA ★ TVA SPORTS HD",
    "TVA Sports 2": "CA ★ TVA SPORTS 2 HD",
    "Canal+": "FR ★ CANAL+ HD",
    "Canal+ Sport": "FR ★ CANAL+ SPORT HD",
    "beIN Sports 1": "FR ★ BEIN SPORTS 1 HD",
    "Sky Sports F1": "UK ★ SKY SPORTS F1 RACING HD",
    "Sky Sports Golf": "UK ★ SKY SPORTS GOLF FHD",
    "Golf Channel": "US ★ GOLF CHANNEL HD",
}

def create_xmltv():
    tv = ET.Element("tv")
    for l_id in LEAGUE_IDS:
        try:
            r = requests.get(f"{BASE_URL}/eventsnextleague.php?id={l_id}")
            data = r.json()
            if data and data.get("events"):
                for event in data["events"]:
                    raw_time = event.get("strTimestamp")
                    api_channel = event.get("strTVStation")
                    
                    # FIX: If there is no time or no channel, skip this game
                    if not raw_time or not api_channel:
                        continue
                    
                    start_time = raw_time.replace("-", "").replace(":", "").replace(" ", "") + " +0000"
                    final_channel = channel_map.get(api_channel, api_channel)

                    prog = ET.SubElement(tv, "programme", {
                        "start": start_time, 
                        "stop": start_time, 
                        "channel": str(final_channel) # Added str() to prevent NoneType errors
                    })
                    
                    title_text = event.get("strEvent") or "Sports Event"
                    ET.SubElement(prog, "title").text = title_text
                    
                    sport = event.get("strSport") or "Sports"
                    league = event.get("strLeague") or ""
                    ET.SubElement(prog, "desc").text = f"[{sport}] {league} on {final_channel}"
        except Exception as e:
            print(f"Skipping a league due to error: {e}")
            continue
        
    tree = ET.ElementTree(tv)
    # This part was where the crash happened - fixed!
    with open("sports_guide.xml", "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True)

if __name__ == "__main__":
    create_xmltv()
