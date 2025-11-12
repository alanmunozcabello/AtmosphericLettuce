import os

def contar_imagenes_por_clase(base_dir):
    total = 0
    for folder in os.listdir(base_dir):
        path = os.path.join(base_dir, folder)
        if os.path.isdir(path):
            count = len(os.listdir(path))
            total += count
            print(f"{folder:<40} {count}")
    print("=" * 40)
    print(f"TOTAL DE IMÁGENES: {total}")
