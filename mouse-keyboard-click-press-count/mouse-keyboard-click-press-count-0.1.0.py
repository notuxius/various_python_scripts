from pynput.mouse import Listener as mouse_listener
from pynput.mouse import Button
from pynput.keyboard import Listener as keyboard_listener
import os
import platform
import sys
import datetime

# Suppress echo of chars when pressing keys in console on Linux/Mac?
if platform.system() != "Windows":
    os.system("stty -echo")

else:
    # Disable selection on Windows console to fix freezing of mouse clicks in it
    import win32console

    ENABLE_QUICK_EDIT_MODE = 0x40
    ENABLE_EXTENDED_FLAGS = 0x80
    screen_buffer = win32console.GetStdHandle(-10)
    orig_mode = screen_buffer.GetConsoleMode()
    new_mode = orig_mode & ~ENABLE_QUICK_EDIT_MODE
    screen_buffer.SetConsoleMode(new_mode | ENABLE_EXTENDED_FLAGS)

time_left_click = ""
time_right_click = ""
time_other_click = ""

count_left_button = 0
count_right_button = 0
count_other_button = 0

time_first_click = ""
time_last_click = ""
time_prev_click = ""

time_format = "%d/%m/%Y %H:%M:%S.%f"

try:
    if not os.path.isfile("mkcpc-report-file.txt"):

        with open("mkcpc-report-file.txt", "w+") as mkcpcw:
            print("Created report mkcpc-report-file.txt file")

    else:
        with open("mkcpc-report-file.txt", "w+") as mkcpcw:
            print("Truncated report mkcpc-report-file.txt file")

except PermissionError:
    print("\nCannot create or modify mkcpc-report-file.txt report file")
    sys.exit(1)

delimiter = "--------------------------------------------------\n"

mkcpcrk_lines = []


def on_click(x, y, button, pressed):
    if pressed:

        with open("mkcpc-report-file.txt", "r+") as mkcpcrk:

            klines = mkcpcrk.readlines()

            for line_number, line in enumerate(klines):
                if line.strip() == "Keyboard stats:":
                    mkcpcrk_lines.extend(klines[line_number:])

        with open("mkcpc-report-file.txt", "w+") as mkcpcw:

            if button == Button.left:
                global time_left_click
                time_left_click = datetime.datetime.now()
                global count_left_button
                count_left_button += 1

            elif button == Button.right:
                global time_right_click
                time_right_click = datetime.datetime.now()
                global count_right_button
                count_right_button += 1

            else:
                global time_other_click
                time_other_click = datetime.datetime.now()
                global count_other_button
                count_other_button += 1

            total_count = count_left_button + count_right_button + count_other_button

            mkcpcw.write("Mouse stats: " + "\n")
            mkcpcw.write(delimiter)

            mkcpcw.write("Left button click count: " + str(count_left_button) + "\n")
            if count_left_button > 0:
                mkcpcw.write("Time of left button click: " + time_left_click.strftime(time_format)[:-4] + "\n")
            mkcpcw.write("\n")

            mkcpcw.write("Right button click count: " + str(count_right_button) + "\n")
            if count_right_button > 0:
                mkcpcw.write("Time of right button click: " + time_right_click.strftime(time_format)[:-4] + "\n")
            mkcpcw.write("\n")

            mkcpcw.write("Other button click count: " + str(count_other_button) + "\n")
            if count_other_button > 0:
                mkcpcw.write("Time of other button click: " + time_other_click.strftime(time_format)[:-4] + "\n")
            mkcpcw.write("\n")

            global time_first_click

            if total_count > 0 and not time_first_click:
                time_first_click = datetime.datetime.now()
                mkcpcw.write("Time of any first click: " + time_first_click.strftime(time_format)[:-4] + "\n")
            else:
                mkcpcw.write("Time of any first click: " + time_first_click.strftime(time_format)[:-4] + "\n")

            time_last_click = datetime.datetime.now()

            mkcpcw.write("Time of any last click: " + time_last_click.strftime(time_format)[:-4] + "\n")
            mkcpcw.write("\n")

            mkcpcw.write("Total buttons click count: " + str(total_count) + "\n\n")

            if total_count == 1:
                print("Click " + "{0:08d}".format(total_count))

            if total_count > 1:
                total_time_delta = str(time_last_click - time_first_click)
                mkcpcw.write("Total clicking time: " + total_time_delta[:-4] + "\n")

                global time_prev_click

                if not time_prev_click:
                    time_prev_click = time_first_click

                current_time_delta = str(time_last_click - time_prev_click)

                # TODO improve avg clicks detection

                current_avg_clicks_per_sec = 1 / float(current_time_delta.replace(":", ""))

                mkcpcw.write("Current avg clicks per second: " + str(current_avg_clicks_per_sec)[:4] + "\n\n")

                # total_clicks_per_sec = total_count / float(total_time_delta.replace(":", ""))
                # mkcpcw.write("Total avg clicks per second: " + str(total_clicks_per_sec)[:4] + "\n")

                print("Click " + "{0:08d}".format(total_count) + " | " + "Total time: " + total_time_delta[:-4] +
                      " | " + "Avg: " + str(current_avg_clicks_per_sec)[:4])

                time_prev_click = time_last_click

            for line in mkcpcrk_lines:
                mkcpcw.write(line)

            mkcpcrk_lines.clear()


keyboard_chars_and_count = {}
mkcpcrm_lines = []


def on_press(key):
    # TODO transform keysfrom any keyboard layout into eng

    with open("mkcpc-report-file.txt", "r+") as mkcpcrm:

        for line in mkcpcrm:
            if line.strip() != "Keyboard stats:":
                mkcpcrm_lines.extend(line)
            else:
                break

    with open("mkcpc-report-file.txt", "w+") as mkcpcw:
        for line in mkcpcrm_lines:
            mkcpcw.write(line)

        mkcpcrm_lines.clear()

        if key not in keyboard_chars_and_count.keys():
            keyboard_chars_and_count[key] = 1

        else:
            keyboard_chars_and_count[key] += 1

        mkcpcw.write("Keyboard stats: " + "\n")
        mkcpcw.write(delimiter)

        mkcpcw.write("Different keys press count: " + str(len(keyboard_chars_and_count)) + "\n")

        mkcpcw.write("Total keys press count: " + str(sum(keyboard_chars_and_count.values())) + "\n\n")

        sorted_keyboard_chars_and_count = [(k, keyboard_chars_and_count[k]) for k
                                           in sorted(keyboard_chars_and_count,
                                                     key=keyboard_chars_and_count.get, reverse=True)]

        for k, v in sorted_keyboard_chars_and_count:
            mkcpcw.write("Press count: " + str(k) + ": " + str(v) + "\n")

        # TODO also create avg total time for keyboard stats
        print("Press count: " + str(key) + ": " + str(keyboard_chars_and_count[key]) + \
              " | " + "Diff keys: " + str(len(keyboard_chars_and_count)) + " | " \
              + "Total keys: " + str(sum(keyboard_chars_and_count.values())))


if __name__ == "__main__":

    # TODO allow only one instance of app

    try:

        klistener = keyboard_listener(on_press=on_press)
        klistener.start()

        with mouse_listener(on_click=on_click) as mlistener:
            mlistener.join()

    except KeyboardInterrupt:
        sys.exit(0)

    except FileNotFoundError:
        print("\nReport mkcpc-report-file.txt file was removed or renamed")

    input("Enter key to exit\n")
