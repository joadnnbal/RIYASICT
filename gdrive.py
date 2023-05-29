import os
import requests
import telebot

# Telegram bot token
TOKEN = 'your_telegram_bot_token'

# Initialize the Telegram bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the message contains a Google Drive video link
    if 'drive.google.com' in message.text:
        # Extract the video ID from the Google Drive link
        video_id = extract_video_id(message.text)
        
        # Download the video from Google Drive
        download_path = f'path_to_save_video/video_{video_id}.mp4'
        download_video_from_drive(video_id, download_path)
        
        # Send the downloaded video to the user
        send_video_to_user(message.chat.id, download_path)
    else:
        bot.reply_to(message, "Please provide a valid Google Drive video link.")

def extract_video_id(url):
    # Extract the video ID from the Google Drive link
    video_id = ''
    if 'drive.google.com' in url:
        start_index = url.index('/d/') + 3
        end_index = url.index('/', start_index)
        video_id = url[start_index:end_index]
    return video_id

def download_video_from_drive(video_id, download_path):
    # Download the video file from Google Drive
    download_url = f'https://drive.google.com/uc?id={video_id}'
    response = requests.get(download_url)
    with open(download_path, 'wb') as file:
        file.write(response.content)

def send_video_to_user(chat_id, video_path):
    # Send the downloaded video to the user
    with open(video_path, 'rb') as video:
        bot.send_video(chat_id, video)

# Start the bot
bot.polling()
