import time
import grovepi
import grove_rgb_lcd as lcd

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


try:
    while True:
        temp = read_temperature()
        print("Temperatur: {}°C".format(temp))
        lcd.setRGB(0, 255, 0)  # Hintergrundfarbe setzen
        lcd.setText("Temp:{} C".format(temp))
        
        # LEDs steuern
        if temp < 20:
            turn_on_led(LED_BLUE)
            turn_off_led(LED_GREEN)
            turn_off_led(LED_RED)
        elif 20 <= temp <= 25:
            turn_on_led(LED_GREEN)
            turn_off_led(LED_BLUE)
            turn_off_led(LED_RED)
        else:
            turn_on_led(LED_RED)
            turn_off_led(LED_GREEN)
            turn_off_led(LED_BLUE)
        
        time.sleep(2)  # Wartezeit, um die Messungen zu stabilisieren

except KeyboardInterrupt:
    print("Programm beendet. LEDs ausschalten...")
    turn_off_led(LED_RED)
    turn_off_led(LED_GREEN)
    turn_off_led(LED_BLUE)
    lcd.setText("\nSystem gestoppt")
    lcd.setRGB(0, 0, 0)  # Display ausschalten
    print("Alle LEDs aus.")

