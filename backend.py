import config
import smtplib
import imghdr
from email.message import EmailMessage

SENDER = config.gmail_user
PASSWORD = config.app_pass
RECEIVER = config.gmail_user
def send_email(img_path):
    print("send_email function has started")
    email_message = EmailMessage()
    # acts like a dict
    # Subject
    email_message["Subject"] = "New customer has arrived!"
    # body of email
    email_message.set_content("Hey, we just had a new visitor show up")
    # to add an attackment need to make a python file object

    with open(img_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content,
                                 maintype="image",  # file type
                                 subtype=imghdr.what(None, content)
                                 # this identfies the img type(png jpg and such)
                                 )
    gmail = smtplib.SMTP("smtp.gmail.com", 587) # creating server and host along with port
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function has ended")

if __name__ == "__main__":
    send_email(img_path="img/image40.png")