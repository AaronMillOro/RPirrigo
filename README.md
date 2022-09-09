# RPirrigo - automated watering system

The motivation for this project was to put a Raspberry Pi in action in order to water the plants of my appartment. This with the aim to guarantee their survival during the summer break.

The developed system triggers two peristaltic pumps during a given
period of time (seconds), mainly to control the amount of water. Then, the Pi camera module is activated and takes a picture of the plants. Enventually, an email is sent with the lastest picture recorded. At each action, a log file stores the different actions of the program.

This project has two main blocs: the hardware elecronics and the software logic.

# Hardware

The reauired elements were: 

* Raspberry Pi 3b+ (RPi)
* Two peristaltic pumps operated at 12 V
* Power source of 12 V DC
* A 2-channel relay module of 5V (very important to be triggered at 5 V)
* Plastic tubes of 4 and 7 mm internal and external diameter, respectively
* Simple aquarium air regulators to control the water flow
* One gallon container to keep the water reservoir
* Cables
* (optional) Pi camera module 5M
* (optional) Wood box to attach the elements, in this case a used a Porto wine box

Below the distribution of the GPIOs of the RPi model 3b+. For this project, I connected the following pins:
* #2 (5 V) to power the relay
* #4 to the ground of the relay
* #16 and #32 to trigger the signals for the pumps 

<figure>
  <img
  src="https://github.com/AaronMillOro/RPirrigo/blob/main/img/rpi_gpio.png"
  alt="RPi 3b+ GPIO distribution">
  <figcaption>General Purpose Inputs/Outputs (GPIO) distribution of the RPi model 3b+</figcaption>
</figure>

The circuits connections are detailed in the following picture.

<figure>
  <img
  src="https://github.com/AaronMillOro/RPirrigo/blob/main/img/hardware.png"
  alt="hardware circuits">
  <figcaption>Connection of the RPi components with the relay, the peristaltic pumps and the Pi cam</figcaption>
</figure>

Some images of the watering system

![pumps and Pi cam attached to a Porto wine wood box](https://github.com/AaronMillOro/RPirrigo/blob/main/img/pumps_cam.png)


![5V relay channel next to RPi and peristaltic pumps](https://github.com/AaronMillOro/RPirrigo/blob/main/img/relay.png)

# Software

The logic was implement on python 3.8. The application requires the packages indicated on this [file](https://github.com/AaronMillOro/RPirrigo/blob/main/requirements.txt). 

```
pip install -r requirements.txt
```

In addition,  a directory named **img/** must be created at the same level of 
the directory **src/**. The snapshots will be stored on that directory.

```
user@pc:~/RPirrigo$ ls

img  README.md  requirements.txt  src
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

<figure>
  <img
  src="https://github.com/AaronMillOro/RPirrigo/blob/main/img/watering_syst.png"
  alt="watering system in action">
  <figcaption>System in action</figcaption>
</figure>


Enjoy! :shipit: