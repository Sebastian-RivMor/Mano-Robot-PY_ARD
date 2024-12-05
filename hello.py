import serial
import time
from cvzone.HandTrackingModule import HandDetector
import cv2

# Configuración del puerto serial
comport = 'COM4'  # Ajusta según tu configuración
arduino = serial.Serial(comport, 9600, timeout=1)
time.sleep(2)  # Espera para que la conexión se estabilice

# Configuración de la cámara y detector de manos
detector = HandDetector(detectionCon=0.8, maxHands=1)
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)
    hands, img = detector.findHands(frame)
    
    # Inicializa el estado de los LEDs (todos apagados)
    led_state = [0, 0, 0, 0, 0]

    if hands:
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)
        
        # Asigna el estado de cada LED según los dedos levantados
        for i in range(5):
            led_state[i] = 1 if fingerUp[i] else 0

    # Envía el estado de los LEDs a Arduino
    arduino.write(bytes(led_state))

    # Muestra la cantidad de dedos levantados en la pantalla
    finger_count = fingerUp.count(1)
    cv2.putText(frame, f'Finger count: {finger_count}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.imshow("frame", frame)
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
