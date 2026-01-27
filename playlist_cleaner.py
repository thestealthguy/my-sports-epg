import urllib.request
import re

# 1. YOUR PROVIDER LINK
m3u_url = "http://stealthpro.xyz/get.php?username=WAYNEGREER&password=87DGL0&type=m3u_plus"

# 2. THE CATEGORY KEYWORDS (Updated to be more specific)
keywords = [
    "CA SPORTS", "US SPORTS", "UK SPORTS", "SKY SPORTS", "CA GENERAL",
    "TENNIS", "F1", "MOTOGP", "PPV", "NCAA", "NFL", "NBA", "NHL",
    "MLB", "MILB", "MLS", "BALLY", "NBC LOCALS", "CBS LOCALS", "ABC LOCALS", 
    "FOX LOCALS", "MY-CW", "ME TV", "HORSE RACING", "MATCHROOM", "EPL", 
    "EFL", "FR SPORTS", "RMC SPORTS", "BEIN", "CANAL+", "LIGUE 1", 
    "FR GENERALE", "VICTORY+", "RDS", "TSN", "SPORTSNET", "TVA SPORTS"
]

def clean_channel_name(line, url_line):
    upper_line = line.upper()
    upper_url = url_line.upper()
    
    # --- GUARD 1: THE VOD KILLER ---
    # If the URL looks like a movie file or a series, REJECT IT
    vod_indicators = ["/MOVIE/", "/SERIES/", ".MP4", ".MKV", ".AVI", ".MOV"]
    if any(x in upper_url for x in vod_indicators):
        return None

    # --- GUARD 2: THE CATEGORY FILTER ---
    # Must match one of our keywords
    if not any(word in upper_line for word in keywords):
        return None

    # --- GUARD 3: THE SPORTS GUIDE CLEANER ---
    suffix = ""
    if "HOME" in upper_line:
        suffix = " [HOME FEED]"
    elif "AWAY" in upper_line:
        suffix = " [AWAY FEED]"

    name_match = re.search(r',([^,]+)$', line)
    if name_match:
        clean_name = name_match.group(1).strip()
        # Strip out the junk symbols for a professional look
        clean_name = clean_name.replace("★", "").replace("❖", "").strip()
        return f"{clean_name}{suffix}"
    
    return None

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
                
                cleaned_name = clean_channel_name(line, url_line)
                
                if cleaned_name:
                    f.write(f'#EXTINF:-1,{cleaned_name}\n')
                    f.write(url_line + "\n")

    print("Success! VOD and Global Sports purged.")

except Exception as e:
    print(f"Error: {e}")
