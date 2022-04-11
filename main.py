import os
import shutil
import sys
import cv2
import time

import face_recognition
from PIL import Image, ImageDraw

FIRST_FACE_ENC = ''


def face_rec():
    img_face1 = r"\\192.168.100.144\surveillance\@Snapshot\BN-PROFI-20220328-1104134529.jpg"
    img_face2 = r"\\192.168.100.144\surveillance\@Snapshot\BN-PROFI-20220328-0943354599.jpg"

    face1 = face_recognition.load_image_file(img_face1)
    face_location_img1 = face_recognition.face_locations(face1)
    print(f"Найдено {len(face_location_img1)} лиц(о) на изображении")
    print(face_location_img1)

    face2 = face_recognition.load_image_file(img_face2)
    face_location_img2 = face_recognition.face_locations(face2)
    print(f"Найдено {len(face_location_img2)} лиц(о) на изображении")
    print(face_location_img2)

    pil_img1 = Image.fromarray(face1)
    draw1 = ImageDraw.Draw(pil_img1)

    for (top, right, bottom, left) in face_location_img1:
        draw1.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=2)

    del draw1
    pil_img1.save(r"C:\Users\Anton\Pictures\new_face.jpg")

    pil_img2 = Image.fromarray(face2)
    draw2 = ImageDraw.Draw(pil_img2)

    for (top, right, bottom, left) in face_location_img2:
        draw2.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=2)

    del draw2
    pil_img2.save(r"C:\Users\Anton\Pictures\new_face2.jpg")


def extracting_faces():
    if not os.path.exists(r"\\192.168.100.144\surveillance\@Snapshot"):
        print("Директория недоступна!")
        sys.exit()

    known_encodings = []
    known_faces = []
    images = []

    for file in os.listdir(r"\\192.168.100.144\surveillance\@Snapshot"):
        if os.path.isfile(os.path.join(r"\\192.168.100.144\surveillance\@Snapshot", file)):
            images.append(file)
    first_face = True
    for (i, image) in enumerate(images):
        print(f"Обработка изображений {i + 1}/{len(images)}")
        try:
            face_img = face_recognition.load_image_file(rf"\\192.168.100.144\surveillance\@Snapshot\{image}")
            face_enc = face_recognition.face_encodings(face_img)
            face_locations = face_recognition.face_locations(face_img)
            if len(face_enc) == 0:
                print("Пусто")
                os.remove(rf"\\192.168.100.144\surveillance\@Snapshot\{image}")
            else:
                if first_face:
                    known_faces.append(face_enc[0])
                    first_face = False
                    if not os.path.exists(rf"C:\Users\Anton\Pictures\AUTO\People0"):
                        os.mkdir(rf"C:\Users\Anton\Pictures\AUTO\People0")
                    shutil.move(rf"\\192.168.100.144\surveillance\@Snapshot\{image}",
                                rf"C:\Users\Anton\Pictures\AUTO\People0\{image}")
                else:
                    count = 0
                    for face_location in face_locations:
                        top, right, bottom, left = face_location
                        face = face_img[top:bottom, left:right]
                        pil_img = Image.fromarray(face)
                        found_face = False
                        for (j, known_face) in enumerate(known_faces):
                            print(f"Сравниваю лицо {j+1} из известых {len(known_faces)}")
                            res_compare = face_recognition.compare_faces([known_face], face_enc[count])
                            if res_compare[0]:
                                found_face = True
                                print("Одинаковые")
                                if os.path.exists(rf"\\192.168.100.144\surveillance\@Snapshot\{image}"):
                                    if not os.path.exists(rf"C:\Users\Anton\Pictures\AUTO\People{j}"):
                                        os.mkdir(rf"C:\Users\Anton\Pictures\AUTO\People{j}")

                                    shutil.move(rf"\\192.168.100.144\surveillance\@Snapshot\{image}",
                                                rf"C:\Users\Anton\Pictures\AUTO\People{j}\{image}")
                                    pil_img.save(rf"C:\Users\Anton\Pictures\AUTO\People{j}\{count}_{image}")
                                    break
                                else:
                                    os.remove(rf"\\192.168.100.144\surveillance\@Snapshot\{image}")
                            else:
                                pass
                        if not found_face:
                            print("Найдено неизвесное лицо")
                            if os.path.exists(rf"\\192.168.100.144\surveillance\@Snapshot\{image}"):
                                known_faces.append(face_enc[0])
                                os.mkdir(rf"C:\Users\Anton\Pictures\AUTO\People{len(known_faces)-1}")
                                shutil.move(rf"\\192.168.100.144\surveillance\@Snapshot\{image}",
                                            rf"C:\Users\Anton\Pictures\AUTO\People{len(known_faces)-1}\{image}")
                                pil_img.save(rf"C:\Users\Anton\Pictures\AUTO\People{len(known_faces)-1}\{count}_{image}")
                            else:
                                os.remove(rf"\\192.168.100.144\surveillance\@Snapshot\{image}")
                        count += 1
        except Exception as _ex:
            #os.remove(rf"\\192.168.100.144\surveillance\@Snapshot\{image}")
            print(_ex)


def video_capture():
    capture = cv2.VideoCapture('rtsp://syno:2553b1b0c98800e1052a8a74db9e2f36@192.168.100.10:554/Sms=10.unicast')
    frame_rate = 25
    prev = 0
    while True:
        try:
            time_elapsed = time.time() - prev
            ret, frame = capture.read()

            if time_elapsed > 1. / frame_rate:
                prev = time.time()

                print("Начаниаем поиск лиц")
                locations = face_recognition.face_locations(frame)
                for face_location in locations:
                    left_top = (face_location[3], face_location[0])
                    right_bottom = (face_location[1], face_location[2])
                    color = [0, 255, 0]
                    cv2.rectangle(frame, left_top, right_bottom, color)
                cv2.imshow("Capturing", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as _ex:
            print(_ex)

    capture.release()
    cv2.destroyAllWindows()


def main():
    #video_capture()
    extracting_faces()


if __name__ == '__main__':
    main()
