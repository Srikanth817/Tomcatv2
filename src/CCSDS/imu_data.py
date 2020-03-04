##########################################
# TOMCAT 2020 FSW package
# ASEN4018/4028 for Raytheon
#
# class for creating IMU packets
# written by: Katie Steward -- 02/29/2020
# modified:   [Name] -- [Date]
##########################################

### NOTE ###
# if you're using this, you probably want to run either of these functions:


import os
import inspect
import ccsds as ccsds_class

ccsds = ccsds_class.ccsds()

class imu_data(object):
    def __init__(self, inputs=None, debug=False):
        self.debug = debug

    def bytestring_to_hex(self, bytestring):
        # 80 hex chars (8*3 for accel, 8*3 for rate, 8 for temp, 24 for timestring

        hex_string = bytestring.hex().zfill(80)

        if self.debug:
            print("Bytestring: ",bytestring)
            print("Hex_string: ",hex_string)

        return hex_string

    def ccsds_wrap(self,data_hex_string):
        packet = ccsds.data_hex_to_ccsds_hex(data_hex_string)
        return packet

#    def bytestring_to_ccsds_packet(self,bytestring):
#        data_hex = self.bytestring_to_hex(bytestring)
#        packet = self.ccsds_wrap(data_hex)
#
#        return packet

def main():
    """
    for debugging & such things
    """
    DEBUG = True

    # instatiate class & set debug to true
    ccsds = ccsds_class.ccsds(debug=DEBUG)
    imu_class = imu_data(debug=DEBUG)

    if DEBUG:
        print("Starting from filepath: ",os.getcwd())
        print("")

    #############################
    # CREATE IMU PACKET EXAMPLE #
    #############################
    if DEBUG:
        print("=========================")
        print("CREATE IMU PACKET EXAMPLE")
        print("=========================")
        print("")
   
    #example bytestring:
    bytestring = b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA"

    # create arbitrary software status
    software_status = 'CC'

    # convert to CCSDS packet
    data_hex = imu_class.bytestring_to_hex(bytestring)
    packet = ccsds.data_hex_to_ccsds_hex(data_hex,software_status)

if __name__ == "__main__":
    main()