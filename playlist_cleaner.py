import urllib.request
import re

# 1. YOUR PROVIDER LINK
m3u_url = "http://stealthpro.xyz/get.php?username=WAYNEGREER&password=87DGL0&type=m3u_plus"

# 2. THE CATEGORY KEYWORDS
# We will keep any line that contains these words
keywords = [
    "CA SPORTS", "US SPORTS", "UK SPORTS", "SKY SPORTS", "CA GENERAL",
    "TENNIS", "F1", "MOTOGP", "PPV", "NCAA", "NFL", "NBA", "NHL",
    "MLB", "MILB", "MLS", "BALLY", "NBC LOCALS", "CBS LOCALS", "ABC LOCALS", 
    "FOX LOCALS", "MY-CW", "ME TV", "HORSE RACING", "MATCHROOM", "EPL", 
    "EFL", "FR SPORTS", "RMC SPORTS", "BEIN", "CANAL+", "LIGUE 1", 
    "FR GENERALE", "GLOBAL LIVE SPORTS", "VICTORY+", "RDS", "TSN", "TVA SPORTS"
]

def clean_channel_name(line):
    upper_line = line.upper()
    
    # 1. THE FILTER: If none of our keywords are in the line, skip it
    if not any(word in upper_line for word in keywords):
        return None

    # 2. IDENTIFY HOME/AWAY
    suffix = ""
    if "HOME" in upper_line:
        suffix = " [HOME FEED]"
    elif "AWAY" in upper_line:
        suffix = " [AWAY FEED]"

    # 3. EXTRACT THE CLEAN NAME
    # This looks for the name after the last comma
    name_match = re.search(r',([^,]+)$', line)
    if name_match:
        clean_name = name_match.group(1).strip()
        # Clean up stars and extra symbols
        clean_name = clean_name.replace("★", "").replace("❖", "").strip()
        return f"{clean_name}{suffix}"
    
    return "Unknown Sports Channel"

# 4. THE ROBOT
req = urllib.request.Request(m3u_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8', errors='ignore')
        lines = content.splitlines()

    with open("stealth_playlist.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("#EXTINF") and (i + 1) < len(lines):
                url_line = lines[i+1]
                
                # Apply our catch-all filter
                cleaned_name = clean_channel_name(line)
                
                if cleaned_name:
                    f.write(f'#EXTINF:-1,{cleaned_name}\n')
                    f.write(url_line + "\n")

    print("Success! Filtered by keywords.")

except Exception as e:
    print(f"Error: {e}")
