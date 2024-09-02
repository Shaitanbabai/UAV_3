import cv2
import torch
import os

class ObjectDetection:
    def __init__(self):
        self.__model = self.__load_model()
        self.classes = self.__model.names

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model.to(device)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.faces_dir = "detected_faces"
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)

        # self.face_counter = 0
        self.obj_counter = 0
        self.trackers = {}

    def __load_model(self):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
        return model

    def detected_obj(self, frame):
        results = self.__model(frame)
        detections = results.xyxy[0].cpu().numpy()
        return detections

    def detected_faces(self, roi):
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces

    def create_obj_dir(self):
        self.obj_counter += 1
        obj_dir = os.path.join(self.faces_dir, f"person_{self.obj_counter}")
        if not os.path.exists(obj_dir):
            os.makedirs(obj_dir)
        return obj_dir

    def save_face(self, face_img, obj_dir, face_counter):
        face_filename = os.path.join(obj_dir, f"face_{face_counter}.jpg")
        cv2.imwrite(face_filename, face_img)

    def init_trackers(self, frame, detections):
        # persons = [detection for detection in detections if self.classes[int(detections[5])] == "person"]
        for person in detections:
            x1, y1, x2, y2, conf, class_id = person
            if self.classes[int(class_id)] == "person":
                # person_roi = frame[y1:y2, x1:x2]
                # faces = self.detected_faces(person_roi)

                tracker = cv2.TrackerKCF_create()
                face_coord = (int(x1), int(y1), int(x2 - x1), int(y2 - y1))
                tracker.init(frame, face_coord)

                odj_dir = self.create_obj_dir()
                self.trackers[self.obj_counter] = {"tracker": tracker, "dir": odj_dir, "face_counter": 0}

    def update_trackers(self, frame):
        for person_id, data in self.trackers.items():
            success, person_coord = data["tracker"].update(frame)
            if success:
                x1, y1, w, h = [int(v) for v in person_coord]
                x2, y2 = x1 + w, y1 + h

                person_roi = frame[y1:y2, x1:x2]
                faces = self.detected_faces(person_roi)

                for fx, fy, fw, fh in faces:
                    fx_global, fy_global = x1 + fx, y1 + fy
                    fw_global, fh_global = fx_global + fw, fy_global + fh

                    face_img = person_roi[fy:fy + fh, fx:fx + fw]
                    data["face_counter"] += 1
                    self.save_face(face_img, data["dir"], data["face_counter"])

                    cv2.rectangle(frame,
                                  (fx_global, fy_global),
                                  (fw_global, fh_global),
                                  (0, 255, 0),
                                  2)
                    cv2.putText(frame, f"Face {data['face_counter']}",
                                (fx_global, fy_global - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (255, 0, 0),
                                2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"Person {person_id}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 0, 0),
                            2)

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if len(self.trackers) == 0:
                detections = self.detected_obj(frame)
                self.init_trackers(frame, detections)
            else:
                self.update_trackers(frame)

            cv2.imshow('Трекинг людей', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    obj = ObjectDetection()
    obj.process_video(0)







