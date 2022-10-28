from imu import MPU6050
from time import sleep
from machine import Pin, I2C
import umqtt_robust2 as mqtt
import _thread
import IMUfunk

imu_status = 0
status = False
fald_count = 0
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
imu = MPU6050(i2c)
acceleration = imu.accel


def tackling_status(imu_control):
    global imu_status
    if imu_control == "start" and imu_status != 1:
        imu_status = 1
        _thread.start_new_thread(imu_tackling, ())
        _thread.exit()
    elif imu_control == "stop" and imu_status != 0:
        imu_status = 0
        _thread.exit()
        
# def sprint_status(imu_control):
#     global imu_status
#     if imu_control == "start" and imu_status != 1:
#         imu_status = 1
#         _thread.start_new_thread(imu_tackling, ())
#         _thread.exit()
#     elif imu_control == "stop" and imu_status != 0:
#         imu_status = 0
#         _thread.exit()
        
def imu_tackling():
    while True:
        global imu_status
        if imu_status == 1:
            print ("Acceleration x: ", round(acceleration.x,2), " y:", round(acceleration.y,2),
            "z: ", round(acceleration.z,2))
            sleep(0.2)
            IMUfunk.accel_x(0.8, 0)
            IMUfunk.accel_y(0.8, 0)
            IMUfunk.accel_z(0.8, 0)
            sleep(0.2)
            
            if acceleration.z > 0.8 and status == False:
                fald_count = fald_count + 1
                status = True
        
            if acceleration.x > 0.8 and status == False:
                fald_count = fald_count + 1
                status = True
        
            if acceleration.z < -0.8 and status == False:
                fald_count = fald_count + 1
                status = True
        
            if acceleration.x < -0.8 and status == False:
                fald_count = fald_count + 1
                status = True
            
            if acceleration.y > 0.8 and status == True:
                status = False
        
            print("tacklinger:", fald_count)
        elif imu_status == 0:
            _thread.exit()
            
        

        
            
# def imu_sprint():
    
    