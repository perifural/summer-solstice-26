#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "led.h"

void app_main(void)
{
    led_init();
    vTaskDelay(500);

    while(1)
    {
        LED_TOGGLE();
        vTaskDelay(500);
    }
}
