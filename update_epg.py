import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = "385560" # <--- REPLACE WITH YOUR KEY
# Added League IDs for Golf (4442) and F1 (4443)
LEAGUE_IDS = ["4380", "4391", "4424", "4387", "4346", "4442", "4443"]
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# --- THE MASTER MAP ---
# Add your Quebec (RDS/TVA) and France (Canal+/BeIN) channels here
channel_map = {
    # Canada / Quebec
    "TSN 1": "CA ★ TSN 1 HD",
    "RDS": "CA ★ RDS HD",
    "RDS 2": "CA ★ RDS 2 HD",
    "TVA Sports": "CA ★ TVA SPORTS HD",
    "TVA Sports 2": "CA ★ TVA SPORTS 2 HD",
    
    # France
    "Canal+": "FR ★ CANAL+ HD",
    "Canal+ Sport": "FR ★ CANAL+ SPORT HD",
    "beIN Sports 1": "FR ★ BEIN SPORTS 1 HD",
    
    # UK / US
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
                    if not raw_time: continue
                    
                    start_time = raw_time.replace("-", "").replace(":", "").replace(" ", "") + " +0000"
                    api_channel = event.get("strTVStation")
                    
                    # Match the channel name
                    # If it's in our map, use the map name. 
                    # If not, use the API name but clean up the Star for the TV.
                    final_channel = channel_map.get(api_channel, api_channel)

                    prog = ET.SubElement(tv, "programme", {
                        "start": start_time, 
                        "stop": start_time, 
                        "channel": final_channel
                    })
                    ET.SubElement(prog, "title").text = event.get("strEvent")
                    
                    # Adds Sport Type to description (helps with your tabs)
                    sport = event.get("strSport", "Sports")
                    ET.SubElement(prog, "desc").text = f"[{sport}] {event.get('strLeague')} on {final_channel}"
        except: continue
        
    tree = ET.ElementTree(tv)
    # Using 'utf-8' ensures the ★ Star displays correctly in IBO Pro
    tree.write("sports_guide.xml", encoding="UTF-8", xml_declaration=True)

if __name__ == "__main__":
    create_xmltv()
