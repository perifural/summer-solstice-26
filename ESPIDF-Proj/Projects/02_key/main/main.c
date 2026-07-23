#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "stdio.h"
#include "led.h"
#include "key.h"

void app_main(void)
{
    led_init();
    key_init();
    vTaskDelay(pdMS_TO_TICKS(100));

    while(1)
    {
       led_set(key_scan(1));
       vTaskDelay(pdMS_TO_TICKS(1));
    }
}
