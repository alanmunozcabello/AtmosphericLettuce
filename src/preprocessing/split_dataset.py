import os
import shutil
import random

source_dir = "data/processed/dataset_original"
target_dir = "data/processed/dataset_dividido"

for subset in ["train", "val", "test"]:
    os.makedirs(os.path.join(target_dir, subset), exist_ok=True)

train_ratio, val_ratio, test_ratio = 0.7, 0.15, 0.15

for class_name in os.listdir(source_dir):
    class_path = os.path.join(source_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    images = os.listdir(class_path)
    random.shuffle(images)
    total = len(images)

    train_end = int(total * train_ratio)
    val_end = int(total * (train_ratio + val_ratio))

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for subset, subset_images in splits.items():
        subset_path = os.path.join(target_dir, subset, class_name)
        os.makedirs(subset_path, exist_ok=True)
        for img in subset_images:
            shutil.copy(os.path.join(class_path, img), os.path.join(subset_path, img))

    print(f"📦 {class_name}: {len(images)} imágenes divididas correctamente.")
