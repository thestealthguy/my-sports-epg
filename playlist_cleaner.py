import urllib.request

# 1. YOUR PROVIDER LINK (Change this to your actual link)
m3u_url = "http://stealthpro.xyz/get?username=WAYNEGREERE&password=87DGL0&type=m3u_plus"

# 2. THE ELITE SPORTS LIST (Cleans and prioritizes your channels)
replacements = {
    "SPORTSNET ONTARIO": "Sportsnet Ontario", "SPORTSNET EAST": "Sportsnet East",
    "SPORTSNET WEST": "Sportsnet West", "SPORTSNET PACIFIC": "Sportsnet Pacific",
    "SPORTSNET ONE": "Sportsnet ONE", "SPORTSNET 360": "Sportsnet 360",
    "TSN 1": "TSN 1", "TSN 2": "TSN 2", "TSN 3": "TSN 3", "TSN 4": "TSN 4", "TSN 5": "TSN 5",
    "RDS": "RDS", "RDS 2": "RDS 2", "TVA SPORTS": "TVA Sports", "TVA SPORTS 2": "TVA Sports 2",
    "BALLY SPORTS": "Bally Sports", "MSG": "MSG Network", "NESN": "NESN", 
    "YES NETWORK": "YES Network", "SNY": "SNY", "MASN": "MASN", 
    "MARQUEE": "Marquee Sports", "ROOT SPORTS": "Root Sports", 
    "ALTITUDE": "Altitude Sports", "MONUMENTAL": "Monumental Sports",
    "NBC SPORTS": "NBC Sports", "NHL NETWORK": "NHL Network", "MLB NETWORK": "MLB Network"
}

# 3. THE "BRAIN" (Cleans names and identifies Home/Away feeds)
def clean_channel_name(line):
    suffix = ""
    upper_line = line.upper()
    if "HOME" in upper_line:
        suffix = " [HOME FEED]"
    elif "AWAY" in upper_line:
        suffix = " [AWAY FEED]"

    for key, value in replacements.items():
        if key in upper_line:
            # Tag UK/Europe so they drop to the bottom of the list
            if "SKY" in upper_line or "VIAPLAY" in upper_line:
                return f"{value} (UK/Backup)"
            return f"{value}{suffix}"
    return line

# 4. THE "ROBOT" (Downloads, Filters, and Saves)
req = urllib.request.Request(m3u_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        lines = response.read().decode('utf-8').splitlines()

    with open("stealth_playlist.m3u", "w") as f:
        f.write("#EXTM3U\n")
        for i in range(len(lines)):
            line = lines[i]
            # Check if this line is a channel info line
            if line.startswith("#EXTINF") and (i + 1) < len(lines):
                url_line = lines[i+1]
                
                # --- THE VOD FILTER ---
                # This skips any line that is a Movie or TV Series
                if "/movie/" in url_line or "/series/" in url_line:
                    continue 
                
                # If it's not VOD, it's Live TV! Clean it and write it.
                cleaned_info = clean_channel_name(line)
                f.write(cleaned_info + "\n")
                f.write(url_line + "\n")

    print("Success! Created a lean, sports-focused playlist.")

except Exception as e:
    print(f"Error: {e}")
