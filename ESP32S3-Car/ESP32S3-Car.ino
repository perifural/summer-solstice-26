#include "bsp_motor_iic.hpp"

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
  control_speed(0,0,0,0);
  delay(100);

  Read_10_Enconder();
  Serial.print("M1:"); Serial.print(Encoder_Offset[0]); Serial.print("\t");
  Serial.print("M2:"); Serial.print(Encoder_Offset[1]); Serial.print("\t");
  Serial.print("M3:"); Serial.print(Encoder_Offset[2]); Serial.print("\t");
  Serial.print("M4:"); Serial.print(Encoder_Offset[3]); Serial.println("\t");
  delay(100);
}

