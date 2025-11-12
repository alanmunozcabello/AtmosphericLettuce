import os

# Diccionario de mapeo
class_map = {
    "0": "Apple___Apple_scab",
    "1": "Apple___Black_rot",
    "2": "Apple___Cedar_apple_rust",
    "3": "Apple___healthy",
    "4": "Blueberry___healthy",
    # ... resto de clases ...
    "37": "Tomato___healthy"
}

# Ruta base
base_path = "data/dataset_original"

for folder_name in os.listdir(base_path):
    old_path = os.path.join(base_path, folder_name)
    if os.path.isdir(old_path) and folder_name in class_map:
        new_path = os.path.join(base_path, class_map[folder_name])
        os.rename(old_path, new_path)
        print(f"✅ Renombrado: {folder_name} → {class_map[folder_name]}")
