# The Offical TelegramBot of 2023 Bar-Ilan CS Class!

## A quick rundown of what it can do

### Pre-Prepared Answers

The bot has multiple pre-prepared answers that it can provide, such as relevant contact information, public transport inside the campus, and more. These answers are set to be sent when the corresponding command is received and the code behind it is simple.

Currently, the bot has one functionality that is worth explaining in more detail: accessing the drive and sending files based on user request. We'll cover that on the next part.

### The drive function

The bot imports functions from handle_drive.py that enables it to access google drive using the google drive API provided by google. The bot is set to access a specifc folder that I host on my personal drive account. This folder is an exact copy of the Bar Ilan offical Computer Science drive. In the future, provided that the student council will allow my drive service account access to the drive folder, the bot would gain access to the files in real time (currently I need to update the changes).

After first accessing the drive folder, the Bot then lists all the sub-folders inside, and creates special keys called 'mark-up' inside the user interface. The keys are automatically named after the subfolders inside the drive folders, and also have a header attached to their name: 'folder' if its a folder, and 'file' if its not a folder.

When the user makes his choice, Telegram automatically sends the content of the key chosen in the chat, the bot then detects the message and passes it to a secondary function.

The second function first checks if the user's choice is a file or a folder. If its the latter, the process begins again, but this time in the new sub-folder (the folder is scanned for its contents, and a markup is created for the user). If its the former, the function initiates a file sending logic to deliver the specified file to the user.

Sending a file to the user marks the end of the drive function.

**In this instance of the bot, the drive function is disabled.** This is beacause in order for the drive function to work, a google service account credentials must exist in the working directory. If you want to test or play around with the drive function, feel free to contact me and I'll give you a credentials file.

## Hosting

Currently, the script is hosted on a free hosting service. This may prove difficult in the future, in case the bot will start receiving heavier traffic or if threading will become necessary.

## Webhook functionality

Webhooks essentially allow the bot to wait for updates from telegram, instead of constantly checking for new messages.
This allows the app to use less resources in the hosting service.

## How can I contribute?

I am always looking to add more usefull functions to the bot. Feel free to clone this repository to your machine and expirement with it. If you managed to create additional functions, contact me and we can work together on implementing them.
**Be aware that in this build, no API keys are present and the required credentials.json file does not exist as well, thus running the main file will result in an error. If you want to test the file for development purposees, I can supply you with a testing bot API key.**

### Which file should I work on?

As you may have noticed, there are to instances of the bot in the repository: **"bot_with_flask"**, and **"bot_with_polling"**.
As far as functionality goes, they are the same. The key difference is that the flask bot as webhook logic implemented, and the polling bot has polling logic implemented.

If you want to test the bot on your local machine, you should work with the **polling bot**, since you can just fire it up with an API key and it will start responding.

If you want to test/develop some kind of web functionality, you should work with the **flask bot**. Be aware that for the flask bot to work, a URL that can receive POST requests must be set up. I recommend using ngrok for that.
