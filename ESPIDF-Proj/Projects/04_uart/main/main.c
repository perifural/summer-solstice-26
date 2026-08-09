#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "led.h"
#include "uart.h"

void app_main(void)
{
    uint8_t len = 0;
    uint16_t times = 0;
    unsigned char data[RX_BUF_SIZE] = {0};

    led_init();
    usart_init(115200);
    vTaskDelay(500);

    while(1)
    {
        uart_get_buffered_data_len(USART_UX, (size_t*) &len);

        if (len > 0)
        {
            memset(data, 0, RX_BUF_SIZE);
            uart_read_bytes(USART_UX, data, len, 100);
            printf("UART: \n");
            uart_write_bytes(USART_UX, (const char*)data, strlen((const char*)data));
            // printf("\n");
        }

        times++;

        if (times % 500 == 0)
        {
            printf("%d\n", times);
        }

        if (times % 20 == 0)
        {
            led_toggle();
        }

        vTaskDelay(10);
    }
}
