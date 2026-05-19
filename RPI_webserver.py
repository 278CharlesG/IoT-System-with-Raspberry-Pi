from flask import Flask, render_template
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from RPLCD.i2c import CharLCD

app = Flask(__name__, template_folder="/home/pi/template")
lcd = CharLCD('PCF8574', 0x27)
lcd.clear()
GPIO.setmode(GPIO.BCM)

# Pin assignments
led1 = 18  # LED6
led2 = 23  # LED5
led3 = 25  # LED3
led4 = 24  # LED4
led5 = 8   # LED2
buzzer = 26
DHT11_pin = 4

# Initialize GPIO pins
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)
GPIO.setup(led5, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

# Set initial states
GPIO.output(led1, GPIO.LOW)
GPIO.output(led2, GPIO.LOW)
GPIO.output(led3, GPIO.LOW)
GPIO.output(led4, GPIO.LOW)
GPIO.output(led5, GPIO.LOW)
GPIO.output(buzzer, GPIO.LOW)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/<pin>/<action>")
def action(pin, action):
    temperature = ''
    humidity = ''
    
    # LED and buzzer control
    if pin == "led6" and action == "on":
        GPIO.output(led1, GPIO.HIGH)
    if pin == "led6" and action == "off":
        GPIO.output(led1, GPIO.LOW)

    if pin == "led5" and action == "on":
        GPIO.output(led2, GPIO.HIGH)
    if pin == "led5" and action == "off":
        GPIO.output(led2, GPIO.LOW)

    if pin == "led3" and action == "on":
        GPIO.output(led3, GPIO.HIGH)
    if pin == "led3" and action == "off":
        GPIO.output(led3, GPIO.LOW)

    if pin == "led4" and action == "on":
        GPIO.output(led4, GPIO.HIGH)
    if pin == "led4" and action == "off":
        GPIO.output(led4, GPIO.LOW)

    if pin == "led2" and action == "on":
        GPIO.output(led5, GPIO.HIGH)
    if pin == "led2" and action == "off":
        GPIO.output(led5, GPIO.LOW)

    if pin == "buzzer" and action == "on":
        GPIO.output(buzzer, GPIO.HIGH)
    if pin == "buzzer" and action == "off":
        GPIO.output(buzzer, GPIO.LOW)

    # DHT11 sensor reading
    if pin == "dhtpin" and action == "get":
        humi, temp = dht.read_retry(dht.DHT11, DHT11_pin)
        if humi is not None and temp is not None:
            humi = '{0:0.1f}'.format(humi)
            temp = '{0:0.1f}'.format(temp)
            temperature = 'Temp: ' + temp + '°C'
            humidity = 'Humidity: ' + humi + '%'
            display_on_lcd(temperature, humidity)
        else:
            temperature = "Temp: Error"
            humidity = "Humidity: Error"
            display_on_lcd(temperature, humidity)

    templateData = {
        'temperature': temperature,
        'humidity': humidity,
        'led6_state': 'ON' if GPIO.input(led1) else 'OFF',
        'led5_state': 'ON' if GPIO.input(led2) else 'OFF',
        'led3_state': 'ON' if GPIO.input(led3) else 'OFF',
        'led4_state': 'ON' if GPIO.input(led4) else 'OFF',
        'led2_state': 'ON' if GPIO.input(led5) else 'OFF',
        'buzzer_state': 'ON' if GPIO.input(buzzer) else 'OFF'
    }

    return render_template('main.html', **templateData)

def display_on_lcd(temp, hum):
    try:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(temp[:16].ljust(16))
        lcd.cursor_pos = (1, 0)
        lcd.write_string(hum[:16].ljust(16))
    except Exception as e:
        print(f"LCD Error: {e}")

def cleanup():
    try:
        lcd.clear()
        lcd.write_string("System off")
    except Exception as e:
        print(f"Cleanup Error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        app.run(host='10.0.0.2', port=80, debug=True)
    finally:
        cleanup()