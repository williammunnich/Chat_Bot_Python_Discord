"""Things I still want want to add:

XXXXXXXXXXXTODO spell checkXXXXXXXXX
XXXXXXXXXXXTODO all lower case(for checking user responses)XXXXXXXXXXX
XXXXXXXXXXXXTODO get rid of punctuation when checking responses/adding to databaseXXXXXXXXXXXX
XXXXXXXXXXXtake one response and separate it into sub-responses based on punctuation, respond individuallyXXXXXXXXXXX
TODO have certain responses execute tools
    quit fuction(still has bugs)



"""
'''BUGS
-after running quit funtion and saying no, it doesnt respond the first time, the second time saying no to quit function
lags behind by one response
-

'''


from string_sanitize import string_to_array
from string_sanitize import string_to_string

#import pandas
#for spellcheck
#from textblob import TextBlob
#for interfacing with the csv file
import csv
#for shutting down program
import os
#for getting rid of extra whitespaces
#import re

# headers necessary for saving into csv file, organizing dictionaries
fields = ['saying', 'response']
# name of csv file
filename = "chat_data.csv"

#want to remove all
punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
#seprate context sentancces with these
sentance_divider = '''!;:.?,'''
quit_program = ['exit','quit','leave','abort', 'get out', 'close']
yes = ['yes','y','ye','yee','of course','alright','that is what i want','please', 'yes please', 'yeah', 'yep', 'yeps', 'yip', 'uhuh', 'uhhuh','uh huh', 'u huh', 'thats right', 'thats correct', 'correct','right','positive','true' ]
no = ['no','n','nope', 'na', 'nah','of course not','this is not what i want', 'nay', 'incorrect', 'negative','false']
help = ['help', 'aid', 'support', 'comfort', 'a hand','guidance','service']

def chat(user_input):

    response_is_in_dict = None
    sentance_holder = string_to_array(user_input)
    chat_context_list = create_list_from_csv()
    for sentance in sentance_holder:
        newString = str(sentance)
        is_in_list = check_if_in_csv(sentance)
        quit_words = check_if_quit_statement(sentance)
        if quit_words == True:
            quit_response = input("Bot:You wish to quit the program? ")
            quit_response = string_to_string(quit_response)
            if any(x in quit_response for x in yes):
                os._exit(0)
            print("Bot:Ok, based on your response I will not end this chat program.")
        if is_in_list == False and newString != '' and newString != ' ':
            response_add = input("Bot: I haven't seen '" + newString + "' before, how should I respond? ")
            chat_context_list.append({'saying': newString, 'response': response_add})
            print("Bot: Ok, I will use", "\"" + response_add + "\"", "as a response to", "\"" + newString + "\"","in the future.")
            write_to_csv(chat_context_list)
        elif is_in_list == True:
            for dict in chat_context_list:
                if newString == dict.get("saying"):
                    print("Bot:" + dict.get("response"))


def check_if_in_csv(input):
    chat_context_list = create_list_from_csv()
    sentance_holder = string_to_array(input)
    for sentance in sentance_holder:
        newString = str(sentance)
        # checking if response is in the list and can be handled
        for dict in chat_context_list:
            if newString == dict.get("saying"):
                response_is_in_dict = True
                return response_is_in_dict
            else:
                response_is_in_dict = False
                return response_is_in_dict


def check_if_quit_statement(sentance_holder):
    for sentance in sentance_holder:
        newString = str(sentance)
        # checks if user is using words that would suggest that they want to quit the program
        if any(word in newString for word in quit_program):
            return True
        else:
            return False

def create_list_from_csv():
    chat_context_list = []
    # read csv file and save to a list that can readily be used by python
    with open(filename) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            chat_context_list.append(row)
    return chat_context_list

def write_to_csv(a_list):
    chat_context_list = create_list_from_csv(filename)
    # writing changed list of dictionaries to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        # writing headers (field names)
        writer.writeheader()
        # writing data rows
        writer.writerows(a_list)
    #return true false depending if was able to write to file or not, could also just not return anything if feeling like being lazy
