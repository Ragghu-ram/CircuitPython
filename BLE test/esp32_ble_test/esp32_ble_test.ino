/*
https://dl.espressif.com/dl/package_esp32_index.json
https://downloads.arduino.cc/packages/package_index.json
https://github.com/arduino/ArduinoCore-arduino-nano33ble/releases/download/1.0.0/package_nano33ble_index.json
*/
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEClient.h>
#include <BLERemoteCharacteristic.h>

BLEScan* pBLEScan;
BLEClient* pClient;
BLERemoteCharacteristic* pRemoteCharacteristic;

static BLEUUID serviceUUID("180D"); // Service UUID from Nano 33 BLE
static BLEUUID charUUID("2A37");    // Characteristic UUID from Nano 33 BLE

void setup() {
  Serial.begin(9600);

  // Initialize BLE device
  BLEDevice::init("ESP32_Client");

  // Create a BLE scan
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setActiveScan(true); // Active scan uses more power, but gets results faster
  Serial.println("Scanning for BLE devices...");
}

void loop() {
  // Scan for BLE devices for 5 seconds
  BLEScanResults* pScanResults = pBLEScan->start(5);  // Use pointer to BLEScanResults

  // Print detected devices
  for (int i = 0; i < pScanResults->getCount(); i++) {
    BLEAdvertisedDevice advertisedDevice = pScanResults->getDevice(i);
    if (advertisedDevice.haveName()) {
      Serial.print("Found device: ");
      Serial.println(advertisedDevice.getName().c_str());
    } 
    else {
      Serial.println("Found unnamed device");
    }

    // Check if it matches the Nano 33 BLE
    if (advertisedDevice.haveServiceUUID() && advertisedDevice.isAdvertisingService(serviceUUID)) {
      Serial.println("Nano 33 BLE found. Connecting...");

      // Connect to the server
      pClient = BLEDevice::createClient();
      pClient->connect(&advertisedDevice);

      // Get the service and characteristic
      BLERemoteService* pRemoteService = pClient->getService(serviceUUID);
      if (pRemoteService == nullptr) {
        Serial.println("Failed to find service.");
        return;
      }

      pRemoteCharacteristic = pRemoteService->getCharacteristic(charUUID);
      if (pRemoteCharacteristic == nullptr) {
        Serial.println("Failed to find characteristic.");
        return;
      }

      // Read the data from the characteristic
      if (pRemoteCharacteristic->canRead()) {
        String value = pRemoteCharacteristic->readValue();  // Use String instead of std::string
        Serial.print("Received value: ");
        Serial.println(value);  // Directly print the String value
      }

      // If the characteristic supports notifications, register for them
      if (pRemoteCharacteristic->canNotify()) {
        pRemoteCharacteristic->registerForNotify(notifyCallback);
      }
    }
  }
  
  // Delay before the next scan
  delay(5000);
}

// Callback function for notifications
void notifyCallback(BLERemoteCharacteristic* pBLERemoteCharacteristic, uint8_t* pData, size_t length, bool isNotify) {
  Serial.print("Notification received: ");
  int receivedValue = 0;

  // Assuming the notification contains a 4-byte integer
  for (int i = 0; i < length; i++) {
    receivedValue |= (pData[i] << (8 * i));  // Combine bytes into an integer
  }

  Serial.println(receivedValue);  // Print the received integer value
}

