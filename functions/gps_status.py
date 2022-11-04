import gps_funktion
import micropyGPS
import umqtt_robust2 as mqtt
from time import sleep
import _thread

gps_status_ = 0


def gps_stat(status_gps):
    global gps_status_
    if status_gps == "start gps" and gps_status_ != 1:  #funktionen tjekker om den har fået lov til at køre
        gps_status_ = 1                                 #funktionen ændrer variablens værdi, som den anden funktion kigger på
        _thread.start_new_thread(gps_lokation, ())      #starter tråd
        _thread.exit()                                  #stopper tråd
    elif status_gps == "stop gps" and gps_status_ != 0: #funktionen tjekker om den er bedt om at stoppe
        gps_status_ = 0
        _thread.exit()

def gps_lokation():
    while True:
        global gps_status_                              #indhenter den globale variabel
        if gps_status_ == 1:                            #tjekker om den anden funktion har givet den lov til at køre
            sleep(2)                                    #bestemmer hvor ofte der bliver sendt data til adafruit
            gps_data = gps_funktion.gps_to_adafruit
            print(f"\ngps_data er: {gps_data}")         #printer gps data i shell
            mqtt.web_print(gps_data, 'A6IoT/feeds/mapfeed/csv') #sender data til et bestemt feed i adafruit
            sleep(10)
        elif gps_status_ == 0:                          #stopper funktionen hvis den anden funktion får stop værdien
            _thread.exit()
        