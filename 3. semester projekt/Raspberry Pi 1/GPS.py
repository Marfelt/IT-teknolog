import serial
import pynmea2
from time import sleep



def port_setup():
    possible_ports = ["/dev/ttyS0", "/dev/ttyAMA0", "/dev/serial0"]

    for port in possible_ports:
        try:
            ser = serial.Serial(port, baudrate=9600, timeout=5)
            return ser
        except serial.SerialException as e:
            print(f"Could not open port {port}: {e}")
    
    print("unable to to open any serial port")
    sleep(1)
    return port_setup()


def parseGPSdata(ser):
    keywords = ["$GPRMC", "$GPGGA"]
    gps_data = ser.readline()
    try:
        gps_data = gps_data.decode("utf-8")
    except UnicodeDecodeError:
        return None

    if len(gps_data) > 5:
        if gps_data[0:6] in keywords:
            gps_msg = pynmea2.parse(gps_data)
            lat = round(gps_msg.latitude, 4)
            lng = round(gps_msg.longitude, 4)
            return (lat, lng)
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    #gps_port = port_setup.possible_ports
    ser = port_setup()

    print("GPS coordinate Stream:")
    while True:
        try:
            gps_coords = parseGPSdata(ser)
            if gps_coords is None or gps_coords[0] == 0.0:
                print("No Data")
            else:
                print(f"latitude: {gps_coords[0]}, longitude: {gps_coords[1]}")
            sleep(5)

  #      except serial.SerialException as e:
   #         print(f"\nERROR: {e}")
    #        print("... reconnecting to serial\n")
     #       ser = port_setup(gps_port)

        except KeyboardInterrupt as e:
            print("--- Program shutting down ---")

        except serial.SerialException as e:
            print(f"\.ERROR: {e}")
        finally:
            if ser.is_open:
                ser.close()

