#include <ESP8266WiFi.h>
#include <string.h>
#ifdef ESP8266
extern "C" {
#include "user_interface.h"
}
#endif
#include "config.h"
#include <EEPROM.h>
#include <math.h>
int addr = 12;
int id = 1001;
#define PACKET_LEN 128
#include <PN532_HSU.h>
#include <PN532.h>

PN532_HSU pn532hsu(Serial1);
PN532 nfc(pn532hsu);

//
//const unsigned char wake[24]={
//  0x55, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
//0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x03, 0xfd, 0xd4, 0x14, 0x01, 0x17, 0x00};//wake up NFC module
//const unsigned char firmware[9]={
//  0x00, 0x00, 0xFF, 0x02, 0xFE, 0xD4, 0x02, 0x2A, 0x00};//
//const unsigned char tag[11]={
//  0x00, 0x00, 0xFF, 0x04, 0xFC, 0xD4, 0x4A, 0x01, 0x00, 0xE1, 0x00};//detecting tag command
//const unsigned char std_ACK[25] = {
//  0x00, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0x00, 0x00, 0xFF, 0x0C, \
//0xF4, 0xD5, 0x4B, 0x01, 0x01, 0x00, 0x04, 0x08, 0x04, 0x00, 0x00, 0x00, 0x00, 0x4b, 0x00};
//unsigned char old_id[5];

//unsigned char receive_ACK[25];//Command receiving buffer
////int inByte = 0;               //incoming serial byte buffer
//
//#if defined(ARDUINO) && ARDUINO >= 100
//#include "Arduino.h"
//#define print1Byte(args) Serial1.write(args)
//#define print1lnByte(args)  Serial1.write(args),Serial1.println()
//#else
//#include "WProgram.h"
//#define print1Byte(args) Serial1.print(args,BYTE)
//#define print1lnByte(args)  Serial1.println(args,BYTE)
//#endif

char spaces[] = {' ', '\r', '\n', '\t'};
byte channel;
uint8_t mac[6] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06 };

uint8_t packet[PACKET_LEN] = { 0x80, 0x00, 0x00, 0x00,
                               /*4*/   0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                               /*10*/  0x01, 0x02, 0x03, 0x04, 0x05, 0x06,
                               /*16*/  0x01, 0x02, 0x03, 0x04, 0x05, 0x06,
                               /*22*/  0xc0, 0x6c,
                               /*24*/  0x83, 0x51, 0xf7, 0x8f, 0x0f, 0x00, 0x00, 0x00,
                               /*32*/  0x64, 0x00,
                               /*34*/  0x11, 0x05,
                               /* SSID */
                               /*36*/  0x00, 0x06, 0x72, 0x72, 0x72, 0x72, 0x72, 0x72,
                               0x01, 0x08, 0x82, 0x84,
                               0x8b, 0x96, 0x24, 0x30, 0x48, 0x6c, 0x03, 0x01,
                               /*56*/  0x04
                             };
uint8_t len;

inline void constructBeaconPacket(uint8_t mac[6], uint8_t ssid_len, uint8_t *ssid, uint8_t channel) {
  uint8_t packet_end[13] = {
    0x01, 0x08, 0x82, 0x84, 0x8b, 0x96, 0x24, 0x30,
    0x48, 0x6c, 0x03, 0x01, 0x04
  };

  // Write sender MAC
  memcpy(packet + 10, mac, 6);
  memcpy(packet + 16, mac, 6);
  // Write SSID
  if (ssid_len > 75) ssid_len = 75;
  packet[37] = ssid_len;
  uint8_t slen = strlen((char*)ssid);
  if (slen > ssid_len) slen = ssid_len;
  //uint8_t slen = ssid_len;
  memcpy(packet + 38, ssid, slen);
  for (uint8_t i = 38 + slen + 1; i <= 38 + ssid_len; i++) packet[i] = spaces[random(3)];
  // Write channel
  packet_end[12] = channel;

  memcpy(packet + 38 + ssid_len, packet_end, 13);
}

void setup() {
  Serial.begin(115200);
  WiFi.printDiag(Serial);
  delay(500);
  delayMicroseconds(100000);
  channel = 6;
  EEPROM.begin(512);
  EEPROM.write(addr, 32);
  byte value = EEPROM.read(addr);

  
  wifi_set_opmode(3);
  wifi_promiscuous_enable(1);
  wifi_set_channel(channel); 
  char text[] = "233";
//  EEPROM.write(addr, 1);
  WiFi.begin("Hackathon", ""); 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
}
void loop() {
//  wake_card();
  uint8_t ssid[14] = {0};
  byte slen=13;
    
  int stat = EEPROM.read(addr);
  int hash = 1001;
  int result = 0;
  while(hash>0){
    result = result*31+hash%10;
    hash = hash/10;
  }
  result = result%10000;
  int code = hash*10000+result%10;
  char words[4];
  Serial.println(code);
  int a = result;
  for(int i = 0;i<4;i++){
    words[3-i]='0'+(a%10);
    a = a/10;
  }
  memcpy(ssid, "B1001", 5);
  //sprintf(words, "%d", code);
  Serial.println("copy ID");
  memcpy(ssid+5, words, 4); 
  Serial.println("copy hash");
  Serial.println((char*)ssid);
  mac[0] = 0x00;
  mac[1] = 0x1a;
  mac[2] = 0x2e;
  mac[3] = 0x6e;
  mac[4] = 0x2a;
  mac[5] = 0x1a;
  constructBeaconPacket(mac, slen, ssid, channel);
  
  wifi_send_pkt_freedom(packet, 51 + sizeof(ssid), 0);
  wifi_send_pkt_freedom(packet, 51 + sizeof(ssid), 0);
  wifi_send_pkt_freedom(packet, 51 + sizeof(ssid), 0);
  Serial.println(" Packets sent");
  delayMicroseconds(1000);
}
