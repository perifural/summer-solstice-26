#include "esptim.h"

void esptim_int_init(uint64_t tps)
{
    esp_timer_handle_t esp_tim_handle;

    esp_timer_create_args_t tim_periodic_arg = {
        .callback = esptim_callback,
        .arg = NULL,
    };

    esp_timer_create(&tim_periodic_arg, &esp_tim_handle);
    esp_timer_start_periodic(esp_tim_handle, tps);
}

void esptim_callback(void* arg)
{
    led_toggle();
}