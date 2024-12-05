# import cv2
# import mediapipe as mp

# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands()

# # Iniciar la captura de video (puede ser desde la cámara)
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convertir la imagen a RGB
#     image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Procesar la imagen y detectar manos
#     results = hands.process(image_rgb)

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#     # Mostrar la imagen con las manos detectadas
#     cv2.imshow('Hand Detection', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Liberar los recursos
# cap.release()
# cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import serial



# Inicializar la comunicación serial con Arduino (ajusta el puerto y velocidad si es necesario)
arduino = serial.Serial('COM6', 9600)  # Cambia 'COM3' por tu puerto correspondiente

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Iniciar la captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # Inicializar el estado de los dedos
    dedos = [0, 0, 0, 0, 0]  # Meñique, anular, medio, índice, pulgar

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Aquí puedes usar las coordenadas de los landmarks para determinar si un dedo está doblado o no.
            # Por ejemplo, puedes comparar la posición de las articulaciones para cada dedo.
            
            # Por ejemplo, detección simple (podrías mejorarlo):
            if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y:
                dedos[4] = 1  # Pulgar doblado
            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y:
                dedos[3] = 1  # Índice doblado
            if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y:
                dedos[2] = 1  # Medio doblado
            if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y:
                dedos[1] = 1  # Anular doblado
            if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y:
                dedos[0] = 1  # Meñique doblado

            # Enviar el estado de los dedos a Arduino
            arduino.write(bytearray(dedos))

    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()
arduino.close()

