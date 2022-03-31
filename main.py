from deepface import DeepFace
import face_recognition
from PIL import Image, ImageDraw
import os, sys
import time
import shutil

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
    images = []

    for file in os.listdir(r"\\192.168.100.144\surveillance\@Snapshot"):
        if os.path.isfile(os.path.join(r"\\192.168.100.144\surveillance\@Snapshot", file)):
            images.append(file)
    first_face = True
    first_img = []
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
                    first_img = face_enc[0]
                    first_face = False
                    shutil.move(rf"\\192.168.100.144\surveillance\@Snapshot\{image}",
                                rf"C:\Users\Anton\Pictures\Человек\{image}")
                else:
                    count = 0
                    for face_location in face_locations:
                        top, right, bottom, left = face_location
                        face = face_img[top:bottom, left:right]
                        pil_img = Image.fromarray(face)

                        res_compare = face_recognition.compare_faces([first_img], face_enc[count])
                        if res_compare[0]:
                            print("Одинаковые")
                            shutil.move(rf"\\192.168.100.144\surveillance\@Snapshot\{image}",
                                        rf"C:\Users\Anton\Pictures\People\{image}")
                            pil_img.save(rf"C:\Users\Anton\Pictures\People\{count}_{image}")
                        else:
                            print("Неодинаковые")
                        count += 1
        except Exception as _ex:
            os.remove(rf"\\192.168.100.144\surveillance\@Snapshot\{image}")
            print(_ex)


def main():
    extracting_faces()


if __name__ == '__main__':
    main()
