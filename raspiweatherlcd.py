import time
import grovepi
import grove_rgb_lcd as lcd
import requests

# OpenWeatherMap API
API_KEY = "c62f2ea1c7b5315200507ced0f98ad3b"
CITY = "Zurich,CH"  # Ändere die Stadt nach Bedarf
URL = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(CITY, API_KEY)

# Ports definieren
TEMP_SENSOR = 2  # Angeschlossen am analogen Port A0
LED_RED = 5
LED_GREEN = 6
LED_BLUE = 4
I2C_PORT = 1

# Pins initialisieren
grovepi.pinMode(LED_RED, "OUTPUT")
grovepi.pinMode(LED_GREEN, "OUTPUT")
grovepi.pinMode(LED_BLUE, "OUTPUT")

def turn_on_led(pin):
    """Schaltet eine LED ein."""
    grovepi.digitalWrite(pin, 1)

def turn_off_led(pin):
    """Schaltet eine LED aus."""
    grovepi.digitalWrite(pin, 0)

def read_temperature():
    """Liest die Temperatur vom Sensor aus."""
    [temp, _] = grovepi.dht(TEMP_SENSOR, 0)
    return temp

def get_outdoor_temperature():
    """Holt die Außentemperatur von der Wetter-API."""
    try:
        response = requests.get(URL)
        data = response.json()
        return data["main"]["temp"]
    except:
        return None

try:
    while True:
        temp_indoor = read_temperature()
        temp_outdoor = get_outdoor_temperature()
        
        print("Indoor: {}°C | Outdoor: {}°C".format(temp_indoor, temp_outdoor))
        lcd.setRGB(0, 255, 0)  # Hintergrundfarbe setzen
        lcd.setText("Indoor: {}C\nOutdoor: {}C".format(temp_indoor, temp_outdoor))
        
        # LEDs steuern
        if temp_indoor < 20:
            turn_on_led(LED_BLUE)
            turn_off_led(LED_GREEN)
            turn_off_led(LED_RED)
        elif 20 <= temp_indoor <= 25:
            turn_on_led(LED_GREEN)
            turn_off_led(LED_BLUE)
            turn_off_led(LED_RED)
        else:
            turn_on_led(LED_RED)
            turn_off_led(LED_GREEN)
            turn_off_led(LED_BLUE)
        
        time.sleep(10)  # Aktualisiere alle 10 Sekunden

except KeyboardInterrupt:
    print("Programm beendet. LEDs ausschalten...")
    turn_off_led(LED_RED)
    turn_off_led(LED_GREEN)
    turn_off_led(LED_BLUE)
    lcd.setText("\nSystem gestoppt")
    lcd.setRGB(0, 0, 0)  # Display ausschalten
    print("Alle LEDs aus.")
