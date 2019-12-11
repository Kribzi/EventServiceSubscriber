import pygame
import pygame_gui
import math
import sys
import random
from Client import *
from queue import deque
import queue


# Pygame Variables
size = 10
width = 800
height = 600

# CLient
client = None
clientObject = Client()
connectButtonBoolean = False

activeSubscriptions = []


# Initialization
pygame.init()
display = pygame.display.set_mode((width, height))
manager = pygame_gui.UIManager((width, height))
pygame.display.init()
pygame.display.set_caption("Event Service Subscriber")
clock = pygame.time.Clock()

# Fonts
myFont = pygame.font.SysFont("Arial", 20)
bigFont = pygame.font.SysFont("Arial", 32)

# Colors
RGB_RED = (255, 0, 0)
BACKGROUND_COLOR = (55, 55, 55)


subscribe_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((500, 50), (100, 50)), text="Subscribe", manager=manager)


connect_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 50), (100, 30)), text="Connect", manager=manager)

unsubscribe_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((600, 50), (100, 50)), text="Unsubscribe", manager=manager)

eventOptionsList = ["0", "1", "2", "3", "4", "5"]

rolldown_list = pygame_gui.elements.UIDropDownMenu(options_list=eventOptionsList, starting_option=eventOptionsList[0],
                                                   relative_rect=pygame.Rect((420, 50), (80, 50)), manager=manager)


eventInformationText = pygame_gui.elements.UITextBox(
    html_text="", relative_rect=pygame.Rect((5, 150), (400, 300)), manager=manager)

allowedCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

ip_entry = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
    relative_rect=pygame.Rect((5, 50), (150, 50)), manager=manager)
ip_entry.set_allowed_characters(allowedCharacters)

subscriptionText = ""
subscribtionInformation = pygame_gui.elements.UITextBox(
    html_text=subscriptionText, relative_rect=pygame.Rect((420, 150), (350, 300)), manager=manager)


def ReadAndHandleInput(client, connect):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            if clientObject is not None:
                clientObject.Destructor()
            sys.exit()

        if event.type == pygame.USEREVENT:

            if event.user_type == "ui_button_pressed":
                if event.ui_element == subscribe_button:
                    #print("Subscribe button pressed")
                    sendMessage("3")

                elif event.ui_element == unsubscribe_button:
                    #print("Unsubscribe button pressed")
                    sendMessage("4")
                elif event.ui_element == connect_button:
                    ConnectToServer(client)

        manager.process_events(event)
# When the subscribe button has been pressed.


def updateText():
    global activeSubscriptions

    text = bigFont.render("Event Service Client", True, (255, 255, 255))
    display.blit(text, (0, 0))
    text = myFont.render("Incoming Events:", True, (255, 255, 255))
    display.blit(text, (5, 115))
    text = myFont.render("Subscriptions:", True, (255, 255, 255))
    display.blit(text, (420, 115))

    activeSubscriptions.sort()

    text = ""
    for event in activeSubscriptions:
        text = text + "Event " + str(event) + ": Subscribed" + "<br>"

    subscribtionInformation.html_text = text
    subscribtionInformation.rebuild()


def main():
    # Variables
    GameRunning = True
    connect = False

    while (GameRunning):

        display.fill(BACKGROUND_COLOR)
        time_delta = clock.tick(60)/1000.0
        ReadAndHandleInput(client, connect)

        # DrawObjects()
        updateText()

        updateNotifyData()

        manager.update(time_delta)
        manager.draw_ui(display)
        pygame.display.update()


def updateNotifyData():

    tempList = []
    tempList = clientObject.receivedData

    if len(clientObject.receivedData) == 0:
        return

    for data in tempList:
        print("ADDING DATA")
        eventInformationText.html_text = eventInformationText.html_text + \
            "Event: " + str(data[0]) + ", Message: " + \
            str(data[1]) + "<br>" + "<br>"
        clientObject.receivedData.remove(data)

    eventInformationText.rebuild()


def ConnectToServer(client):

    global connectButtonBoolean

    if ip_entry.text != "" and connectButtonBoolean == False:

        connectButtonBoolean = True
        print("Establishing connection", connectButtonBoolean)

        # ip_entry.get_text()

        clientObject.bindSocket(ip_entry.text)
        clientObject.startThread()
        connect_button.set_text("Disconnect")

    elif connectButtonBoolean == True:
        connectButtonBoolean = False

        print("Disconnecting")
        connect_button.set_text("Connect")
        clientObject.Destructor()


def sendMessage(operation):
    global connectButtonBoolean
    global activeSubscriptions

    if connectButtonBoolean == True:
        # We have a connections
        clientObject.sendToEventService(
            operation, rolldown_list.selected_option)

        if operation == "3":  # If operation is subscribeh
            if isDuplicate(rolldown_list.selected_option, activeSubscriptions) == False:
                activeSubscriptions.append(rolldown_list.selected_option)

        else:
            if isDuplicate(rolldown_list.selected_option, activeSubscriptions) == True:
                activeSubscriptions.remove(rolldown_list.selected_option)

    else:
        print("Not connected")
        return


def isDuplicate(value, list):
    for elem in list:
        if elem == value:
            return True
    return False


main()
