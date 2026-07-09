// -----------------------------------------------------
#include "bsp_motor_iic.hpp"

// -----------------------------------------------------
// Xbox controller
#include <XboxSeriesXControllerESP32_asukiaaa.hpp>
XboxSeriesXControllerESP32_asukiaaa::Core xboxController;

uint8_t isCtrl = 0;
int16_t ctrlSpd = 0;
int16_t ctrlDir = 0;
uint8_t ctrlA = 0;
uint8_t ctrlY = 0;

// Read Xbox controller input
void ctrlRead() {
  xboxController.onLoop();
  if(xboxController.isConnected()){
    isCtrl = 1;
    ctrlSpd = (-1) * (xboxController.xboxNotif.joyLVert - 32767);
    ctrlDir = xboxController.xboxNotif.joyRHori - 32767;
    ctrlA = xboxController.xboxNotif.btnA;
    ctrlY = xboxController.xboxNotif.btnY;
  }else{
    isCtrl = 0;
  }
}

// -----------------------------------------------------
void setup() {
  // Serial monitor setup
  Serial.begin(115200);
  
  // Xbox controller setup
  xboxController.begin();

  // Motor control setup
  IIC_Motor_Init();
  Set_motor_type(3);  // 3:测速码盘TT电机
	delay(100);
	Set_Pluse_Phase(45);
	delay(100);
	Set_Pluse_line(13);
	delay(100);
	Set_Wheel_dis(68.00);
	delay(100);
	Set_motor_deadzone(1850);
	delay(100);
}

void loop() {
  // Xbox controller read
  ctrlRead();

  // Xbox controller steady state tolerance
  if (ctrlSpd > -2500 && ctrlSpd < 2500) ctrlSpd = 0;
  if (ctrlDir > -2500 && ctrlDir < 2500) ctrlDir = 0;

  // Xbox controller input scaling
  ctrlSpd /= 15;
  ctrlDir /= 30;

  // Convert to motor speed
  int16_t spdL = constrain(ctrlSpd + ctrlDir, -2000, 2000);
  int16_t spdR = constrain(ctrlSpd - ctrlDir, -2000, 2000);

  // Motor speed control
  control_speed(spdL,spdR,spdL,spdR);

  // delay(100);

  // Read_10_Enconder();
  // Serial.print("M1:"); Serial.print(Encoder_Offset[0]); Serial.print("\t");
  // Serial.print("M2:"); Serial.print(Encoder_Offset[1]); Serial.print("\t");
  // Serial.print("M3:"); Serial.print(Encoder_Offset[2]); Serial.print("\t");
  // Serial.print("M4:"); Serial.print(Encoder_Offset[3]); Serial.println("\t");
  // delay(100);
}

