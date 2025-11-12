import os
import shutil
import random

# 📁 Carpeta donde tienes todas las clases
DATASET_DIR = "data/processed/dataset_original"  # cámbiala si es necesario
OUTPUT_DIR = "data/processed/dataset_dividido"

# ⚙️ Porcentajes de división
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.2
TEST_SPLIT = 0.1

# Crear las carpetas destino si no existen
for subset in ["train", "val", "test"]:
    os.makedirs(os.path.join(OUTPUT_DIR, subset), exist_ok=True)

# Recorrer todas las carpetas (clases)
for class_name in os.listdir(DATASET_DIR):
    class_path = os.path.join(DATASET_DIR, class_name)
    if not os.path.isdir(class_path):
        continue  # saltar archivos que no sean carpetas

    print(f"🔍 Procesando clase: {class_name}")

    # Crear carpetas destino para esta clase
    for subset in ["train", "val", "test"]:
        os.makedirs(os.path.join(OUTPUT_DIR, subset, class_name), exist_ok=True)

    # Obtener todas las imágenes de la clase
    images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    random.shuffle(images)

    # Calcular divisiones
    n_total = len(images)
    n_train = int(n_total * TRAIN_SPLIT)
    n_val = int(n_total * VAL_SPLIT)
    n_test = n_total - n_train - n_val

    # Separar las imágenes
    train_imgs = images[:n_train]
    val_imgs = images[n_train:n_train + n_val]
    test_imgs = images[n_train + n_val:]

    # Función auxiliar para copiar imágenes
    def copiar_imagenes(lista, subset):
        for img in lista:
            src = os.path.join(class_path, img)
            dst = os.path.join(OUTPUT_DIR, subset, class_name, img)
            shutil.copy2(src, dst)

    copiar_imagenes(train_imgs, "train")
    copiar_imagenes(val_imgs, "val")
    copiar_imagenes(test_imgs, "test")

    print(f"✅ {class_name}: {n_total} imágenes → Train: {len(train_imgs)}, Val: {len(val_imgs)}, Test: {len(test_imgs)}")

print("\n🎉 División completada correctamente.")
