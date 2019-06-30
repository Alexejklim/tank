#include <ArduinoJson.h>

#define VT_PIN A6
#define AT_PIN A7

void setup() {
  Serial.begin(115200);
  analogReference(DEFAULT);
}
void loop() {

  if (Serial.available() > 0) {
    DynamicJsonDocument reply(1024);

    if (Serial.readStringUntil("\n") == "/battery?act=status&\n")
    {
      float vt_temp = analogRead(VT_PIN);
      float at_temp = analogRead(AT_PIN);
      double voltage = vt_temp * (5 / 1023.0) * (16.5 / 3.55);
      double current = at_temp * (5 / 1023.0);
      reply["Voltage"] = voltage;
      reply["Current"] = current;
      reply["status"] = "OK";
      serializeJson(reply, Serial);
    }
  }
}
