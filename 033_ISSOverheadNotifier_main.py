import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 60.000000  # Your latitude
MY_LONG = 60.000000  # Your longitude

EMAIL_SUBJECT = "ISS overhead warning"
EMAIL_TEXT = "LOOK UP! IT'S ABOVE!"

my_email = ""
my_password = ""
email_receiver = ""


def send_email(email, subject, message_body):
    with smtplib.SMTP("smtp.gmail.com") as connection: # for gmail mailboxes
        connection.starttls()  # secure connection
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"Subject: {subject}\n\n{message_body}"
        )


def check_iss():
    # If the ISS is close to my current position...
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_is_near = False
    if abs(MY_LAT - iss_latitude) <= 5 and abs(MY_LONG - iss_longitude) <= 5:
        iss_is_near = True

    # ... and if it is currently dark
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(
        url="https://api.sunrise-sunset.org/json",
        params=parameters
    )
    response.raise_for_status()
    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    hour_now = datetime.now().hour
    is_dark = False
    if hour_now >= sunset_hour or hour_now <= sunrise_hour:
        is_dark = True

    # then return True or False
    if is_dark and iss_is_near:
        return True
    else:
        return False


while True:
    if check_iss():
        # print("Look up!")
        send_email(email_receiver, EMAIL_SUBJECT, EMAIL_TEXT)
    # else:
    #     print("Wait")
    time.sleep(60)
