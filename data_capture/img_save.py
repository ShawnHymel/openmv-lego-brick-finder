import pyb, sensor, image, lcd, time

# Settings
btn_pin = 'P4'
led_color = 1
file_prefix = "/IMG"
file_suffix = ".bmp"
shutter_delay = 1000                # Milliseconds to wait after button press

# Globals
timestamp = time.ticks()
btn_flag = 0
btn_prev = 1
led_state = True
file_num = 0
filename = file_prefix + str(file_num) + file_suffix

####################################################################################################
# Functions

def file_exists(filename):
    try:
       f = open(filename, 'r')
       exists = True
       f.close()
    except OSError:
        exists = False
    return exists

####################################################################################################
# Main

# Start sensor
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect

# Start clock
clock = time.clock()

# Set up LED
led = pyb.LED(led_color)
led.off()

# Set up button
btn = pyb.Pin(btn_pin, pyb.Pin.IN, pyb.Pin.PULL_UP)

# Set up LCD
lcd.init()

# Figure where to start numbering files
while file_exists(filename):
    file_num += 1
    filename = file_prefix + str(file_num) + file_suffix

# Main while loop
while(True):

    # Update FPS clock
    clock.tick()

    # Get button state
    btn_state = btn.value()

    # Get image, print out resolution and FPS
    img = sensor.snapshot()
    print(img.width(), "x", img.height(), "FPS:", clock.fps())

    # If flag is set, countdown to shutter (blink LED) and save image
    if btn_flag == 1:
        if (time.ticks() - timestamp) <= shutter_delay:
            led_state = not led_state
            if led_state:
                led.on()
            else:
                led.off()
        else:
            btn_flag = 0
            led.off()
            img.save(filename)
            print("Image saved to:", filename)

    # If button is released, start shutter countdown
    if (btn_prev == 0) and (btn_state == 1):

        # Set flag and timestamp
        btn_flag = 1
        timestamp = time.ticks()

        # Figure out what to name file
        while file_exists(filename):
            file_num += 1
            filename = file_prefix + str(file_num) + file_suffix

    # Scale image (in place) and display on LCD
    lcd.display(img.mean_pool(2, 2))

    # Record button state
    btn_prev = btn_state
