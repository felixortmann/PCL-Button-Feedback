import serial
import time

port = 'COM4'  # change port if not COM4
baudrate = 115200

signal = "b'happy\r\n'"


def receiveSignal():
    try:
        arduino = serial.Serial(port, baudrate)
        print("Connection successful!")

        try:

            while True:
                s = arduino.readline()
                signal = s
                print(s)
                time.sleep(1)

        finally:
            arduino.close()

    except:
        print("Failed Connection")


# signals: e.g. b'angry\r\n'
def evalSignal():
    s = signal
    x = s.replace('\r', '')
    y = x.replace('\n', '')

    res = y.split("'")[1]
    print(res)

    return res


evalSignal()