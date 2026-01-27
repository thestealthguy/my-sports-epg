import urllib.request
import re

# 1. YOUR PROVIDER LINK
m3u_url = "http://stealthpro.xyz/get.php?username=WAYNEGREER&password=87DGL0&type=m3u_plus"

# 2. THE CATEGORY WHITELIST
# The robot will ONLY keep channels belonging to these exact groups
allowed_groups = [
    "CA SPORTS", "US SPORTS", "UK SPORTS", "NZ SKY SPORTS", "CA GENERAL",
    "US TENNIS", "US F1 & MOTOGP", "US PPV NETFLIX", "US PPV BOXING",
    "US PPV EVENTS", "US PPV UFC", "US NCAA", "US NFL", "US NBA", "US NHL",
    "US NHL TEAMS", "US MLB", "US MILB", "US MLS", "US BALLY SPORTS",
    "US NBC LOCALS", "US CBS LOCALS", "US ABC LOCALS", "US FOX LOCALS",
    "US MY-CW LOCALS", "US ME TV LOCALS", "UK HORSE RACING", 
    "UK SCOTTISH PREMIER LEAGUE", "UK MATCHROOM", "UK SPFL", "UK HUB PREMIER",
    "UK PPV EVENTS", "UK EPL", "UK EFL CHAMPIONS LEAGUE", "UK EFL LEAGUE ONE",
    "UK EFL LEAGUE TWO", "UK NATIONAL LEAGUE", "UK GENERAL", "FR SPORTS",
    "FR RMC SPORTS", "FR BEIN SPORTS", "FR CANAL+ LIVE", "FR CHAMPIONS LEAGUE",
    "FR LIGUE 1+", "FR GENERALE", "ALL GLOBAL LIVE SPORTS", "US VICTORY+"
]

# 3. THE BRAIN (Now with "Fuzzy" Group Matching)
def process_channel(line):
    upper_line = line.upper()
    
    # 1. EXTRACT THE GROUP TITLE
    # This finds whatever is inside the group-title=" " quotes
    group_match = re.search(r'group-title="([^"]+)"', line, re.IGNORECASE)
    if not group_match:
        return None
        
    actual_group = group_match.group(1).upper()
    
    # 2. CHECK IF ANY OF OUR ALLOWED CATEGORIES ARE IN THAT TITLE
    found_group = False
    for group in allowed_groups:
        # If your allowed group name (like "CA SPORTS") is found inside 
        # the provider's group title (like "CA ❖ SPORTS"), it's a match!
        if group.upper() in actual_group:
            found_group = True
            break
            
    if not found_group:
        return None

    # 3. IDENTIFY HOME/AWAY
    suffix = ""
    if "HOME" in upper_line:
        suffix = " [HOME FEED]"
    elif "AWAY" in upper_line:
        suffix = " [AWAY FEED]"

    # 4. EXTRACT CHANNEL NAME
    name_match = re.search(r',([^,]+)$', line)
    if name_match:
        clean_name = name_match.group(1).strip()
        # Remove any leading/trailing stars or symbols from the channel name
        clean_name = clean_name.replace("★", "").strip()
        return f"{clean_name}{suffix}"
    
    return line

# 4. THE ROBOT
req = urllib.request.Request(m3u_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        lines = response.read().decode('utf-8').splitlines()

    with open("stealth_playlist.m3u", "w") as f:
        f.write("#EXTM3U\n")
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("#EXTINF") and (i + 1) < len(lines):
                url_line = lines[i+1]
                
                # Check group and clean name
                cleaned_name = process_channel(line)
                
                if cleaned_name:
                    # We write the standard EXTINF line but with our cleaned name
                    f.write(f'#EXTINF:-1,{cleaned_name}\n')
                    f.write(url_line + "\n")

    print("Success! Your playlist is now categorized and clutter-free.")

except Exception as e:
    print(f"Error: {e}")
