/*
* ASEN 4028 Senior Projects -- TOMCAT
* Script for interfacing with an Xsens MTI-3 IMU.
* Requires XsensIMU.h/cpp to work
* Author: Srikanth Venkataraman
*
*/

#include <iostream>
#include "XsensIMU.h"
#include <unistd.h>
#include <pthread.h>
#include <cstdint>
#include <cstring>

using namespace std;
using namespace tomcat;


int main() {
	//Initialize new IMU object
	XsensIMU imu(2,0x6b);

	//Buffer to store data from I2C bus
	unsigned char* status_buffer ;
	//Get the status of the notification and measurement pipes
	status_buffer = imu.readRegisters((uint8_t)4,0x04);
	
	//Extract size of message waiting in each pipe
	uint16_t notificationSize;
	uint16_t measurementSize;

	notificationSize = (uint16_t)status_buffer[0] | ((uint16_t)status_buffer[1]<<8);
	measurementSize = (uint16_t)status_buffer[2] | ((uint16_t)status_buffer[3]<<8);
	// cout<<"Notification size: "<<hex<<notificationSize<<"\n";
	// cout<<"Measurement size: "<<hex<<measurementSize<<"\n";

	//Buffer to store measurements
	uint8_t* measurements;

	//Read from mmeasurement pipe
	measurements = imu.readRegisters(measurementSize,0x06);
	
	//Print for debugging
	// for(int i = 0; i < measurementSize; ++i){
	// 		cout<<i<<": "<<hex<<(int)(measurements[i])<<"\n";
	// 	}

	//Extract acceleration and rotation data
	float motionData[6];
	int indexes[6] = {23,27,31,38,42,46};
	uint8_t tempMeas[4];
	for (int i = 0;i<6;i++){
		
			tempMeas[0] = measurements[indexes[i]];
			tempMeas[1] = measurements[indexes[i]-1];
			tempMeas[2] = measurements[indexes[i]-2];
			tempMeas[3] = measurements[indexes[i]-3];
			memcpy(&motionData[i],&tempMeas,4);


	}
	uint8_t tempNano[4];
	uint32_t nanoTime;

	tempNano[0] = measurements[8];
	tempNano[1] = measurements[7];
	tempNano[2] = measurements[6];
	tempNano[3] = measurements[5];
	memcpy(&nanoTime,&tempNano,4);

	uint8_t tempYear[2];
	uint32_t year;
	tempYear[0] = measurements[10];
	tempYear[1] = measurements[9];
	memcpy(&year,&tempYear,2);

	uint16_t month = measurements[11];
	uint16_t day = measurements[12];
	uint16_t hour = measurements[13];
	uint16_t min = measurements[14];
	uint16_t sec = measurements[15];


	 cout<<"Time: "<<year<<"/"<<month<<"/"<<day<<" : "<<hour<<":"<<min<<":"<<sec<<"."<<nanoTime<<"\n";
	 cout<<"Acc 1: "<<motionData[0]<<" m/s^2"<<"\n";
	 cout<<"Acc 2: "<<motionData[1]<<" m/s^2"<<"\n";
	 cout<<"Acc 3: "<<motionData[2]<<" m/s^2"<<"\n";
	 cout<<"Rot 1: "<<motionData[3]<<" m/s"<<"\n";
	 cout<<"Rot 2: "<<motionData[4]<<" m/s"<<"\n";
	 cout<<"Rot 3: "<<motionData[5]<<" m/s"<<"\n";



	return 0;
}



