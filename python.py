import cvzone
import cv2  # versï¿½o 1.4.1
import serial
from cvzone.HandTrackingModule import HandDetector

# Configuraï¿½ï¿½o da cï¿½mera e comunicaï¿½ï¿½o serial
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=int(0.7))
mySerial = serial.Serial("COM6", 9600, timeout=1)

while True:
    success, img = cap.read()
    if not success:
        print("Erro ao acessar a cï¿½mera.")
        break

    # Detecta a mï¿½o e encontra os pontos
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if lmList:
        # Identifica quais dedos estï¿½o levantados
        fingers = detector.fingersUp()

        # Converte a lista de dedos para uma string separada por vï¿½rgulas e envia via serial
        data = ",".join(map(str, fingers)) + "\n"  # Ex: "1,0,1,0,1\n"
        mySerial.write(data.encode())  # Envia como bytes
        print("Dados enviados:", data.strip())  # Exibe os dados enviados no terminal para depuraï¿½ï¿½o

    # Exibe a imagem da cï¿½mera com a detecï¿½ï¿½o
    cv2.imshow("Image", img)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a cï¿½mera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
mySerial.close()

     
    #.\novo_venv\Scripts\activate
    # python .\codigo_mao_inicial.py

#import cvzone  # versão - 0.10.18
#import cv2     # versão - 1.4.1
#from cvzone.HandTrackingModule import HandDetector
#import math
#
## Configurar a câmera
#cap = cv2.VideoCapture(0)
#
## Detector de mãos, detecção com confiança 0.7
#detector = HandDetector(maxHands=1, detectionCon=int(0.7))
#
## Função para calcular a porcentagem de extensão do dedo (padrão)
#def calculate_extension(finger_tip, finger_base, palm_base):
#    distance_tip_base = math.sqrt((finger_tip[0] - finger_base[0])**2 + (finger_tip[1] - finger_base[1])**2)
#    distance_max = math.sqrt((finger_base[0] - palm_base[0])**2 + (finger_base[1] - palm_base[1])**2)
#    extension_percentage = min(max((distance_tip_base / distance_max) * 100, 0), 100)
#    return extension_percentage
#
## Função específica para o polegar com inversão e normalização
#def calculate_thumb_extension(finger_tip, finger_base, pinky_base):
#    distance_tip_base = math.sqrt((finger_tip[0] - finger_base[0])**2 + (finger_tip[1] - finger_base[1])**2)
#    distance_max = math.sqrt((finger_base[0] - pinky_base[0])**2 + (finger_base[1] - pinky_base[1])**2)
#    extension_percentage = min(max(100 - (distance_tip_base / distance_max) * 100, 0), 100)
#    thumb_min = 15
#    thumb_max = 56
#    normalized_thumb = (extension_percentage - thumb_min) / (thumb_max - thumb_min) * 100
#    normalized_thumb = min(max(normalized_thumb, 0), 100)
#    return normalized_thumb
#
## Função para calcular o ângulo de rotação do pulso usando as coordenadas X do indicador e mindinho
#def calculate_wrist_rotation(palm_base, index_base, pinky_base):
#    # Usar as coordenadas X da base do indicador e mindinho em relação à palma da mão
#    delta_x_index = index_base[0] - palm_base[0]
#    delta_x_pinky = pinky_base[0] - palm_base[0]
#
#    # A rotação será baseada na diferença entre os vetores X dos dedos
#    rotation = delta_x_index - delta_x_pinky
#
#    # Normalizar para um intervalo de 0 a 360
#    rotation_normalized = (rotation + 180) % 360  # Garantir que o valor fique entre 0 e 360
#
#    return rotation
#
#while True:
#    success, img = cap.read()  # Captura a imagem da câmera
#    img = detector.findHands(img)  # Detecta as mãos
#    lmList, bbox = detector.findPosition(img)  # Posição das landmarks
#
#    if lmList:
#        palm_base = lmList[0]  # Base da palma da mão (landmark 0)
#        
#        # Polegar: ponta (4), base (2), usa base do mindinho (landmark 17)
#        thumb = calculate_thumb_extension(lmList[4], lmList[2], lmList[17])
#
#        # Indicador: ponta (8), base (5)
#        index_finger = calculate_extension(lmList[8], lmList[5], palm_base)
#
#        # Médio: ponta (12), base (9)
#        middle_finger = calculate_extension(lmList[12], lmList[9], palm_base)
#
#        # Anelar: ponta (16), base (13)
#        ring_finger = calculate_extension(lmList[16], lmList[13], palm_base)
#
#        # Mindinho: ponta (20), base (17)
#        pinky_finger = calculate_extension(lmList[20], lmList[17], palm_base)
#
#        # Calcular a rotação do pulso usando a base da mão, dedo indicador e mindinho
#        wrist_rotation = calculate_wrist_rotation(palm_base, lmList[5], lmList[17])
#
#        # Exibir as porcentagens de extensão de cada dedo e rotação do pulso
#        finger_extensions = [thumb, index_finger, middle_finger, ring_finger, pinky_finger, wrist_rotation]
#        print([round(ext, 1) for ext in finger_extensions])
#
#    # Mostrar a imagem com detecção de mãos
#    cv2.imshow("Image", img)
#
#    # Pressione 'q' para sair
#    if cv2.waitKey(1) & 0xff == ord('q'):
#        break
#
#cap.release()
#cv2.destroyAllWindows()