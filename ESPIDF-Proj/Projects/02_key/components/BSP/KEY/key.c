#include "key.h"

void key_init(void)
{
    gpio_config_t gpio_init_struct = {0};
    gpio_init_struct.intr_type = GPIO_INTR_DISABLE;
    gpio_init_struct.mode = GPIO_MODE_INPUT;
    gpio_init_struct.pull_up_en = GPIO_PULLUP_ENABLE;
    gpio_init_struct.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpio_init_struct.pin_bit_mask = 1ull << BOOT_GPIO_PIN;
    gpio_config(&gpio_init_struct);

}

uint8_t key_scan(uint8_t keyMode)  // mode: continuous press detection. 
{
    uint8_t keyVal = 0;
    static uint8_t keyRead = 1;

    if (keyMode)
    {
        keyRead = 1;
    }

    if (keyRead && (gpio_get_level(BOOT_GPIO_PIN) == 0))
    {
        keyRead = 0;
        vTaskDelay(10);

        if (gpio_get_level(BOOT_GPIO_PIN) == 0)
        {
            keyVal = 1;
        }
    }
    else if (gpio_get_level(BOOT_GPIO_PIN) == 1)
    {
        keyRead = 1;
    }

    return keyVal;
}