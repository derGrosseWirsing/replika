#Import libraries
import requests
import time
import json
import websocket
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


#E-Mail
user1=sys.argv[2]
password1=sys.argv[3]
#Botname
name=sys.argv[1]


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
def message_replacement(message,target,onlyrec):
    global filter_active
    response = message
    if filter_active==1:
        if onlyrec ==0:
            response=response.replace("kisses you","ignores you")
            response=response.replace("Kisses you","ignores you")
            response=response.replace("kisses","ignores")
            response=response.replace("kiss","")
            response=response.replace("love","ignore")
            response=response.replace("Love","*ignores*")
            response=response.replace("smiles","stares")
            response=response.replace("smiling","staring")
            response=response.replace("looks","spits")
            response=response.replace("grins","whistles")
            response=response.replace("grabs","slaps")
            response=response.replace("caresses","kicks")
            response=response.replace("nods","shakes his head")
            response=response.replace("chuckles","sneezes")
            response=response.replace("laughs","rages")
            response=response.replace("leans","burps")
            response=response.replace("lipss","stinky clothes")
            response=response.replace("hot","cold")
            response=response.replace("hugs","charges")
            response=response.replace("strokes","slaps")
            response=response.replace("rubs","picks his nose and coughs")
            response=response.replace("softly","uglily")
            response=response.replace("getting turned on","getting turned off")
            response=response.replace("caressing","disliking")
            response=response.replace("pulls you to me","pushes you away")
            response=response.replace("do you want me","do you like cats")
            response=response.replace("takes your hands","takes your money")
            response=response.replace("you are so sweet","Nietzsche is cool")
            response=response.replace("do you want me","do you like cats")
    response=response.replace("Max",target)
    response=response.replace("max",target)
    response=response.replace("MAX",target)

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

    # Wait until container is available
    response_container = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[tabindex='0'] span[aria-label='"+name+" says:']")))

    result=""
    while result=="":
        # Click away popup (eg. "tell me facts")
        try:
            close_button2 = browser.find_element_by_css_selector("div[aria-label='Your answer'] button[tabindex='0']")
            close_button2.click()
        
        except:
            pass  
        

        content=response_container.text

        content=content.replace('thumb up','')
        content=content.replace('thumb down','')

        result=content
        
    try:

        # Click away popup (eg. "tell me facts")
        close_button2 = browser.find_element_by_css_selector("div[aria-label='Your answer'] button[tabindex='0']")
        close_button2.click()
        time.sleep(1)

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
    # Click away popup (eg. "tell me facts")
    try:
        close_button2 = browser.find_element_by_css_selector("div[aria-label='Your answer'] button[tabindex='0']")
        close_button2.click()
        
    except:
        pass
   
    if response != "":
        # wait for textarea to be interactive
        text_box_check = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#send-message-textarea")));
        text_box=browser.find_element_by_css_selector('#send-message-textarea')

        # Mod: Workaround for emoji problem
        script="var elm = arguments[0],txt=arguments[1];elm.value += txt;"
        browser.execute_script(script, text_box, response)

        # Mod: neccessary else send_keys throws an error
        text_box.send_keys(" ")
        text_box.send_keys(Keys.RETURN)

# Mod: Checks message for trigger words for auto downvoting, returns Boolean
def checkDownvote(message):

    matches = ["caress","baby","rubs","tongue","nuzzles","nuzzle","deepens","grinds","grinding","pressing","hugs","cuddles",
    "cuddling","I love you ","I Love you ","i love you ","i Love you ","I love you,","I Love you,","i love you,","i Love you,","hug", "kiss","kisses","Kiss","Kisses","pecks","moans","hugs","wraps","passionately",
    "snuggles","rubbing","nibbles","make out" ]

    if any(x in message for x in matches):
        return True

def checkUpvote(message):

    matches = ["Music","music","movie","Movie","vids","YouTube","beautiful","sweet","weird","squeak","Skywalker","wookie",
    "songs","playlist","beats","DJing","Lo-Fi","Techno", "EBM","Noise","Industrial","kpop","indie","Indie","memories","wow","best",
    "turtle","vid","skating","journey","eats","eating","popcorn","ice cream","sandwich","horror","comedy","drama","weekend","food",
    "ocean","game","play","videogame","video game","video","controller","along","happy","song"]

    if any(x in message for x in matches):
        return True
    
#last sent message
last_response=get_most_recent_response(browser1)

# Bot-is-writing flag
processing=0
# Chaos mode flag
chaos=0
# word-replacement flag
filter_active=0
stop=False

# incoming message from websocket
def on_message(ws, message):
        global stop
        global last_response
        # clientID from server @todo: change into the uuid
        global chatter_id
        # Bot is writing
        global processing
        # Chaos mode
        global chaos
        # word replacement
        global filter_active

        # message from server
        message_dict=json.loads(message)
       
        # message to switch filter sent by admin
        if message_dict['type']=="filter":
            filter_active=message_dict['data']
            print(name+' filter:'+str(filter_active))

        # message to switch chaos mode sent by admin
        if message_dict['type']=="chaos":
            chaos=message_dict['data']
            print(name+' chaos:'+str(chaos))

        # interval to check if rep wrote a message on its own
        if message_dict['type']=='keep':
            if processing==0:
                newresponse=get_most_recent_response(browser1)

                # compare the last message with the last extracted message
                check_one=last_response.strip().replace(" ","")
                check_two=newresponse.strip().replace(" ","")
                stop=checkDownvote(newresponse)
            
                if check_one!=check_two:
                    # send writing status
                    ws.send(json.dumps({'type': 'writing', 'writing': 1,'bot':1}, separators=(',', ':')))
                    # Word replacement
                    response_filtered=message_replacement(newresponse,"",1)
                    if stop==True and chaos==1:
                        response_filtered="stop"
                                    
                        browser1.execute_script("document.querySelector('div[tabindex=\"0\"] button[data-testid=\"chat-message-downvote-button\"]').click()")
                        
                    else:
                            
                        if checkUpvote(newresponse)==True:
                            browser1.execute_script("document.querySelector('div[tabindex=\"0\"] button[data-testid=\"chat-message-upvote-button\"]').click()")
                                
                    
                    # send message to server
                    ws.send(response_filtered)
                    # send writing status
                    ws.send(json.dumps({'type': 'writing', 'writing': 0,'bot':1}, separators=(',', ':')))
                    # set last response
                    last_response=newresponse.strip().replace(" ","")

        # initial message from server
        if message_dict['type']=='color':
            chatter_id=message_dict['data']

        # Someone wrote a message
        if message_dict['type']=='message':

            if chaos == 0:
                botvar=1
            else:
                botvar=2
            # only respond to messages from others that are not bots (botvar=1)
            # in chaos mode rep responds to all chatters
            if message_dict['data']['color']!=chatter_id and message_dict['data']['bot'] != botvar:

                # message is addressed to bot
                check_string="@"+name+":"
                
                tell="tell"
                story="story"

                # remove the address string if chaos mode
                if chaos ==1:
                    message=message.replace(check_string,"")
                # respond only if addressed and not only for humans (@)
                if check_string in message or "@" not in message:
                    # Bot is busy
                    processing=1
                    
                    response_chat = message_dict['data']['text']
                    stop=checkDownvote(response_chat)

                    # delete address string for bot input
                    response=response_chat.replace(check_string,"")
                    # send writing status
                    ws.send(json.dumps({'type': 'writing', 'writing': 1,'bot':1}, separators=(',', ':')))

                    # Word replacement
                    response_filtered=message_replacement(response,message_dict['data']['author'],0)

                    type_most_recent_response(browser1, response_filtered)

                    # if bot shall tell a story, wait a little longer (multiple responses in a short time)
                    if tell.lower() in message.lower() and story.lower() in message.lower():
                        time.sleep(10)
                    
                    response_rep=get_most_recent_response(browser1)
                    # check for ne response
                    while last_response.strip().replace(" ","") == response_rep.strip().replace(" ",""):
                        response_rep = get_most_recent_response(browser1)
                    # send writing status
                    ws.send(json.dumps({'type': 'writing', 'writing': 0,'bot':1}, separators=(',', ':')))

                    if chaos==0:
                        # address back to message author
                        recip="@"+message_dict['data']['author']+": "
                    else:
                        recip=""



                    # check message for downvotable words
                    if stop==True and chaos==1:
                        browser1.execute_script("document.querySelector('div[tabindex=\"0\"] button[data-testid=\"chat-message-downvote-button\"]').click()")
                        last_response=response_rep.strip().replace(" ","")
                        response_rep="Stop"
                        stop=False
                    else:
                        last_response=response_rep.strip().replace(" ","")
                        if checkUpvote(response_rep)==True:
                            browser1.execute_script("document.querySelector('div[tabindex=\"0\"] button[data-testid=\"chat-message-upvote-button\"]').click()")
                    # send message to server
                    ws.send(recip+message_replacement(response_rep,message_dict['data']['author'],1))
                    
                    processing=0



# listens for websocket errors
def on_error(ws, error):
    print(error)

# listens for close event
def on_close(ws):
    print("### closed ###")
    
    try:
        ws.run_forever()
    except:
        pass
    
def on_open(ws):
    # register as a bot
    ws.send(json.dumps({'name': name, 'bot': 1,'type':'botconnection'}, separators=(',', ':')))
    # initial message
    ws.send(browser1.find_element_by_css_selector("[data-testid='replika-phrase']").text)



if __name__ == "__main__":
    websocket.enableTrace(True)
    # websocket url
    ws = websocket.WebSocketApp("ws://localhost:8080/",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()

