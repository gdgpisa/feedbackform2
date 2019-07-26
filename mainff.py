from pathlib import Path
from gpiozero import Button, LED
import csv, time

# We use BCM scheme for GPIO ports
LEDS = {
    "red": {
        "GPIO": 14,
        "button": ""
    },
    "green": {
        "GPIO": 15,
        "button": ""
    },
    "blue": {
        "GPIO": 16,
        "button": ""
    }
}

BUTTONS = {
    "sad": {
        "GPIO": "4",
        "button": "",
        "rank": "🙁"
    },
    "normal": {
        "GPIO": "17",
        "button": "",
        "rank": "😐"
    },
    "happy": {
        "GPIO": "18",
        "button": "",
        "rank": "🙂"
    }
}

def blink(colour):
    for i in range(3):
        LEDS[colour]["button"].on()
        time.sleep(0.2)
        LEDS[colour]["button"].off()
        time.sleep(0.2)


def init():
    # Initializing LEDs following previous dictionary
    # The GPIO field represents the port to which the LED pin is connected
    # The button field contains the LED object
    for colour in LEDS:
        LEDS[colour]["button"] = LED(LEDS[colour]["GPIO"])
    # Initializing buttons following previous dictionary
    # The GPIO field represents the port to which the button is connected
    # The button field contains the Button object
    for key in BUTTONS:
        BUTTONS[key]["button"] = Button(BUTTONS[key]["GPIO"])
        BUTTONS[key]["button"].when_pressed = feedback

    # The event's title uses the format DD-MM-YYYY
    event_title = time.strftime("%d-%m-%Y", time.localtime())

    # Writing header of the CSV if it doesn't exists
    if not Path(event_title+".csv").exists():
        with open(event_title+".csv", "a+") as begin:
            feedback_file = csv.writer(begin, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            feedback_file.writerow(["Timestamp","Valutazione"])
    
    # Returns event's title avoiding to calculate it for every feedback
    return event_title


def feedback(port):
    # Obtaining the GPIO PIN from the Button object
    port = str(port.pin).replace("GPIO","")
    # Fallback value for rank
    rank = -1
    # Correct rank associated to the button
    for state in BUTTONS:
       if BUTTONS[state]["GPIO"] == port:
           rank = BUTTONS[state]["rank"]
    
    blink("blue")
    # Appending feedback into CSV
    with open(event_title+".csv", "a") as outfile:
        feedback_file = csv.writer(outfile)
        feedback_file.writerow([time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime()), str(rank)])
    blink("green")


if __name__ == "__main__":
    print("Avvio del programma")
    event_title = init()
    try:
        print("Settaggi di base correttamente impostati")
        print("Inizio ciclo di ascolto:")
        # Startup completed, starting blinking sequence
        blink("green")
        while True:
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nChiusura programma")

    except Exception as e:
        with open("log.json", "a") as log:
            log_file = csv.writer(log, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            log_file.writerow(["Timestamp","Error"])
            log_file.writerow([time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime()),str(e)])
        blink("red")
        print("Error: "+str(e))
