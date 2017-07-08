#include <ESP8266WiFi.h>
#include <string.h>
#ifdef ESP8266
extern "C" {
#include "user_interface.h"
}
#endif
#include "config.h"
#include "aes256.h"
aes256_context ctxt;
#include <EEPROM.h>
int addr = 12;
int id = 1001;
#define PACKET_LEN 128
char spaces[] = {' ', '\r', '\n', '\t'};
byte channel;

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
uint8_t mac[6] = { 0x00, mac_addr1, mac_addr2, mac_addr3, mac_addr4, mac_addr5 };


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
  EEPROM.write(addr, 232);
  
  EEPROM.begin(512);
  EEPROM.write(addr, 0);
  EEPROM.write(addr+1, 0);
  byte value = EEPROM.read(addr);

  
  wifi_set_opmode(STATION_MODE);
  wifi_promiscuous_enable(1);
  wifi_set_channel(6); 
  char text[] = "233";
//  EEPROM.write(addr, 1);
  
  
}

void loop() {
   uint8_t key[] = { //
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f
  };
    aes256_init(&ctxt, key);
//  uint8_t data[] = { //"asdfasdfasdfasdf"
//    0x61, 0x73, 0x64, 0x66, 0x61, 0x73, 0x64, 0x66,
//    0x61, 0x73, 0x64, 0x66, 0x61, 0x73, 0x64, 0x66
//  };
  uint8_t data[] = {
    EEPROM.read(addr), EEPROM.read(addr+1), 0x01, 0x00, 0x00, 0x01, random(255)
  };
  Serial.print(EEPROM.read(addr));
  Serial.print(EEPROM.read(addr+1));  
//  data[0] = EEPROM.read(addr);
//  data[1] = EEPROM.read(addr+1);
//  data[2] = '1';
//  data[3] = '0';
//  data[4] = '0';
//  data[5] = '1';
//  data[6] = random(255)+1;
  uint8_t ssid[8];
  aes256_encrypt_ecb(&ctxt, data);
  for(int i=0; i<sizeof(data); ++i) {
    if(data[i]<0x10) {
      Serial.print('0'); 
    }
    Serial.print(char(data[i]), HEX);
    } 
   Serial.println();
   Serial.println(buf);
  memcpy(ssid, data,sizeof(data));
//  aes256_decrypt_ecb(&ctxt, data);
  aes256_done(&ctxt);
  
  // if (random(2)) {
  //   memcpy(ssid + 1, "", 5);
  //
  // } else {
  //   byte seq = random(strlen(emoji)) / 4;
  //   memcpy(ssid, emoji + seq * 4, 4);
  //   memcpy(ssid + 4, "-HDU", 5);
  //   slen = 8;
  // }
  //Serial.print((char*)ssid);

  constructBeaconPacket(mac, sizeof(ssid), ssid, channel);
  
  wifi_send_pkt_freedom(packet, 51 + sizeof(ssid), 0);
  wifi_send_pkt_freedom(packet, 51 + sizeof(ssid), 0);
  wifi_send_pkt_freedom(packet, 51 + sizeof(ssid), 0);
  //Serial.println(" Packets sent");
  delayMicroseconds(100000);
}
