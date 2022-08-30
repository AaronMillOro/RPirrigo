"""
Main program to set a specific watering schedule.
One email with a photograph will be sent at the end
of each watering cycle
"""
import glob
import logging
import os
import smtplib, ssl
import time

from dotenv import dotenv_values
from email.message import EmailMessage
from picamera import PiCamera
import RPi.GPIO as GPIO
import schedule

# sensitive data
SRC_DIR = os.path.abspath(os.getcwd())
CONFIG_FILE = SRC_DIR + "/.env"
config = dotenv_values(CONFIG_FILE)
# GPIO setup 
RELAY_PIN = 36 # check RPi model and pin
RELAY_PIN2 = 16 # check RPi model and pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RELAY_PIN2, GPIO.OUT, initial=GPIO.LOW)
# logs
log_file = SRC_DIR + config["LOGS"]
logger = logging.getLogger("watering system")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s => %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_last_snapshot():
    """
    Logic to return the string of the lastest image captured on the
    images folder. This element will be attached to the notification
    email.
    """
    REPOSITORY = config["IMG_DIR"] + "*.jpg"
    files_directory = glob.glob(REPOSITORY) 
    latest_file = max(files_directory, key=os.path.getctime)
    return latest_file


def email_notification():
    """ Logic to send and email when the plants were watered """
    message = EmailMessage()
    message['Subject'] = "Plantitas"
    message['From'] = config["SENDER_EMAIL"]
    message['To'] = config["RECEIVER_EMAIL"]
    msg_content = """
    AMO, este mensaje es para confirmar que sus entes verdes han sido humectados.
    Cambio y fuera.
    La RPi  ^.^ 
    """
    message.set_content(msg_content)
    last_image = get_last_snapshot() 
    with open(last_image, "rb") as image_file:
        message.add_attachment(image_file.read(), maintype="image", subtype="jpg")
    with smtplib.SMTP(config["SMTP_SERVER"], config["PORT"]) as server:
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(config["SENDER_EMAIL"], config["PASS"])
        server.send_message(message)
    print("Email sent")
    logger.info("Email sent")


def snap_picture():
    """ Logic to get a picture from the picamera """
    filename = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
    cam = PiCamera()
    snapshot_file = config["IMG_DIR"] + filename + ".jpg"
    cam.capture(snapshot_file)
    cam.close()
    msg = "This picture was taken: " + snapshot_file.split("/")[-1]
    print(msg)
    logger.info(msg)


def activate_pump(gpio_number, seconds):
    """
    Logic to activate a water pump triggered by the GPIO pin number
    indicated as the first argument. The second argument indicates the
    time in seconds that the pin will be activated.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpio_number, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(gpio_number, GPIO.HIGH)
    time.sleep(seconds) # seconds
    msg = "Pump activated by GPIO " + str(gpio_number) + " during " + str(seconds) + " seconds"
    print(msg)
    logger.info(msg)    
    GPIO.output(gpio_number, GPIO.LOW)
    GPIO.cleanup()


def restart():
    """
    To reboot system. Interesting option for absence during long periods
    """
    logger.info("System rebooting ...")
    time.sleep(5)
    os.system("sudo reboot")


#----- Main program with defined tasks -----

#schedule.every().day.at("09:00:00").do(lambda: activate_pump(RELAY_PIN, 35))
#schedule.every().day.at("09:01:00").do(lambda: snap_picture())
#schedule.every().day.at("09:01:20").do(lambda: email_notification())
#schedule.every().sunday.at("18:00:00").do(lambda: restart())
#schedule.every().wednesday.at("18:00:00").do(lambda: restart())

schedule.every(3).hours.do(lambda: snap_picture())
schedule.every(3).hours.do(lambda: email_notification())
schedule.every(4).hours.do(lambda: restart())

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
