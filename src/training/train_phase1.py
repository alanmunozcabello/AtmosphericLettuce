"""
Entrenamiento Fase 1 - Clasificación de cultivos saludables
Modelo: EfficientNetB0 (TensorFlow / Keras)
Autor: Alan + Mentor IA 🌱
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models
import os

# ===============================
# 🔧 CONFIGURACIÓN
# ===============================
BASE_DIR = "data/processed/dataset_dividido"
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VAL_DIR = os.path.join(BASE_DIR, "val")
TEST_DIR = os.path.join(BASE_DIR, "test")

IMG_SIZE = (224, 224)       # Tamaño estándar para EfficientNetB0
BATCH_SIZE = 32
EPOCHS = 15                 # Puedes ajustar según rendimiento
LEARNING_RATE = 1e-4

# ===============================
# 🧠 GENERADORES DE DATOS
# ===============================
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1.0/255.0)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

# ===============================
# 🧱 MODELO BASE
# ===============================
base_model = EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(*IMG_SIZE, 3)
)
base_model.trainable = False  # Congelamos las capas del modelo base

# ===============================
# 🔗 CONSTRUCCIÓN DEL MODELO
# ===============================
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(train_generator.num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ===============================
# 🚀 ENTRENAMIENTO
# ===============================
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# ===============================
# 💾 GUARDAR MODELO
# ===============================
os.makedirs("models", exist_ok=True)
model.save("models/efficientnetb0_phase1.h5")

print("✅ Modelo guardado correctamente en 'models/efficientnetb0_phase1.h5'")
