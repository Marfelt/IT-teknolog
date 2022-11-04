import umqtt_robust2 as mqtt
from time import sleep
import _thread
import gps_status as gps_s
import imu_status as imu_s
import battery_percentage as battp
import gps_funktion

_thread.start_new_thread(gps_funktion.gps_main, ())


while True: #Her kalder og kører vi alle vores funktioner fra de andre filer
    
#     _thread.start_new_thread(gps_funktion.gps_main, ())
    try:
        
        if mqtt.besked == "start gps":                                #tjekker om den har fået start beskeden fra adafruit
            _thread.start_new_thread(gps_s.gps_stat, ("start gps",))  #starter en thread
            mqtt.besked = ""
            
        if mqtt.besked == "stop gps":                                 #tjekker om den har fået stop beskeden fra adafruit
            _thread.start_new_thread(gps_s.gps_stat, ("stop gps",))   #stopper thread
            mqtt.besked = ""
            
        if mqtt.besked == "start tacklinger":
            _thread.start_new_thread(imu_s.tackling_status, ("start tacklinger",))
            mqtt.besked = ""
        
        if mqtt.besked == "stop tacklinger":
            _thread.start_new_thread(imu_s.tackling_status, ("stop tacklinger",))
            mqtt.besked = ""
            
        if mqtt.besked == "start sprint":
            _thread.start_new_thread(imu_s.sprint_status, ("start sprint",))
            mqtt.besked = ""
            
        if mqtt.besked == "stop sprint":
            _thread.start_new_thread(imu_s.sprint_status, ("stop sprint",))
            mqtt.besked = ""
            
        if mqtt.besked == "start batt":
            _thread.start_new_thread(battp.battery_status, ("start batt",))
            mqtt.besked = ""
        
        if mqtt.besked == "stop batt":
            _thread.start_new_thread(battp.battery_status, ("stop batt",))
            mqtt.besked = ""
            
            

        mqtt.sync_with_adafruitIO()
        print('.', end = '')
        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()