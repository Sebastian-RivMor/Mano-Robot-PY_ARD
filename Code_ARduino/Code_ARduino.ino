// int ledPins[] = {2, 3, 4, 5, 8};

// void setup() {
//     Serial.begin(9600);
//     for (int i = 0; i < 5; i++) {
//         pinMode(ledPins[i], OUTPUT);
//     }
// }

// void loop() {
//     if (Serial.available() >= 5) {
//         byte ledState[5];
//         for (int i = 0; i < 5; i++) {
//             ledState[i] = Serial.read();
//         }

//         for (int i = 0; i < 5; i++) {
//             if (ledState[i] == 1) {
//                 digitalWrite(ledPins[i], HIGH);
//             } else {
//                 digitalWrite(ledPins[i], LOW);
//             }
//         }
//     }
// }

#include <Servo.h>

Servo servos[5];  // Arreglo de 5 servos para los dedos

int servoPins[] = {2, 3, 4, 5, 8};  // Pines conectados a los servos

void setup() {
    Serial.begin(9600);
    for (int i = 0; i < 5; i++) {
        servos[i].attach(servoPins[i]);
        servos[i].write(0);  // Posición inicial (0 grados, todos los dedos abiertos)
    }
}

void loop() {
    if (Serial.available() >= 5) {
        byte servoState[5];
        for (int i = 0; i < 5; i++) {
            servoState[i] = Serial.read();
        }

        for (int i = 0; i < 5; i++) {
            if (servoState[i] == 1) {
                servos[i].write(180);  // Dedo doblado
            } else {
                servos[i].write(0);  // Dedo extendido
            }
        }
    }
}
