# GEMINI API DISCORD BOT - GEORGE CM FOR GDSC ROUND 2
Source code for a Discord bot called GDSC Bot, that has access to the Gemini API which allows user to interact and ask questions with AI. Features also include polling, music playing(and queueing) system, reminder setting system, and a coin flip function(for the gambling men and women)

## Image and video demo
![gdsc gemini bot ss](https://github.com/user-attachments/assets/ed1a08ae-eea1-49f4-b236-0b6e4480ff7f)
**DEMO LINK** : https://youtu.be/EZGV9hobv9I

## How its made
Tech Stack : Python
**Python modules used for dev:**
-> discord.py -> for discord developer tools
-> asyncio -> concurrency and running multiple tasks at onces, used await/async
-> yt_dlp -> for connecting to youtube to play music
-> datetime -> for tracking date and time for reminder command
-> random -> for coinflip command 

Built this with the help of youtube tutorials and existing git repos. Things were going smoothly in the beggining was able to setup the gemini api relatively easily? But then when it came to combining functionalities from different youtube videos it became confusing and i faced a lot of errors. But after spending probably the entirety of today debugging finally made it work.(Thank you for extending deadline)

### Optimizations
Its not a highly optimized code since I did not have enough time. The bot is run locally on my computer, but for better optimization I would simply just run it on a free cloud server and then use a pinging automation to make sure it stays online. I wanted to do this but did not have the time (and patience after a bad differential quiz yesterday).
You can also view the iterations of my version on the commit history, I forked out a new branch to try something new for the music function (which ended up working) and then merged it to the main branch.

## Sources I used to build this thing:
https://discordpy.readthedocs.io/en/stable/index.html
https://github.com/shahidfoy/discord-gemini-bot
https://www.youtube.com/watch?v=5xJgZOiCSM8&list=PLD0qnaHPys3uTeblWgFh0Cpo3V2sHPksq
https://www.youtube.com/watch?v=hHfzHVuRx7k
https://www.youtube.com/watch?v=dRHUW_KnHLs
