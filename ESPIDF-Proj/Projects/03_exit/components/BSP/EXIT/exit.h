#ifndef __EXIT_H_
#define __EXIT_H_

#include "driver/gpio.h"
#include "esp_system.h"

#define BOOT_INT_GPIO_PIN   GPIO_NUM_0

void exit_init(void);

#endif