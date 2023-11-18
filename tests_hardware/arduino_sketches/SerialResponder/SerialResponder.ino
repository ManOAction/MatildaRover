void setup()
{
    Serial.begin(9600);
}

void loop()
{
    if (Serial.available() > 0)
    {
        // read the incoming byte:
        char incomingByte = Serial.read();
        // send the byte back:
        Serial.write(incomingByte);
        Serial.write('\n');
    }
}