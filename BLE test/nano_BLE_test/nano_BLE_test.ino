/*
https://dl.espressif.com/dl/package_esp32_index.json
https://downloads.arduino.cc/packages/package_index.json
https://github.com/arduino/ArduinoCore-arduino-nano33ble/releases/download/1.0.0/package_nano33ble_index.json
*/

#include <ArduinoBLE.h>

// Define the BLE service and characteristic
BLEService dataService("180D"); // Custom service UUID
BLECharacteristic dataCharacteristic("2A37", BLERead | BLENotify, sizeof(int)); // Custom characteristic UUID

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial monitor to open
  
  if (!BLE.begin()) {
    Serial.println("BLE initialization failed!");
    while (1);
  }

  BLE.setLocalName("Nano33BLE");
  BLE.setAdvertisedService(dataService);
  dataService.addCharacteristic(dataCharacteristic);
  BLE.addService(dataService);
  BLE.advertise();

  Serial.println("BLE device is advertising");
}

void loop() {
  BLEDevice central = BLE.central();

  // Check if a central device is connected
  if (central) {
    Serial.print("Connected to ");
    Serial.println(central.address());

    // Collect and send data (for example, a random number)
    int dataToSend = random(0, 100); // Replace with your data collection logic

    // Convert integer to a byte array
    dataCharacteristic.setValue((uint8_t*)&dataToSend, sizeof(dataToSend)); // Send data as bytes

    // Print sent data for debugging
    Serial.print("Sent data: ");
    Serial.println(dataToSend);
    
    // Optional: delay for a moment to simulate data processing
    delay(1000); // Adjust delay as needed
  }
}
