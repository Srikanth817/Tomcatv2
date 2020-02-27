#include <iostream>
#include "XsensIMU.h"
#include <unistd.h>
#include <pthread.h>
#include <cstdint>
#include <cstring>

using namespace std;
using namespace tomcat;


int main() {

	XsensIMU imu(2,0x6b);



	//imu.write(0x04);

	unsigned char* status_buffer ;//= new unsigned char[4];

	status_buffer = imu.readRegisters((uint8_t)4,0x04);
	
	uint16_t notificationSize;
	uint16_t measurementSize;

	notificationSize = (uint16_t)status_buffer[0] | ((uint16_t)status_buffer[1]<<8);
	measurementSize = (uint16_t)status_buffer[2] | ((uint16_t)status_buffer[3]<<8);
	cout<<"Notification size: "<<hex<<notificationSize<<"\n";
	cout<<"Measurement size: "<<hex<<measurementSize<<"\n";

	//imu.write(0x06);
	
	uint8_t* measurements;
	
	measurements = imu.readRegisters(measurementSize,0x06);
	
	for(int i = 0; i < measurementSize; ++i){
			cout<<i<<": "<<hex<<(int)(measurements[i])<<"\n";
		}

	float fangle1;
	uint8_t angle1[4];
	angle1[0] = measurements[20];
	angle1[1] = measurements[19];
	angle1[2] = measurements[18];
	angle1[3] = measurements[17];
	memcpy(&fangle1,&angle1,4);

	float fangle2;
	uint8_t angle2[4];
	angle2[0] = measurements[24];
	angle2[1] = measurements[23];
	angle2[2] = measurements[22];
	angle2[3] = measurements[21];
	memcpy(&fangle2,&angle2,4);

	float fangle3;
	uint8_t angle3[4];
	angle3[0] = measurements[28];
	angle3[1] = measurements[27];
	angle3[2] = measurements[26];
	angle3[3] = measurements[25];
	memcpy(&fangle3,&angle3,4);


	cout<<"\n";
	cout<<"Angle 1: "<<fangle1<<" Degrees"<<"\n";
	cout<<"Angle 2: "<<fangle2<<" Degrees"<<"\n";
	cout<<"Angle 3: "<<fangle3<<" Degrees"<<"\n";


	// imu.write(0xFA);
	// imu.write(0xFF);
	// imu.write(0x00);
	// imu.write(0x00);
	// imu.write(0x01);

	
	



	return 0;
}



