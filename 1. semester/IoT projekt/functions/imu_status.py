from imu import MPU6050
from time import sleep
from machine import Pin, I2C, PWM
import umqtt_robust2 as mqtt
import _thread
import IMUfunk
import tm1637


i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)  #her sætter vi alle vores variabler og definerer de pins der bliver brugt
imu = MPU6050(i2c)
tm = tm1637.TM1637(clk=Pin(4), dio=Pin(2))
buzzer = Pin(14, Pin.OUT)
tackling_status_ = 0
sprint_status_ = 0
status = False
fald_count = 0
sprint_start = False
skridt_tæller = 0
sprint_tæller = 0
acceleration = imu.accel
gyroscope = imu.gyro



def tackling_status(imu_control):
    global tackling_status_
    if imu_control == "start tacklinger" and tackling_status_ != 1: #tjekker om funktionen har fået lov til at køre
        tackling_status_ = 1                                        #ændrer den globale værdi
        _thread.start_new_thread(imu_tackling, ())                  #starter en thread
        _thread.exit()                                              #stopper thread
    elif imu_control == "stop tacklinger" and tackling_status_ != 0:#tjekker om funktionen er blevet bedt om at stoppe
        tackling_status_ = 0                                        #ændrer den globale værdi
        _thread.exit()
        
def sprint_status(imu_control):
    global sprint_status_
    if imu_control == "start sprint" and sprint_status_ != 1:
        sprint_status_ = 1
        _thread.start_new_thread(imu_sprint, ())
        _thread.exit()
    elif imu_control == "stop sprint" and sprint_status_ != 0:
        sprint_status_ = 0
        _thread.exit()
        
def imu_tackling():                                                 #funktion der bliver kaldt i funktionen ovenfor
    while True:
        global tackling_status_                                     #indhenter de globale værdier der bliver brugt i funktionen
        global status
        global acceleration
        global fald_count
        if tackling_status_ == 1:                                   #tjekker om den globale værdi er ændret
            print ("Acceleration x: ", round(acceleration.x,2), " y:", round(acceleration.y,2),
            "z: ", round(acceleration.z,2))
            sleep(0.2)
            IMUfunk.accel_x(0.8, 0)                                 #funktioner der er indhentet for at gøre det mere overskueligt
            IMUfunk.accel_y(0.8, 0)                                 #istedet for at skrive 3-4 linjer til hver kode
            IMUfunk.accel_z(0.8, 0)                                 #bliver alt koden skrevet på 3 linjer
            sleep(0.2)
            
            if acceleration.z > 0.8 and status == False:            #ændrer værdien på en global værdi hvis betingelser er mødt
                fald_count = fald_count + 1
                status = True
        
            if acceleration.x > 0.8 and status == False:            #ændrer værdien på en global værdi hvis betingelser er mødt
                fald_count = fald_count + 1
                status = True
        
            if acceleration.z < -0.8 and status == False:           #ændrer værdien på en global værdi hvis betingelser er mødt
                fald_count = fald_count + 1
                status = True
        
            if acceleration.x < -0.8 and status == False:           #ændrer værdien på en global værdi hvis betingelser er mødt
                fald_count = fald_count + 1
                status = True
            
            if acceleration.y > 0.8 and status == True:             #ændrer værdien på en global værdi hvis betingelser er mødt
                status = False
        
            
            print("tacklinger:", fald_count)
            sleep(2)
            mqtt.web_print(fald_count, "A6IoT/feeds/tacklinger")
            
            #printer variablen i shell
            tm.number(fald_count)
            #viser værdien på vores segment display
        elif tackling_status_ == 0:                                 #tjekker om funktionen er blevet bedt om at stoppe
            _thread.exit()                                          #lukker thread
            
        
def imu_sprint():
    while True:
        global sprint_status_                                      #indhenter de globale værdier der bliver brugt i funktionen
        global sprint_start
        global skridt_tæller
        global acceleration
        global gyroscope
        global sprint_tæller
        if sprint_status_ == 1:                                    #tjekker om den globale værdi er ændret og starter funktionen
            print("gyroscope x:", round(gyroscope.x,2))            #printer værdier i shell, mest for at vise os om koden kører
            sleep(0.2)                                             #bestemmer hvor ofte den printer værdier
            if gyroscope.x > 200:                                  #tjekker om betingelserne er mødt, ændrer en global værdi og printer i shell
                sprint_start = True
                print("SPRINT START")
        
            if 0 < gyroscope.x < 5:                                #tjekker om betingelserne er mødt, ændrer en global værdi og printer i shell
                sprint_start = False
                skridt_tæller = 0
                print("Jeg står stille")
            
            if acceleration.y > 1 and sprint_start == True:       #tjekker om betingelserne er mødt, ændrer en global værdi og printer i shell
                skridt_tæller = skridt_tæller + 1
                
            if skridt_tæller >= 10:
                sprint_tæller = sprint_tæller + 1
                print("skridts:", skridt_tæller)
                skridt_tæller = 0
                mqtt.web_print(sprint_tæller, "A6IoT/feeds/accel-visual")
                

        
            if sprint_tæller >= 10:                               #hvis betingelsen er mødt starter buzzeren, ændrer en global værdi og printer i shell
                beeper = PWM(Pin(14), freq=3000, duty=512)
                sleep(0.5)
                beeper.deinit()
                skridt_tæller = 0
                print("1 sprint")
        elif sprint_status_ == 0:                                 #tjekker om den globale værdi er ændret og stopper funktionen
            _thread.exit()                                        #stopper thread    
    