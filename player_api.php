<?php
// 1. Get the username and password from the TV App
$user = $_GET['username'];
$password = $_GET['password'];
$action = $_GET['action'];

// 2. Your Provider's Base DNS (The main part of their link)
$provider_dns = "http://stealthpro.xyz"; 

// 3. If the app is just logging in
if (!$action) {
    $login_url = "$provider_dns/player_api.php?username=$user&password=$password";
    $response = file_get_contents($login_url);
    echo $response;
} 

// 4. If the app wants the Live Streams, give it YOUR cleaned list
if ($action == "get_live_streams") {
    header("Location: https://thestealthguy.github.io/my-sports-epg/stealth_playlist.m3u");
}
?>
