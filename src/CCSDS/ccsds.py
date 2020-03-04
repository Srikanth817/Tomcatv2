##########################################
# TOMCAT 2020 FSW package
# ASEN4018/4028 for Raytheon
#
# class for parsing/creating CCSDS packets
# written by: Katie Steward -- 02/16/20
# modified:   [Name] -- [Date]
##########################################

### NOTE ###
# if you're using this, you probably want to run either of these functions:
#     - ccsds.data_binary_to_ccsds_hex(file)
#     - ccsds.ccsds_hex_to_data_binary(file)

import os

class ccsds(object):
    def __init__(self, inputs=None, debug=False):
        self.debug = debug
        
    def read_in_file(self, file_string):
        """
        read file into single string (generally either binary or hex)
        """
        if self.debug:
            print("Reading in file: ",file_string)
            print("")
        file = open(file_string,"r")
        string = file.read()
        file.close()

        return string

    def hex_string_to_binary_string(self,hex_string):
        """
        reads in hex string with spaces and newlines and converts to binary string
        """

        # remove newlines and spaces
        hex_string = hex_string.replace(" ","")
        hex_string = hex_string.replace("\n","")

        if self.debug:
            print("CCSDS packet: ",hex_string)
            print()

        # convert hex to binary
        hex_length = len(hex_string);
        binary_string = bin(int(hex_string, 16))[2:].zfill((hex_length)*4)

        return binary_string

    def binary_to_hex_string(self,binary_string):
        """
        reads in binary string with spaces/newlines and converts to hex string
        """

	    # remove newlines and spaces
        binary_string = binary_string.replace(" ","")
        binary_string = binary_string.replace("\n","")

        # convert binary to hex
        hex_string = hex(int(binary_string,2))[2:]

        # NOTE!!! If we decide to fix packet length, will need to add a zfill here!!!
        #binary_length = len(binary_string)
        #hex_string = hex(binary_string).zfull(fixed_packet_length_in_hex_form)

        return hex_string

    def binary_string_to_hex(self,binary_string):
        """
        Convert binary string to hex
        NOTE: this is necessary because the binary is too long to use hex(int(binary)) w/out overflow
        """
        length = len(binary_string)
        if length%4 != 0:
            raise Exception('Length of binary ({}) not divisible by 4. Cannot convert to hex.'.format(length))
        else:
            hex_string = ''
            for i in range(0,length-1,4): ## beginning of each 4 bits (4bit = 1hex)
                binary = binary_string[i:i+4]
                if binary == '0000': hex_val = '0' 
                if binary == '0001': hex_val = '1' 
                if binary == '0010': hex_val = '2' 
                if binary == '0011': hex_val = '3' 
                if binary == '0100': hex_val = '4' 
                if binary == '0101': hex_val = '5' 
                if binary == '0110': hex_val = '6' 
                if binary == '0111': hex_val = '7' 
                if binary == '1000': hex_val = '8' 
                if binary == '1001': hex_val = '9' 
                if binary == '1010': hex_val = 'A' 
                if binary == '1011': hex_val = 'B' 
                if binary == '1100': hex_val = 'C' 
                if binary == '1101': hex_val = 'D' 
                if binary == '1110': hex_val = 'E' 
                if binary == '1111': hex_val = 'F' 

                hex_string = hex_string + hex_val

        return hex_string

    def decode_ccsds_header(self,binary):
        """
	    Decodes CCSDS header and returns binary data string from data field
	    """

	    # pull out CCSDS Version (Bits 0-2)
        version = int(binary[0:3],2)

        # pull out CCSDS Type (Bit 3) 
        # [0 if TLM, 1 if CMD]
        CCSDStype = int(binary[3],2)

        # pull out CCSDS Secondary Packet Header Flag (SHF) (Bit 4) 
        # [0 if FALSE, 1 if TRUE]
        sphf = int(binary[4],2)

        # pull out CCSDS APID (Bits 5-15) 
        apid = int(binary[5:16],2)

        # pull out CCSDS Sequence/Grouping Flags (Bits 16-17) 
        # [01 1st pkt; 00 cont pkt; 10 last pkt; 11 no group]
        seqflag = int(binary[16:18],2)

        # pull out CCSDS Sequence Count (Bits 18-31) 
        seqcount = int(binary[18:32],2)

        # pull out CCSDS Packet Data Length (Bits 32-47)
        # number ot octets of packet data field minus 1
        datalen = int(binary[32:48],2)

        # pull out CCSDS Packet Data Field Data (Bits 48 - end)
        data = binary[49:]

        # if DEBUG print out CCSDS data to screen
        if self.debug:
            print("CCSDS Version: ",binary[0:3],"(",str(version),")")
            print("CCSDS Type: ",binary[3],"(",str(CCSDStype),")")
            print("CCSDS SPHF: ",binary[4],"(",str(sphf),")")
            print("CCSDS APID: ",binary[5:16],"(",str(apid),")")
            print("CCSDS Sequence Flag: ",binary[16:18],"(",str(seqflag),")")
            print("CCSDS Sequence Count: ",binary[18:32],"(",str(seqcount),")")
            print("CCSDS Data Length: ",binary[32:48],"(",str(datalen),")")
            print("")
        return data

    def create_ccsds_header_hex(self,APID,seqflag,seqcount,datalen):
        """
        Puts packet info into CCDDS binary header
        """

        # pull out CCSDS Version (Bits 0-2)
        version_bits = bin(0)[2:].zfill(3)

        # pull out CCSDS Type (Bit 3) 
        # [0 if TLM, 1 if CMD] # TLM for our purposes
        type_bits = bin(0)[2:]

        # pull out CCSDS Secondary Packet Header Flag (SHF) (Bit 4) 
        # [0 if FALSE, 1 if TRUE] # FALSE for our purposes
        sphf_bits = bin(0)[2:]

        # pull out CCSDS APID (Bits 5-15) 
        apid_bits = bin(APID)[2:].zfill(11)

        # pull out CCSDS Sequence/Grouping Flags (Bits 16-17) 
        # [01 1st pkt; 00 cont pkt; 10 last pkt; 11 no group]
        seqflag_bits = bin(seqflag)[2:].zfill(2)

        # pull out CCSDS Sequence Count (Bits 18-31) 
        seqcount_bits = bin(seqcount)[2:].zfill(14)

        # pull out CCSDS Packet Data Length (Bits 32-47)
        # number ot octets of packet data field minus 1
        datalen_bits = bin(datalen-1)[2:].zfill(16)

        # combine header info
        header_binary = version_bits + type_bits + sphf_bits + apid_bits + \
	            seqflag_bits + seqcount_bits + datalen_bits

        # convert to hex 
        header_hex = self.binary_string_to_hex(header_binary)

        # if DEBUG print out bit data to screen
        if self.debug:
            #print("FUNCTION: create_ccsds_header_binary")
            print("CCSDS Version: ",version_bits," (",str(int(version_bits,2)),")")
            print("CCSDS Type: ",type_bits," (",str(int(type_bits,2)),")")
            print("CCSDS SPHF: ",sphf_bits," (",str(int(sphf_bits,2)),")")
            print("CCSDS APID: ",apid_bits," (",str(int(apid_bits,2)),")")
            print("CCSDS Sequence Flag: ",seqflag_bits," (",str(int(seqflag_bits,2)),")")
            print("CCSDS Sequence Count: ",seqcount_bits," (",str(int(seqcount_bits,2)),")")
            print("CCSDS Data Length: ",datalen_bits," (",str(int(datalen_bits,2)),")")
            print("Binary: ",header_binary)
            print("Hex: ",header_hex)
            print('')
        return header_hex

    def binary_to_hex_string(self,binary_string):
        """
        Reads in binary string with spaces/newlines and converts to hex string
        """

        # remove newlines and spaces
        binary_string = binary_string.replace(" ","")
        binary_string = binary_string.replace("\n","")

        # convert binary to hex
        hex_string = hex(int(binary_string,2))[2:]

        # NOTE!!! If we decide to fix packet length, will need to add a zfill here!!!
        #binary_length = len(binary_string)
        #hex_string = hex(binary_string).zfull(fixed_packet_length_in_hex_form)

        return hex_string

    def combine_header_with_data(self,header,data):
        """
        Take CCSDS header hex string and add data hex string
        """
        CCSDS_packet = header+data

        if self.debug:
            #print('FUNCTION: combine_header_with_data')
            print("CCSDS Packet: ",CCSDS_packet)
            print('')

        return CCSDS_packet

    def calculate_data_length(self,hex_data):
        """
        Take in hex data in string form and calculate data length for CCSDS packet
        NOTE: data length is represented as number of octets, or number of hex chars
        """
        data_len = int(len(hex_data))

        return data_len

    def ccsds_hex_to_data_binary(self,ccsds_hex_string):
        """
        Takes the hex string input of a ccsds packet and outputs the 
        raw data from the packet in string binary form
        """

        binary 			 = self.hex_string_to_binary_string(ccsds_hex_string)
        data 			 = self.decode_ccsds_header(binary)
        return data

    def data_hex_to_ccsds_hex(self,imu_hex_string,software_status):
        """
        Takes the string input of raw data binary and outputs
        the ccsds packet in string hex form
        """

        # string the IMU data and software status together
        data_hex_string = imu_hex_string + software_status

        # create the checksum and add that to the end
        checksum = self.create_checksum(data_hex_string)
        data_hex_string = data_hex_string + checksum

        # set these as defaults -- !!!could change later!!!
        APID = 1
        seqflag = 3
        seqcount = 1

        #data_hex_string     = self.binary_to_hex_string(data_binary_string)
        data_length         = self.calculate_data_length(data_hex_string)
        ccsds_header_string = self.create_ccsds_header_hex(APID,seqflag,seqcount,data_length)
        ccsds_packet        = self.combine_header_with_data(ccsds_header_string,data_hex_string)

        return ccsds_packet

    def create_checksum(self,data):
        a = [data[i:i+2] for i in range(0, len(data), 2)] 
        b = [int(i, 16) for i in a] 
        c = 256 - sum(b) % 256 
        checksum = hex(c)[2:]

        if self.debug:
            print("Checksum: ",checksum)

        return checksum


def main():
    """
    for debugging & such things
    """
    DEBUG = True

    # instatiate class & set debug to true
    ccsds_class = ccsds(debug=DEBUG)

    # declare file paths
    raw_data_file = "src\\CCSDS\\raw_data_for_testing.txt"
    CCSDS_packet_file = "src\\CCSDS\\ccsds_tlm_packet_for_testing.txt"

    if DEBUG:
        print("Starting from filepath: ",os.getcwd())
        print("")

    ##############################
    # PARSE CCSDS PACKET EXAMPLE #
    ##############################
    if DEBUG:
        print("==========================")
        print("PARSE CCSDS PACKET EXAMPLE")
        print("==========================")
        print("")

    ccsds_hex_string = ccsds_class.read_in_file(CCSDS_packet_file)
    data = ccsds_class.ccsds_hex_to_data_binary(ccsds_hex_string)

    if DEBUG:
        print("Data remaining excluding header: ")
        print(data)
        print("")

    ###############################
    # CREATE CCSDS PACKET EXAMPLE #
    ###############################
    if DEBUG:
        print("===========================")
        print("CREATE CCSDS PACKET EXAMPLE")
        print("===========================")
        print("")
    
    # create arbitrary software status
    software_status = '0000'

    data_binary_string  = ccsds_class.read_in_file(raw_data_file)
    data_hex_string     = ccsds_class.binary_to_hex_string(data_binary_string)
    packet = ccsds_class.data_hex_to_ccsds_hex(data_hex_string,software_status)
    

if __name__ == "__main__":
    main()