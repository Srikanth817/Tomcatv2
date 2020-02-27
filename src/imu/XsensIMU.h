#ifndef I2C_H_
#define I2C_H_

#define I2C_BUS "/dev/i2c-2"

namespace tomcat {


class XsensIMU{
private:
	unsigned int bus;
	unsigned int device;
	int file;
public:
	 XsensIMU(unsigned int bus, unsigned int device);
	 int open();
	 int write(unsigned char value);
	 unsigned char* read (unsigned int number);
	 unsigned char* readRegisters(unsigned int number, unsigned int fromAddress=0);
	 void close();
	 ~XsensIMU();
};

} 
#endif