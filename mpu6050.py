from mpu6050 import *
import time

mpu_file_name = 'mpu.csv'


def SelectAccelRange() -> int:
    print('\n\n', '*' * 5, "SELECT ACCEL RANGE", '*' * 5)

    while True:
        print("1) 2G")
        print("2) 4G")
        print("3) 8G")
        print("4) 16G")
        
        try:
            range = int(input("Select accel range: "))

            if range == 1:
                return ACCEL_RANGE_2G
            elif range == 2:
                return ACCEL_RANGE_4G
            elif range == 3:
                return ACCEL_RANGE_8G
            elif range == 4:
                return ACCEL_RANGE_16G 

            else:
                print("ERROR SELECT ACCEL RANGE\n")
                continue

        except:
            print("ERROR SELECT ACCEL RANGE\n")


def SelectGyroRange() -> int:
    print('\n\n', '*' * 5, "SELECT GYRO RANGE", '*' * 5)
    
    while True:
        print("1) 250 deg")
        print("2) 500 deg")
        print("3) 1000 deg")
        print("4) 2000 deg")
        
        try:
            range = int(input("Select gyro range: "))

            if range == 1:
                return GYRO_RANGE_250DEG
            elif range == 2:
                return GYRO_RANGE_500DEG
            elif range == 3:
                return GYRO_RANGE_1000DEG
            elif range == 4:
                return GYRO_RANGE_2000DEG 

            else:
                print("ERROR SELECT GYRO RANGE\n")
                continue

        except:
            print("ERROR SELECT GRYO RANGE\n")
    

def SelectType():
    print('\n\n', '*' * 5, "SELECT TYPE", '*' * 5)

    gyro = False
    accel = False

    while True:
        print("1) Only gyro")
        print("2) Only accel")
        print("3) Gyro and accel")
        
        try:
            sel = int(input("Select type sensor: "))

            if sel == 1:
                gyro = True
                break
            elif sel == 2:
                accel = True
                break
            elif sel == 3:
                accel = True
                gyro = True
                break

            else:
                print("ERROR SELECT TYPE\n")
                continue

        except:
            print("ERROR SELECT TYPE\n")

    
    return gyro, accel


def SelectFilter() -> int:
    print('\n\n', '*' * 5, "SELECT FILTER", '*' * 5)

    while True:
        print("1) 256")
        print("2) 188")
        print("3) 98")
        print("4) 42")
        print("5) 20")
        print("6) 10")
        print("7) 5")
        print("0) NO")

        try:
            filt = int(input("Select filter: "))

            if range == 1:
                return FILTER_BW_256
            elif range == 2:
                return FILTER_BW_188
            elif range == 3:
                return FILTER_BW_98
            elif range == 4:
                return FILTER_BW_42 
            elif range == 5:
                return FILTER_BW_20
            elif range == 6:
                return FILTER_BW_10
            elif range == 7:
                return FILTER_BW_5
            elif range == 0:
                return -1

            else:
                print("ERROR SELECT FILTER\n")
                continue

        except:
            print("ERROR SELECT FILTER\n")



if __name__ == '__main__':

    mpu = mpu6050(0x68)

    is_gyro, is_accel = SelectType()

    if is_accel:
        accel_range = SelectAccelRange()
        mpu.set_accel_range(accel_range)

    if is_gyro:
        gyro_range = SelectGyroRange()
        mpu.set_gyro_range(gyro_range)


    filt = SelectFilter()
    if filt != -1:
        mpu.set_filter_range(filt)


    mpu_file = open(mpu_file_name, 'w')

    settings = f'gyro: {is_gyro}, accel: {is_accel}, filter: {filt}\n'
    mpu_file.write(settings)

    while True:
        str_gyro = ''
        if is_gyro:
            gyro_data = mpu.get_gyro_data()

            Gx = gyro_data['x']
            Gy = gyro_data['y']
            Gz = gyro_data['z']

            str_gyro = f'{Gx}, {Gy}, {Gz}, '

        if is_accel:
            accel_data = mpu.get_accel_data()

            Ax = accel_data['x']
            Ay = accel_data['y']
            Az = accel_data['z']

            str_accel = f'{Ax}, {Ay}, {Az}, '

        str_writen = str_gyro + str_accel + f"{time.time()}\n"

        mpu_file.write()


    mpu_file.close()
