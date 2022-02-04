
import discord

import os
import csv
#dotenv is needed to pull information from an env file
from dotenv import load_dotenv
from textblob import TextBlob
import re
#chat it from chat.py and it is the chatbot
from chat import chat
from string_sanitize import string_to_array
from string_sanitize import string_to_string

# headers necessary for saving into csv file, organizing dictionaries
fields = ['saying', 'response']
# name of csv file
filename = "chat_data.csv"
previous_message = None
chat_only_used_once = 0

#next 2 lines are for getting bot authentication token from env file then turning into a python discord recognizable format
load_dotenv()
TOKEN_FILLED = int(os.getenv('TOKEN_FILLED'))
CHANNEL_FILLED = int(os.getenv('DISCORD_CHANNEL'))
if TOKEN_FILLED == 0 or CHANNEL_FILLED == 0:
    print("There is no Discord token or Discord channel specified.")
    print("Please go to your .env file and specify a Discord token and Discord channel.")
    print("After doing so change 'TOKEN_FILLED' and 'CHANNEL_FILLED' to a value of 1")
    os._exit(0)
TOKEN = os.getenv('DISCORD_TOKEN')
server_channel_id = int(os.getenv('DISCORD_CHANNEL'))

#client has something to do with an instance of viewpoint? IDK lol
client = discord.Client()

@client.event
#on ready means when server starts back uo
async def on_ready():
    #channel is something like general in a server, needs to be specified with an id because by itself it does not have refferential data for what server you want
    channel = client.get_channel(server_channel_id)
    #tells terminal successful login
    print('We have logged in as {0.user}'.format(client))
    #asserts dominace in general channel of murrayherbig's server
    await channel.send("Hi!! Type '$chat' to activate the chatbot. \nAfter activating the chatbot use any of the following words to end the program: \n'exit', 'quit', 'leave', 'abort', 'get out', 'close', 'end'")

#variable used so that if you type $chat more than once it doesnt respond several times to the same message (dont want several instances of chat program running)
chat_only_used_once = 0

@client.event
#event is when a message is sent and bot can see it
async def on_message(message):
    global chat_only_used_once
    def check(m):
        #check if boolean of whether message in front of bot is of same as the one the one previously sent (and not the bot itself which is client.user)
        return m.channel == message.channel and m.author != client.user and message.content

    
    
    #wake symbol for bot is $
    if message.content.startswith("$chat") and chat_only_used_once == 0:
        await message.channel.send("Hello, my name Is Wpaai. Let's chat!")
        chat_only_used_once = 1
        while True:
            #print("chat program activated")
            #await message.channel.send("chat functionality activated, lets chat")

            # want to remove all
            punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            # seprate context sentancces with these
            sentance_divider = '''!;:.?,'''
            #
            sentance_buffer = ""
            sentance_holder = []
            newString = ""
            chat_context_list = []
            response_add = ""
            quit_program = ['exit', 'quit', 'leave', 'abort', 'get out', 'close', 'end']
            yes = ['yes', 'y', 'ye', 'yee', 'of course', 'alright', 'that is what i want', 'please', 'yes please', 'yeah',
                   'yep', 'yeps', 'yip', 'uhuh', 'uhhuh', 'uh huh', 'u huh', 'thats right', 'thats correct', 'correct',
                   'right', 'positive', 'true', 'affirmative', 'indeed']
            no = ['no', 'n', 'nope', 'na', 'nah', 'of course not', 'this is not what i want', 'nay', 'incorrect',
                  'negative', 'false']
            help = ['help', 'aid', 'support', 'comfort', 'a hand', 'guidance', 'service']

            # variable gets changed to 1 if the response by user is already in the dictionary, otherwise will trigger code to get a valid response
            response_is_in_dict = 0

            user_input = await client.wait_for('message', check=check)
            user_input = (user_input.content).lower()
            previous_message = user_input

            sentance_holder = string_to_array(user_input)

            # read csv file and save to a list that can readilly be used by python
            with open(filename) as fh:
                rd = csv.DictReader(fh, delimiter=',')
                for row in rd:
                    chat_context_list.append(row)

            for sentance in sentance_holder:

                newString = str(sentance)

                # checks if user is using words that would suggest that they want to quit the program
                if any(word in newString for word in quit_program):
                    await message.channel.send("You wish to quit the program? ")
                    quit_response = await client.wait_for('message', check=check)
                    quit_response = string_to_string(quit_response.content)
                    if any(x in quit_response for x in yes):
                        await message.channel.send("hasta la vista 😎🤖")
                        os._exit(0)
                    await message.channel.send("Ok, based on your response I will not end this chat program.")


                # checking if response is in the list and can be handled
                for dict in chat_context_list:
                    if newString == dict.get("saying"):
                        await message.channel.send(dict.get("response"))
                        response_is_in_dict = 1


                # handler if response has not been seen before, asks how to handle response and adds it to the chat_context_list
                if (response_is_in_dict == 0 and newString != '' and newString != ' '):
                    await message.channel.send("I haven't seen '" + newString + "' before, how should I respond? ")
                    response_add = await client.wait_for('message', check=check)
                    response_add = response_add.content
                    chat_context_list.append({'saying': newString, 'response': response_add})
                    await message.channel.send("Ok, I will use" + "\"" + response_add + "\"" + "as a response to" + "\"" + newString + "\"" + "in the future.")

            # writing changed list of dictionaries to csv file
            with open(filename, 'w') as csvfile:
                # creating a csv dict writer object
                writer = csv.DictWriter(csvfile, fieldnames=fields)

                # writing headers (field names)
                writer.writeheader()

                # writing data rows
                writer.writerows(chat_context_list)

#login with token, if works the bot is online
client.run(TOKEN)