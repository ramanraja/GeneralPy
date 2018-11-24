#include "common.h" 
#include "config.h"
#include "myfi.h"
#include "MqttLite.h"
#include "otaHelper.h"
#include <Button.h>  // https://github.com/JChristensen/Button
#include <Timer.h>   // https://github.com/JChristensen/Timer

#define LONG_DURATION  2000
int led = 2;
int button = 0;

Timer T;
Config C;
MqttLite M;
//OtaHelper O;
// Button (pin, enable_pullup, invert_logic, debounce_mSec) 
Button B(button, false, true, 20);

void setup(){
    init_serial();
    init_hardware();
    C.init();
    C.dump();   
    M.init (&C);
    //O.init (&C, &M);
    //T.after(3600000L, check_for_updates);  // TODO: enable this ?
    T.oscillate(led, 500, HIGH, 2);  // ready to read the command button
}

void loop(){
    T.update(); 
    M.update();    
    check_button();  
}

void check_button() {
  int button_status = read_button();
    switch (button_status) {
        case 0:
            break;
        case 1:
            SERIAL_PRINTLN ("button pressed.");
            M.publish("TOGGLE RemCam");
            break;
        case 2:
            SERIAL_PRINTLN ("button long pressed !");
            M.publish("EXIT");
            break;
    }
}

bool in_long_press_state = false;
int read_button() {
    B.read();
    if (B.wasReleased()) {
        if (in_long_press_state)
            in_long_press_state = false;
        else
            return 1;
    }
    else if (B.pressedFor(LONG_DURATION) && !in_long_press_state) {
        in_long_press_state = true;
        return 2;
    }
    return 0;
}

void  app_callback(const char* command_string) {
    SERIAL_PRINTLN ("app_callback: MQTT message received :");
    SERIAL_PRINTLN (command_string);
    if (command_string[0]=='O' && command_string[1]=='N') {
        SERIAL_PRINTLN ("Remote cam is ON");
        T.oscillate(led,50,HIGH,8);
    }
    else
    if (command_string[0]=='O' && command_string[1]=='F' && 
        command_string[2]=='F') {
        SERIAL_PRINTLN ("Remote cam is OFF");
        T.oscillate(led,200,HIGH,4);
    }    
    else
    if (command_string[0]=='E' && command_string[1]=='X' && 
        command_string[2]=='I' && command_string[3]=='T') {
        SERIAL_PRINTLN ("Remote cam app has terminated !");
        if (C.sleep_deep) {
            M.publish("RemCam Button goes to sleep..");
            digitalWrite (led, LOW);
            delay(2000);
            digitalWrite (led, HIGH);
            ESP.deepSleep(0);
        }
        else
            T.pulse(led,2000,HIGH);
    }     
}

void init_hardware() {
    pinMode(led, OUTPUT);  
    pinMode(button, INPUT);
    blinker();
}

/*
void check_for_updates() {
    SERIAL_PRINTLN ("\n<<<<<<---------  checking for FW updates... ----------->>>>>>\n");
    int result = O.check_and_update();  // if there was an update, this will restart 8266
    SERIAL_PRINT ("OtaHelper: response code: ");   // if the update failed
    SERIAL_PRINTLN (result);
    T.oscillate(led, 500, HIGH, 2);  // ready to read the command button
}
*/

void init_serial () {
    #ifdef ENABLE_DEBUG
        //Serial.begin(C.baud_rate);  // there is no C !
        Serial.begin(BAUD_RATE); 
        #ifdef VERBOSE_MODE
          Serial.setDebugOutput(true);
        #endif
        Serial.setTimeout(250);
    #endif    
    SERIAL_PRINTLN("\n\n********************* IoT Button starting... ********************\n"); 
}

void blinker() {
    for (int i=0; i<6; i++) {
        digitalWrite(led, LOW);
        delay(100);
        digitalWrite(led, HIGH);
        delay(100);        
    }
}

