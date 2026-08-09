#ifndef __LED_H_
#define __LED_H_

#include "driver/gpio.h"

#define LED_GPIO_PIN GPIO_NUM_1

void led_init(void);
void led_set(uint8_t ledVal);
uint8_t led_stat();
void led_toggle();

#endif