import umqtt_robust2 as mqtt
from machine import Pin, ADC
from time import sleep
import _thread
import tm1637

battery_status_ = 0                                              #sætter global værdi og bestemmer pins der bliver brugt

analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)
tm = tm1637.TM1637(clk=Pin(4), dio=Pin(2))


def battery_status(battery_control):
    global battery_status_
    if battery_control == "start batt" and battery_status_ != 1: #funktionen tjekker om den har fået lov til at køre
        battery_status_ = 1                                      #ændrer den globale værdi
        _thread.start_new_thread(battery_percentage, ())         #starter en thread
        _thread.exit()                                           #stopper thread
    elif battery_control == "stop batt" and battery_status_ != 0:#tjekker om funktionen er blevet bedt om at stoppe
        battery_status_ = 0                                      #ændrer den globale værdi
        _thread.exit()                                           #stopper thread

def battery_percentage():
    while True:
        global battery_status_                                   #indhenter den globale værdi
        if battery_status_ == 1:                                 #tjekker om funtionen har fået lov til at køre
            analog_val = analog_pin.read()
            volts = (analog_val * 0.00089238)*5
            battery_percentage = (volts/2)*100 - 320             #udregner batteriprocent
            print('The battery percentage is:', battery_percentage,'%') #printer batteriprocent i shell
            mqtt.web_print(battery_percentage, 'A6IoT/feeds/battery-percentage') #sender batteriprocent til adafruit
            
            sleep(5)                                             #bestemmer hvor tit batteriprocent bliver printet i shell og sendt til adafruit
            tm.number(int(battery_percentage))                   #viser batteriprocent på segmentdisplayet som en integer, da man ikke kan vise floats på segmentdisplayet
            sleep (2)
        elif battery_status_ == 0:                               #tjekker om funktionen er blevet bedt om at stoppe
            _thread.exit()                                       #stopper thread
            