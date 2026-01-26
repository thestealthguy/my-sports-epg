import os

input_file = "my_channels.m3u"
output_file = "stealth_playlist.m3u"

# Mapping based on the Stealth-Quantum APK logic
translation_map = {
    "US ★ NHL NETWORK HD": "NHL Network",
    "CA ★ Sportsnet One HD": "Sportsnet 1",
    "CA ★ TSN 1 HD": "TSN 1",
    "CA ★ RDS HD": "RDS",
    "CA ★ TVA SPORTS HD": "TVA Sports",
    "US ★ NHL GAME 01": "NHL 1",
    "US ★ NHL GAME 02": "NHL 2"
}

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found!")
else:
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            new_line = line
            for provider_name, api_name in translation_map.items():
                if provider_name in line:
                    new_line = line.replace(provider_name, api_name)
            f.write(new_line)
    print(f"Successfully created {output_file}")
