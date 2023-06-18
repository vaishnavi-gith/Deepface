from deepface import DeepFace
import cv2
import os
from PIL import Image

cap = cv2.VideoCapture(0)
count = 0

while True:

  ret, test_img = cap.read()
  cv2.resize(test_img,(1000,700))
  if not ret:
    continue
  path = "frame%d.jpg" % count
  print(path)
  cv2.imwrite(path, test_img)  # save frame as JPG file
  ipath = os.path.join(os.getcwd(), path)
  print(ipath)

  # face detection and alignment
  face_objs = DeepFace.extract_faces(img_path=ipath)

  try:

    for i, face in enumerate(face_objs):

      points = face['facial_area']
      print(points)
      x = points['x']
      y = points['y']
      w = points['w']
      h = points['h']

      original_image = Image.open(ipath)

      face_image = original_image.crop((x, y, x + w, y + h))
      face_image.save(f'image{i}.jpg')
      exists = DeepFace.find(db_path="Use your database path",img_path=f'image{i}.jpg')

      print(".......Face......")
      try:
        if exists[0]['identity'][0]:
          print("..........Face found in Database..........")
        print(exists[0]['identity'][0])
        name = os.path.basename(exists[0]['identity'][0]).split('/')[-1].split('.jpg')
        dict = {
            "name": f"{name}"
        }
        print(dict)

      except:
        print("..........Face not found in Database...........")

      i = i + 1
    print(exists[0])
  except:
    print(".......... Not Face ...........")

  count += 1
  if count == 1:  # used for sample
    break
  if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
    break

cap.release()
cv2.destroyAllWindows
