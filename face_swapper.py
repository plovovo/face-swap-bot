import insightface
import numpy as np
import cv2
import os

class FaceSwapper:
    def __init__(self):
        self.model = insightface.app.FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        self.model.prepare(ctx_id=0)

        model_path = os.path.abspath("models/inswapper_128.onnx")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель не найдена: {model_path}")

        self.swap_model = insightface.model_zoo.get_model(model_path, download=False, providers=['CPUExecutionProvider'])

    def swap_faces(self, source_img, target_img):
        source_faces = self.model.get(source_img)
        target_faces = self.model.get(target_img)

        if not source_faces:
            raise Exception("Не найдено лицо на исходном фото")
        if not target_faces:
            raise Exception("Не найдено лицо на целевом фото")

        source = source_faces[0]
        res = target_img.copy()
        for face in target_faces:
            res = self.swap_model.get(res, face, source)

        return res
