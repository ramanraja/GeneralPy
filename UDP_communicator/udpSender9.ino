// Split large packets int 512 byte chunks and send them one by one
// in response to prompts of 'N'. Aborts  if the prompt is 'A'.
//use the test tool: https://packetsender.com/documentation
// Or the python program udpReceiver.py

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "xxxx";
const char* password = "yyyy";

#define IN_BUFFER_SIZE   12     // mostly single byte commands 
#define OUT_BUFFER_SIZE  512    // theoretical max; don't alter this ! 
#define NUM_CHUNKS       12     // must be a single hex digit (<16)
#define  NEXT_PROMPT     'N'
#define  ABORT_PROMPT    'A'
char request_packet[IN_BUFFER_SIZE];  // buffer for incoming packets
char  response_packet[OUT_BUFFER_SIZE];  
unsigned int local_udp_port = 12345;  // incoming local port to listen on

IPAddress ip(192,168,0,109);
IPAddress gateway(192,168,0,1);
IPAddress subnet(255,255,255,0);
IPAddress remote_IP = IPAddress(192,168,0,105);
unsigned int remote_udp_port = 54321;
WiFiUDP Udp;

void setup() {
  init_serial();
  init_wifi();
  init_udp();
}

int next_chunk = 0;
int ic_pkt_length;

void loop() {
    //request_packet[0] = '*';  // just for safety ?!
    int packetSize = Udp.parsePacket();
    if (!packetSize)
        return; 
    ic_pkt_length = Udp.read(request_packet, IN_BUFFER_SIZE);
    if (ic_pkt_length == 0)
        return;
    if (request_packet[0] == ABORT_PROMPT) {
        Serial.println("- Aborting chunks -");
        next_chunk = 0;
        return;      
    }
    if (request_packet[0] == NEXT_PROMPT) {
        make_response(next_chunk);
        send_response();
        next_chunk = (next_chunk+1) % NUM_CHUNKS;
    }
    //delay(100);
}

void send_response() {
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    //Udp.beginPacket(remote_IP, remote_udp_port);
    Udp.write(response_packet, strlen(response_packet));
    Udp.endPacket();
}

char tmp[12];     
float data = 10.25;  // always 2 digits + 2 decimals

void make_response (int chunk) {
    response_packet[0] = '[';   // start a new packet
    response_packet[1] = chunk < 10 ? (chunk+'0') : (chunk-10+'A') ;    // a single hex digit
    response_packet[2] = '|';   // separator
    response_packet[3] = '\0'; 
    for (int i=0; i<64; i++) {   
        data = data+0.5;
        if (data >= 100) data = 10.25;
        // dtostrf(FLOAT, WIDTH, PRECSISION, BUFFER)
        dtostrf(data,4,2,tmp); 
        strcat(response_packet, tmp);
        strcat(response_packet, " ");
    }
    strcat(response_packet, "]");    
    Serial.println(response_packet);
    Serial.println(strlen(response_packet));
}

void init_wifi() {  
    Serial.printf("Connecting to %s ", ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)  {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nConnected.");
    WiFi.config(ip,gateway,subnet);
    Serial.println("Configured.");
}

void init_udp() {  
    Udp.begin(local_udp_port);
    Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), local_udp_port);
}

void init_serial() {  
  Serial.begin(115200);
  Serial.println();
  Serial.println("\n\nUDP_TX_PACKET_MAX_SIZE: ");
  Serial.println(UDP_TX_PACKET_MAX_SIZE);  
}  
