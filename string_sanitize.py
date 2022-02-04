#for spellcheck
from textblob import TextBlob
#for getting rid of extra whitespaces
import re

#want to remove all
punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
#seprate context sentancces with these
sentance_divider = '''!;:.?,'''

def string_to_array(user_input):
    #to be appended to after punctuation edit
    sentance_buffer = ""
    #to be added to between punctuation/sentance/context dividers
    sentance_holder = []

    #makes all char in string lowercase
    user_input = user_input.lower()

    #creates a special type of variable for correcting spelling
    for_spellcheck = TextBlob(user_input)
    #corrects spelling
    for_spellcheck = for_spellcheck.correct()
    #converts back to string so is easier to use
    for_spellcheck = str(for_spellcheck)


    for character in for_spellcheck:
        #sanitize from punctuation
        if character not in punctuation:
                #add to what will be sentance
                sentance_buffer = sentance_buffer + character

        if character in sentance_divider:
            #convert sentance_buffer to a string so you can edit spaces
            sentance_buffer = str(sentance_buffer)
            #replace anything that is a collection of more than one space with a single space
            sentance_buffer = re.sub(' +',' ',sentance_buffer)
            #get rid of spaces at beggining and end of string
            sentance_buffer = sentance_buffer.strip()
            #append sanitized sentance to sentance_holder array
            sentance_holder.append(sentance_buffer)
            sentance_buffer = ""
    if sentance_buffer != "":
        #convert sentance_buffer to a string so you can edit spaces
        sentance_buffer = str(sentance_buffer)
        #replace anything that is a collection of more than one space with a single space
        sentance_buffer = re.sub(' +',' ',sentance_buffer)
        #get rid of spaces at beggining and end of string
        sentance_buffer = sentance_buffer.strip()
        #append sanitized sentance to sentance_holder array
        sentance_holder.append(sentance_buffer)

    #return an array of sanitized sentances, which were seperated by punctuation
    return sentance_holder




def string_to_string(user_input):
    #to be appended to after punctuation edit
    sentance_buffer = ""


    #makes all char in string lowercase
    user_input = user_input.lower()

    #creates a special type of variable for correcting spelling
    for_spellcheck = TextBlob(user_input)
    #corrects spelling
    for_spellcheck = for_spellcheck.correct()
    #converts back to string so is easier to use
    for_spellcheck = str(for_spellcheck)


    for character in for_spellcheck:
        #sanitize from punctuation
        if character not in punctuation:
                #add to what will be sentance
                sentance_buffer = sentance_buffer + character
    if sentance_buffer != "":
        #convert sentance_buffer to a string so you can edit spaces
        sentance_buffer = str(sentance_buffer)
        #replace anything that is a collection of more than one space with a single space
        sentance_buffer = re.sub(' +',' ',sentance_buffer)
        #get rid of spaces at beggining and end of string
        sentance_buffer = sentance_buffer.strip()

    #return sanitized string
    return sentance_buffer
