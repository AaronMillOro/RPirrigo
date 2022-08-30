# RPirrigo - automated watering system

## Required packages

The application requires the packages indicated on this [file](https://github.com/AaronMillOro/RPirrigo/blob/main/requirements.txt). 

```
pip install -r requirements.txt
```

## Sensitive data

For the correct performance of the main script, a **.env** file should be placed on the **src/** directory and should contain the following environment variables.
 
```
PORT = Number of port indicated by the SMTP server
SMTP_SERVER = SMTP server
SENDER_EMAIL = Email of the sender
RECEIVER_EMAIL = Email of the recipient
PASS = Password to access the SMTP server
IMG_DIR = Directory to store the cam images
LOGS = "/file.log"
```

## Running the application

The following command runs the application on a terminal.

```
python3 watering.py
```

Alternatively, there is the possibility to run the application automatically at startup of the RPi. To do so, a cron task should be declared on a terminal by typing:

```
crontab -e
```
Then, add the following line at the end of the file. It is really important the last "&" for the correct functionning of the RPi.

```
@reboot cd /path/to/RPirrigo/src && python3 watering.py &
```
After reboot the following command allows to verify the declared cron task.

```
systemctl status cron
```

Enjoy! :shipit: