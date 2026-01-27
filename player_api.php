<?php
// If the app is just logging in:
if (!isset($_GET['action'])) {
    echo '{"user_info":{"auth":1,"status":"Active","exp_date":"1735689600"},"server_info":{"url":"https://thestealthguy.github.io/my-sports-epg/","port":"443","https_port":"443","server_protocol":"https"}}';
} 
// If the app is asking for the TV channels:
elseif ($_GET['action'] == 'get_live_streams') {
    header('Location: https://thestealthguy.github.io/my-sports-epg/get_live_streams.json');
}
?>
