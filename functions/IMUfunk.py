from imu import MPU6050
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
imu = MPU6050(i2c)
acceleration = imu.accel

def accel_x(a, b):                                #skriver 3 funktioner her som gør den samlede kode kortere og nemmere at læse
    if abs(acceleration.x) > a:
        if (acceleration.x) > b:
            print("The x axis points upwards")
        else:
            print("the x axis points downwards")

def accel_y(a, b):
    if abs(acceleration.y) > a:
        if (acceleration.y) > b:
            print("The y axis points upwards")
        else:
            print("the y axis points downwards")
            
def accel_z(a, b):
    if abs(acceleration.z) > a:
        if (acceleration.z) > b:
            print("The z axis points upwards")
        else:
            print("the z axis points downwards")