import socket
import pygame_gui
import threading


class Client:
    def __init__(self):

        self.sock = None
        self.server_adress = None

        # Variables
        self.receivedData = []
        self.clientActive = True
        self.listenerThread = None

    def bindSocket(self, _server_adress):
        self.clientActive = True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_adress = (_server_adress, 1000)
            self.sock.bind(('0.0.0.0', 12345))

        except:
            print("Can't bind socket")

    def startThread(self):
          # Start threads
        self.listenerThread = threading.Thread(
            target=self.Thread_Listener, args=())
        self.listenerThread.start()

    def Destructor(self):
        self.clientActive = False
        # self.listenerThread.close()
        self.sock.close()

    def Thread_Listener(self):
        content = None

        while self.clientActive:

            try:
                content, ip = self.sock.recvfrom(1024)
            except Exception as e:
                print("############ Exception THROWN: ", e)
                break

            recievedMessage = content.decode("UTF-8")
            print("Recieved ", recievedMessage[0])

            if recievedMessage[0] == "5":
                notifyEvent = recievedMessage[1]
                notifyText = recievedMessage[2:]
                self.receivedData.append([notifyEvent, notifyText])

            elif recievedMessage[0] == "6":
                # error
                notifyText = "Error from: " + \
                    recievedMessage[0] + ", message: " + recievedMessage[1:]
                self.receivedData.append(notifyText[1:])
                print("error from: {}  {}", content[1], content[2:])

        print("killing listnerthread")

    def sendToEventService(self, operation, event):

        # Only allow 3, 4 as operations
        if operation == "3" or operation == "4":
            message = (operation + event).encode('utf8')

            print(self.server_adress)
            print("Message:", message)
            self.sock.sendto(message, self.server_adress)
            print("Sending message: ", message)
        else:
            print("Invalid operation input")
            return
