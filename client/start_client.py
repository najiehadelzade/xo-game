from client import Client
from constants import *
from graphic import init_graphic, events

def __main__():
    client = Client(SERVER_HOST, SERVER_PORT)
    while True:
        print("***************\n"
              "1. Connect to server\n"
              "2. Exit\n"
              "***************")
        choice = input("Enter your choice: ")
        if choice == "1":
            client.start()
            screen = init_graphic()
            events(screen, client)

        elif choice == "2":
            client.stop()
            break


if __name__ == "__main__":
    __main__()
