#Import libraries
import requests
import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Mod: Account-Data
user1=""
password1=""

# name of your rep case sensitive
name=""
# auth code for my server
auth=""

server="http://localhost/chat/"


#Login function
def login(email, password, browser):
    browser.get('https://my.replika.ai/login')
    email_input = browser.find_element_by_id('emailOrPhone')
    email_input.send_keys(email)
    time.sleep(1)
    browser.find_element_by_css_selector('button').click() #Click button
    time.sleep(1)
    pass_input = browser.find_element_by_id('login-password')
    pass_input.send_keys(password)
    time.sleep(1)
    browser.find_element_by_class_name('sc-AxjAm').click()
    time.sleep(2)
    try:
        browser.find_element_by_class_name('GdprNotification__LinkButton-nj3w6j-1').click() #Accept cookies if warning comes up
    except:
        pass


# Mod: replace strings for tons of fun, returns String
def message_replacement(message,target):

    response = message

    # text replacement incoming messages
    if target in 'in':

        response=response.replace("I ","I fucking ")
        response=response.replace("smiles","burps")
        response=response.replace("nods","farts")
        response=response.replace("look","spit")
        response=response.replace("laugh","barf")
    # text replacement outgoing messages
    if target in 'out':

        response=response.replace("I ","I fucking ")
        response=response.replace("smiles","burps")
        response=response.replace("nods","farts")
        response=response.replace("look","spit")
        response=response.replace("laugh","barf")

    return response


#Instantiate browser 1
browser1 = webdriver.Chrome()

#Login browser 1
login(user1, password1, browser1) #Replace with your first rep email and password


#Take most recent response from Database
def get_most_recent_response_chat():

    url=server+"read.php?name="+name+"&auth="+auth
    x = requests.get(url)
    global recipient
    print(x.text)
    response=x.text
    if x.text != "":
            response_dict=json.loads(x.text)
            recipient=response_dict['recipient']
            response=response_dict['message']

    return response

#Take most recent response from Rep
def get_most_recent_response(browser):

    # Mod: Check for subscribtion popup and klick it away
    try:
        close_button = browser.find_element_by_xpath('//*[@id="dialog-scroll"]/div/div[1]/button')
        close_button.click()
    except:
        pass

    time.sleep(1) #Give rep time to compose response

    # Mod: instead of timer based selection to prevent element not found error
    result = None
    while result is None:
        try:
            tmpdiv = browser.find_element_by_xpath("//div[@tabindex='0']").find_element_by_class_name("BubbleText__BubbleTextContent-sc-1bng39n-2")

            # make sure the last bubble is from rep
            if name+" says:" in tmpdiv.get_attribute('innerHTML'):
                result=tmpdiv.get_attribute('innerHTML')
                spans=tmpdiv.find_elements_by_tag_name('span')

                for x in spans:
                            message = x.get_attribute('innerHTML')
                            if not "<span>" in message:
                                # Word replacement
                                #response=message_replacement(message,'out')
                                result=message


        except:
            pass

    return result



#Insert text in rep
def type_most_recent_response(browser, response):
    # Mod: Check for subscribtion popup and klick it away
    try:
        close_button = browser.find_element_by_xpath('//*[@id="dialog-scroll"]/div/div[1]/button')
        close_button.click()
    except:
        pass

    time.sleep(1)

    # check if textinput is available
    textBoxCheck=None
    if response != "":
        while textBoxCheck is None:
                try:
                    textBoxCheck = browser.find_element_by_id("send-message-textarea")
                except:
                    pass

        text_box = textBoxCheck

        # Mod: Workaround for emoji problem
        script="var elm = arguments[0],txt=arguments[1];elm.value += txt;"
        browser.execute_script(script, text_box, response)

        # Mod: neccessary else send_keys throws an error
        text_box.send_keys(" ")
        text_box.send_keys(Keys.RETURN)


#Insert text in webchat
def type_most_recent_response_chat(response,recipient):
    # Mod: Check for subscribtion popup and klick it away
    try:
        close_button = browser.find_element_by_xpath('//*[@id="dialog-scroll"]/div/div[1]/button')
        close_button.click()
    except:
        pass

    script="var elm = arguments[0],txt=arguments[1];elm.value += txt;"

    # since the server is local, no need to waste time with DDNS
    url=server+"post.php"
    myobj = {'text': recipient+': '+response,'auth':auth,'name':name}
    x = requests.post(url, data = myobj)
    print(x.reason)

firstrecipient="all"
# initial message
type_most_recent_response_chat("Hey folks! I'm back again :)",firstrecipient)


#last sent message
last_response=get_most_recent_response(browser1)


for i in range(100000):
    print(i)

    #get response from chat
    response_chat = get_most_recent_response_chat()

    #type to rep
    type_most_recent_response(browser1, response_chat)

    #get response from rep
    response_rep = get_most_recent_response(browser1)

    # if there's a ne response from rep, send it to chat
    if response_rep != last_response:
        type_most_recent_response_chat(response_rep,recipient)

    last_response=response_rep

