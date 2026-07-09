#include "bsp_motor_iic.hpp"

#define UPLOAD_DATA 2  // 1:接收总的编码器数据 2:接收实时的编码器

void setup() {
  Serial.begin(115200);
  IIC_Motor_Init();

  Set_motor_type(3);  // 3:测速码盘TT电机
	delay(100);
	Set_Pluse_Phase(45);
	delay(100);
	Set_Pluse_line(13);
	delay(100);
	Set_Wheel_dis(68.00);
	delay(100);
	Set_motor_deadzone(1250);
	delay(100);
}

void loop() {
  for (int i = 0; i < 100; i++) {
    // control_speed(i * 10, i * 10, i * 10, i * 10);
		control_speed(0,0,0,0);
    delay(100);

    #if UPLOAD_DATA == 1
      Read_ALL_Enconder();
      Serial.print("M1:"); Serial.print(Encoder_Now[0]); Serial.print("\t");
      Serial.print("M2:"); Serial.print(Encoder_Now[1]); Serial.print("\t");
      Serial.print("M3:"); Serial.print(Encoder_Now[2]); Serial.print("\t");
      Serial.print("M4:"); Serial.print(Encoder_Now[3]); Serial.println("\t");
    #elif UPLOAD_DATA == 2
      Read_10_Enconder();
      Serial.print("M1:"); Serial.print(Encoder_Offset[0]); Serial.print("\t");
      Serial.print("M2:"); Serial.print(Encoder_Offset[1]); Serial.print("\t");
      Serial.print("M3:"); Serial.print(Encoder_Offset[2]); Serial.print("\t");
      Serial.print("M4:"); Serial.print(Encoder_Offset[3]); Serial.println("\t");
    #endif

    if (i == 100) i = 0;
  }
}

