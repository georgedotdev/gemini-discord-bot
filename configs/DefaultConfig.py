import configparser
#allows you to use the config file
config = configparser.ConfigParser()
config.read('config.ini') #reads the config file using parser

#stores the variables so we can use it throughout the application
DISCORD_OWNER_ID = config['DEFAULT']['discord_owner_id']
DISCORD_SDK = config['DEFAULT']['discord_sdk']
GEMINI_SDK = config['DEFAULT']['gemini_sdk']