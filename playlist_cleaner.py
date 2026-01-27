import urllib.request

# 1. Your Master List of Elite Channels
replacements = {
    # Canadian National (All 11)
    "SPORTSNET ONTARIO": "Sportsnet Ontario", "SPORTSNET EAST": "Sportsnet East",
    "SPORTSNET WEST": "Sportsnet West", "SPORTSNET PACIFIC": "Sportsnet Pacific",
    "SPORTSNET ONE": "Sportsnet ONE", "SPORTSNET 360": "Sportsnet 360",
    "TSN 1": "TSN 1", "TSN 2": "TSN 2", "TSN 3": "TSN 3", "TSN 4": "TSN 4", "TSN 5": "TSN 5",
    
    # French Canadian
    "RDS": "RDS", "RDS 2": "RDS 2", "TVA SPORTS": "TVA Sports", "TVA SPORTS 2": "TVA Sports 2",
    
    # Major Local Groups (NHL & MLB)
    "BALLY SPORTS": "Bally Sports", "MSG": "MSG Network", "NESN": "NESN", 
    "YES NETWORK": "YES Network", "SNY": "SNY", "MASN": "MASN", 
    "MARQUEE": "Marquee Sports", "ROOT SPORTS": "Root Sports", 
    "ALTITUDE": "Altitude Sports", "MONUMENTAL": "Monumental Sports",
    "NBC SPORTS": "NBC Sports", "SPECTRUM SPORTSNET": "Spectrum SportsNet",
    
    # National Brands (The "Last Resort" search)
    "NHL NETWORK": "NHL Network", "MLB NETWORK": "MLB Network",
    "ESPN": "ESPN", "TNT": "TNT", "TBS": "TBS"
}

def clean_channel_name(line):
    # This part handles the "Home" and "Away" tags
    suffix = ""
    upper_line = line.upper()
    if "HOME" in upper_line:
        suffix = " [HOME FEED]"
    elif "AWAY" in upper_line:
        suffix = " [AWAY FEED]"

    # This part applies your Elite names
    for key, value in replacements.items():
        if key in upper_line:
            # If it's a UK channel, we move it to the bottom later
            if "SKY" in upper_line or "VIAPLAY" in upper_line:
                return f"{value} (UK/Backup)"
            return f"{value}{suffix}"
    
    return line # If no match, keep the original name

# --- The "Disguised Robot" part ---
# Update this URL to your provider's link
m3u_url = "http://stealthpro.xyz/get.php?username=WAYNEGREER&password=87DGL0&type=m3u"

# This "headers" part is the disguise!
req = urllib.request.Request(
    m3u_url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
)

with urllib.request.urlopen(req) as response:
    lines = response.read().decode('utf-8').splitlines()

with open("stealth_playlist.m3u", "w") as f:
    for i, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            cleaned = clean_channel_name(line)
            f.write(cleaned + "\n")
        else:
            f.write(line + "\n")
