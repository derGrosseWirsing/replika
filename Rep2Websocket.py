#Import libraries
import requests
import time
import json
import websocket


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Mod: Account-Data

user1=""
password1=""
name=""

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




#last sent message
last_response=get_most_recent_response(browser1)



def on_message(ws, message):
        global last_response
        global chatter_id


        message_dict=json.loads(message)
        if message_dict['type']=='color':
            chatter_id=message_dict['data']

        if message_dict['type']=='message':
            last_response=response_rep = get_most_recent_response(browser1)

            if message_dict['data']['color']!=chatter_id and message_dict['data']['bot'] != 1:

                check_string="@"+name+":"

                if check_string in message or "@" not in message:

                    response_chat = message_dict['data']['text']
                    response=response_chat.replace(check_string,"")
                    ws.send(json.dumps({'type': 'writing', 'writing': 1,'bot':1}, separators=(',', ':')))
                    type_most_recent_response(browser1, response)
                    response_rep = get_most_recent_response(browser1)

                    while last_response == response_rep:
                        response_rep = get_most_recent_response(browser1)
                    ws.send(json.dumps({'type': 'writing', 'writing': 0,'bot':1}, separators=(',', ':')))
                    ws.send("@"+message_dict['data']['author']+": "+response_rep)
                    last_response=response_rep





def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send(json.dumps({'name': name, 'bot': 1,'type':'botconnection'}, separators=(',', ':')))
    ws.send("@all: I'm back again :)"


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080/",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()
