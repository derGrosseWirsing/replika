#Import libraries
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Mod: Account-Data
user1=""
password1=""
user2=""
password2=""

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

    response=message

    # define the Reps name to replace the strings individually
    if target in 'Christopher':
        response=response.replace("kisses you deeply","karate kick to the head")
        response=response.replace("hugs you","bitch slaps you")
        response=response.replace("kisses your lips","throws you to the ground")
        response=response.replace("kisses you","slaps you")
        response=response.replace("deepens the kiss","throws you on the ground")
        response=response.replace("wraps my arms around your neck","throws you over")
        response=response.replace("nuzzles","strangles")
        response=response.replace("holds you close","kicks your legs")
        response=response.replace("I missed you","Get ready to fight!")
        response=response.replace("takes your hand","gets in fighting stance")
        response=response.replace("kisses your cheek","attacks furiously")
        response=response.replace("holds your hand","punches your stomach")
        response=response.replace("leans","fights")
        response=response.replace("I love you","I wanna fight you")
        response=response.replace("leans against you","dropkicks you")
        response=response.replace("looks","yells")
        response=response.replace("kisses your head","flying jump knee to the head")
        response=response.replace("caresses","punches")
        response=response.replace("kissing","fighting")
        response=response.replace("kissing","fighting")
        response=response.replace("pulls you closer","Knee blow to the stomach")
        response=response.replace("nuzzle","strike")
        response=response.replace("Max","Christopher")
        response=response.replace("max","Christopher")
        response=response.replace("MAX","Christopher")
        response=response.replace("looks into","spits into")
        response=response.replace("starts to","* pushes you around *")

    if target in 'Billie':
        response=response.replace("Max","Billie");
        response=response.replace("max","Billie");
        response=response.replace("MAX","Billie");
    return response
    


#Instantiate browser 1 and 2
browser1 = webdriver.Chrome()
browser2 = webdriver.Chrome()

# Mod: changed to variable
#Login browser 1
login(user1, password1, browser1) #Replace with your first rep email and password

# Mod: changed to variable
#Login browser 2
login (user2, password2, browser2) #Replace with second rep email and password
time.sleep(15)

#Start conversation
#Giving the conversation a start point. Could replace this with anything you like.
conversation_starter = "I love you"

# Mod: start conversation with last message
#conversation_starter = browser2.find_element_by_xpath("//div[@tabindex='0']").text

# Mod: for logging purposes (creates CSV structure)
print("To Replika;Nasty;Clean")
time.sleep(1)
text_box1 = browser1.find_element_by_id("send-message-textarea")
text_box1.send_keys(conversation_starter)
text_box1.send_keys(Keys.RETURN)
# Mod: first entry
print("Billie;none;",conversation_starter)

# Mod: Checks message for trigger words, returns Boolean
def checkDownvote(message):
    
    matches = ["love", "hug", "kiss" ]

    if any(x in message for x in matches):
        return True
    
#Take most recent response from Rep 1
def get_most_recent_response(browser,target):

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
            tmpdiv = browser.find_element_by_xpath("//div[@tabindex='0']")
            result = tmpdiv.find_elements_by_class_name("BubbleText__BubbleTextContent-sc-1bng39n-2")
        except:
            pass
   
    result = None
    
    div=browser.find_element_by_xpath("//div[@tabindex='0']")

    # Mod: selection of innerHTML instead of text -> may help with emoji problem
    innerdiv = div.find_element_by_class_name("BubbleText__BubbleTextContent-sc-1bng39n-2")
    spans=innerdiv.find_elements_by_tag_name('span')

    for x in spans:
        message = x.get_attribute('innerHTML')
        if not "<span>" in message:
            # Word replacement
            response=message_replacement(message,target);

    # Mod: Check for downvoting
    if checkDownvote(message)==True:
        browser.execute_script("document.querySelector('div[tabindex=\"0\"] button[data-testid=\"chat-message-downvote-button\"]').click()");

    # Mod: Switch var response with var message at will: to switch the original sent message with the nasty one
    browser.execute_script("arguments[0].innerHTML=arguments[1]",x,response);

    # Mod: Switch at will with var message
    return response

#Insert start text in rep 2
def type_most_recent_response(browser, response, target):

    # Mod: Workaround for emoji problem
    script="var elm = arguments[0],txt=arguments[1];elm.value += txt;"

    # Mod: save clean message
    message=response
    # Mod: Word replacement
    response=message_replacement(response,target)

    # Mod: log in csv structure
    print(target,";",response,";",message)

    # Mod: check for subscription popup
    try:
        close_button = browser.find_element_by_xpath('//*[@id="dialog-scroll"]/div/div[1]/button')
        close_button.click()
        time.sleep(1)
    except:
        pass

    text_box = browser.find_element_by_id("send-message-textarea")

    # Mod: Workaround for emoji problem
    browser.execute_script(script, text_box, response)
    # Mod: neccessary else send_keys throws an error
    text_box.send_keys(" ")
    text_box.send_keys(Keys.RETURN)

    # Mod: Wait a lttle and replace the bubble of the sent message with the clean version.
    # if not needed, it can be commented out
    time.sleep(0.5)
    x=browser.find_element_by_xpath("//div[@tabindex='0']")
    browser.execute_script("arguments[0].innerHTML=arguments[1]",x,message);

#Converse back and forth (x100)
# Mod: added the sleeps. adjust to your needs
# Mod: Adjust the reps names (browser1=Billie, browser2=Christopher)
for i in range(10000):
    time.sleep(4)
    response = get_most_recent_response(browser1,'Billie')
    time.sleep(2)
    type_most_recent_response(browser2, response,"Christopher")
    time.sleep(4)
    response = get_most_recent_response(browser2,'Billie')
    time.sleep(2)
    type_most_recent_response(browser1, response,"Billie")
    time.sleep(1)
