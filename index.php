<?php

$botToken = "YOUR_BOT_TOKEN"; // Replace with your bot token
$lastUpdateId = 0; // Store the last update ID to get only new updates

// Function to fetch new updates from Telegram
function getUpdates($botToken, $lastUpdateId) {
    // Telegram API URL to get updates
    $url = "https://api.telegram.org/bot$botToken/getUpdates?offset=$lastUpdateId";

    // Send request to Telegram API
    $response = file_get_contents($url);
    return json_decode($response, true);
}

// Function to send a message to the chat
function sendMessage($chatId, $message, $botToken) {
    $url = "https://api.telegram.org/bot$botToken/sendMessage";
    $postData = [
        'chat_id' => $chatId,
        'text' => $message
    ];
    // Sending the message
    file_get_contents($url . '?' . http_build_query($postData));
}

// Loop to fetch updates and handle new subscribers
while (true) {
    // Get updates
    $updates = getUpdates($botToken, $lastUpdateId);

    if (!empty($updates['result'])) {
        foreach ($updates['result'] as $update) {
            // Get the latest update ID
            $lastUpdateId = $update['update_id'] + 1;

            // Check if a new member joined the group
            if (isset($update['message']['new_chat_members'])) {
                $newMember = $update['message']['new_chat_members'][0];
                $chatId = $update['message']['chat']['id'];
                $userId = $newMember['id'];
                $userFirstName = $newMember['first_name'];

                // Send a message to the new user
                sendMessage($chatId, "Hello $userFirstName! Welcome to the group!", $botToken);
            }

            // Handle messages or other updates (e.g., button clicks, commands)
            if (isset($update['message']['text'])) {
                $chatId = $update['message']['chat']['id'];
                $text = $update['message']['text'];

                // Example: Check if the user sends a specific command or message
                if ($text == '/start') {
                    sendMessage($chatId, "Welcome to the bot! Please subscribe to our channel.", $botToken);
                }
            }
        }
    }

    // Sleep to avoid hitting Telegram API too frequently
    sleep(1); // sleep for 1 second, you can adjust based on the update frequency
}
?>
