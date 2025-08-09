# Mejorado con MobileNetV2 y Xception + Preprocesamiento MTCNN + Data Augmentation + Metrics Avanzadas

# Librerías necesarias
# !pip install mtcnn

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2, Xception
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC
from sklearn.utils import class_weight
from mtcnn.mtcnn import MTCNN
import cv2

# === Parámetros ===
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30

train_dir = "../data/140k-real-and-fake-faces/real_vs_fake/real-vs-fake/train"
val_dir = "../data/140k-real-and-fake-faces/real_vs_fake/real-vs-fake/valid"
test_dir = "../data/140k-real-and-fake-faces/real_vs_fake/real-vs-fake/test"

# --- Detección y recorte facial ---
def crop_face(image):
    detector = MTCNN()
    faces = detector.detect_faces(image)
    if faces:
        x, y, w, h = faces[0]['box']
        x, y = max(0, x), max(0, y)
        return image[y:y+h, x:x+w]
    return image

def preprocess_and_save(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for root, _, files in os.walk(input_dir):
        for f in files:
            img_path = os.path.join(root, f)
            img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
            face = crop_face(img)
            face = cv2.resize(face, IMG_SIZE)
            rel_path = os.path.relpath(root, input_dir)
            save_path = os.path.join(output_dir, rel_path)
            os.makedirs(save_path, exist_ok=True)
            cv2.imwrite(os.path.join(save_path, f), cv2.cvtColor(face, cv2.COLOR_RGB2BGR))

# Preprocesa train/val/test (solo la primera vez)
preprocess_and_save(train_dir, "./preprocessed/train_faces")
preprocess_and_save(val_dir, "./preprocessed/valid_faces")
preprocess_and_save(test_dir, "./preprocessed/test_faces")

# === Data Augmentation ===
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=10,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   horizontal_flip=True)
val_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory('./preprocessed/train_faces',
                                                    target_size=IMG_SIZE,
                                                    batch_size=BATCH_SIZE,
                                                    class_mode='binary')
validation_generator = val_datagen.flow_from_directory('./preprocessed/valid_faces',
                                                       target_size=IMG_SIZE,
                                                       batch_size=BATCH_SIZE,
                                                       class_mode='binary')

# --- Pesos de clase ---
y_train = train_generator.classes
class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights_dict = {i: class_weights[i] for i in range(len(class_weights))}

# === Modelo 1: MobileNetV2 ===
base_mobilenet = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMG_SIZE + (3,))
base_mobilenet.trainable = False

mobilenet_model = models.Sequential([
    base_mobilenet,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

mobilenet_model.compile(optimizer=Adam(learning_rate=1e-4),
                        loss='binary_crossentropy',
                        metrics=['accuracy', AUC(name='auc')])

callbacks = [EarlyStopping(patience=7, restore_best_weights=True),
             ReduceLROnPlateau(patience=3, factor=0.2, verbose=1),
             ModelCheckpoint('mobilenet_model.h5', save_best_only=True)]

history_mobilenet = mobilenet_model.fit(train_generator,
                                        validation_data=validation_generator,
                                        epochs=EPOCHS,
                                        class_weight=class_weights_dict,
                                        callbacks=callbacks)

# === Modelo 2: Xception ===
base_xception = Xception(weights='imagenet', include_top=False, input_shape=IMG_SIZE + (3,))
base_xception.trainable = False

xception_model = models.Sequential([
    base_xception,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

xception_model.compile(optimizer=Adam(learning_rate=1e-4),
                       loss='binary_crossentropy',
                       metrics=['accuracy', AUC(name='auc')])

callbacks_x = [EarlyStopping(patience=7, restore_best_weights=True),
               ReduceLROnPlateau(patience=3, factor=0.2, verbose=1),
               ModelCheckpoint('xception_model.h5', save_best_only=True)]

history_xception = xception_model.fit(train_generator,
                                      validation_data=validation_generator,
                                      epochs=EPOCHS,
                                      class_weight=class_weights_dict,
                                      callbacks=callbacks_x)

# === Evaluación final ===
test_generator = test_datagen.flow_from_directory('./test_faces',
                                                  target_size=IMG_SIZE,
                                                  batch_size=BATCH_SIZE,
                                                  class_mode='binary',
                                                  shuffle=False)

mobile_results = mobilenet_model.evaluate(test_generator)
xception_results = xception_model.evaluate(test_generator)

print("MobileNetV2 Test Results - Loss: {:.4f}, Accuracy: {:.4f}, AUC: {:.4f}".format(*mobile_results))
print("Xception Test Results - Loss: {:.4f}, Accuracy: {:.4f}, AUC: {:.4f}".format(*xception_results))
