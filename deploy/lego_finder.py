# Edge Impulse - OpenMV Image Classification Example

import pyb, sensor, image, time, os, lcd, tf

# Settings
model_path = "trained.tflite"           # Path to tflite model file
labels_path = "labels.txt"              # Path to text file (one label on each line)
btn_pin = 'P4'                          # Pin that button is connected to
led_color = 1                           # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4
shutter_delay = 800                     # Milliseconds to wait after button press
led_off_delay = 200                     # Milliseconds to wait after turning off LED to snap photo
target_label = 'target'                 # See labels.txt for labels
target_thresh = 0.7                     # NN output for target label must be at least this prob.
sub_w = 32                              # Width (pixels) of window
sub_h = 32                              # Height (pixels) of window
hop = 10                                # Pixels between start of windows (vertical and horizontal)

# Globals
timestamp = time.ticks()
btn_flag = 0
btn_prev = 1
led_state = True
target_locations = []

####################################################################################################
# Main

# Set up sensor
sensor.reset()                          # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)     # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)       # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)           # Let the camera adjust.

# Load tflite model and labels
labels = [line.rstrip('\n') for line in open(labels_path)]

# Start clock
clock = time.clock()

# Set up LED
led = pyb.LED(led_color)
led.off()

# Set up button
btn = pyb.Pin(btn_pin, pyb.Pin.IN, pyb.Pin.PULL_UP)

# Load model
model = tf.load(model_path)

# Set up LCD
lcd.init()

# Main while loop
while(True):

    # Update FPS clock
    clock.tick()

    # Get button state
    btn_state = btn.value()

    # Get button state
    img = sensor.snapshot()

    # Initialize top-left markers for sub-image window
    px_left = 0
    px_top = 0

    # If flag is set, count down to shutter (blink LED) and look for target
    if btn_flag == 1:
        if (time.ticks() - timestamp) <= shutter_delay:
            led_state = not led_state
            if led_state:
                led.off()
            else:
                led.on()
        else:

            # Reset flag
            btn_flag = 0

            # Turn off LED to get snapshot, then turn it back on to show it's processing
            led.off()
            time.sleep(led_off_delay)
            img = sensor.snapshot()
            led.on()

            # Crop out sub-image window and run through tflite model (does window contain target?)
            target_locations = []
            total_inference_time = 0
            num_inference_cnt = 0
            while(px_top + sub_h <= img.height()):
                while(px_left + sub_w <= img.width()):

                    # Measure time start
                    start_time = time.ticks()

                    # Crop out window
                    img_crop = img.copy((px_left, px_top, sub_w, sub_h))

                    # Classfiy window (is it our target?), get output probability
                    tf_out = model.classify(img_crop)
                    target_prob = tf_out[0].output()[labels.index(target_label)]

                    # If it is our target, add location and probability to list
                    if target_prob >= target_thresh:
                       prob_str = str("{:.2f}".format(round(target_prob, 2)))
                       target_locations.append((px_left, px_top, prob_str))

                    # Record time to perform inference
                    total_inference_time += (time.ticks() - start_time)
                    num_inference_cnt += 1

                    # Move window to the right
                    px_left += hop

                # Move window down (and reset back to left)
                px_top += hop
                px_left = 0

            # Turn off LED to show we're done
            led.off()

            # Report average inference time
            print()
            print("Number of possible targets found:", len(target_locations))
            print("Average inference time:", total_inference_time / num_inference_cnt, "ms")
            print("Number of inferences performed:", num_inference_cnt)
            print("Total computation time:", total_inference_time / 1000, "s")

    # Draw target locations and probabilities onto image
    for loc in target_locations:
        img.draw_rectangle((loc[0], loc[1], sub_w, sub_h))
        img.draw_string(loc[0] + 1, loc[1], loc[2], mono_space=False)

    # If button is released, start shutter countdown
    if (btn_prev == 0) and (btn_state == 1):

        # Set flag and timestamp
        btn_flag = 1
        timestamp = time.ticks()

    # Scale image and display on LCD
    lcd.display(img.mean_pool(2, 2))

    # Display info to terminal
    #print("FPS:", clock.fps())

    # Record button state
    btn_prev = btn_state
