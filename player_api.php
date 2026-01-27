<?php
// THIS SCRIPT TRICKS YOUR APP INTO THINKING GITHUB IS AN XTREAM SERVER
header('Content-Type: application/json');

$action = $_GET['action'] ?? '';
$username = $_GET['username'] ?? '';
$password = $_GET['password'] ?? '';

// 1. AUTHENTICATION (The Handshake)
if (!$action) {
    echo json_encode([
        "user_info" => [
            "auth" => 1,
            "status" => "Active",
            "exp_date" => "1735689600", // Dec 2026
            "is_trial" => "0",
            "active_cons" => "0",
            "max_connections" => "5"
        ],
        "server_info" => [
            "url" => "thestealthguy.github.io",
            "port" => "80",
            "https_port" => "443",
            "server_protocol" => "https",
            "timezone" => "America/New_York"
        ]
    ]);
    exit;
}

// 2. LIVE STREAMS (This points the app to your clean M3U)
if ($action == 'get_live_streams') {
    // We redirect the app to your cleaned file
    header("Location: https://thestealthguy.github.io/my-sports-epg/stealth_playlist.m3u");
    exit;
}

// 3. CATEGORIES, VOD, SERIES (We return empty so it doesn't crash)
echo json_encode([]);
?>
