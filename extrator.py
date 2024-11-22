import os
from radiomics import featureextractor, logger
import pandas as pd
import logging
from tqdm import tqdm  # Biblioteca para barra de progreso

# Configurar PyRadiomics para mostrar solo advertencias o errores
logger.setLevel(logging.WARNING)

# Carpetas de imágenes y máscaras
image_folder = "Images"  # Cambia esta ruta
mask_folder = "Masks"    # Cambia esta ruta
output_csv = "features_output.csv"

# Inicializar el extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

# Configuración del extractor
extractor.disableAllFeatures()  # Desactivar todas las características
extractor.enableFeatureClassByName('shape2D')  # Activar características de forma para 2D
extractor.enableFeatureClassByName('firstorder')  # Activar estadísticas básicas
extractor.enableFeatureClassByName('glcm')  # Activar características de textura GLCM
extractor.settings['label'] = 255  # Configurar la etiqueta usada en las máscaras

# Lista para almacenar las características
all_features = []

# Obtener lista de imágenes
image_list = [img for img in os.listdir(image_folder) if img.startswith('bus') and img.endswith('.png')]

# Iterar sobre las imágenes con una barra de progreso
for image_name in tqdm(image_list, desc="Procesando imágenes"):
    try:
        # Extraer número y orientación del nombre del archivo
        parts = image_name.split('_')
        if len(parts) < 2:
            print(f"⚠️ Nombre de archivo no válido: {image_name}")
            continue

        base_name, orientation = parts[1].split('-')
        orientation = orientation.replace(".png", "")

        # Construir el nombre de la máscara correspondiente
        mask_name = f"mask_{base_name}-{orientation}.png"
        mask_path = os.path.join(mask_folder, mask_name)
        image_path = os.path.join(image_folder, image_name)

        # Verificar que la máscara exista
        if os.path.exists(mask_path):
            # Extraer características
            features = extractor.execute(image_path, mask_path)
            features['image_name'] = image_name  # Agregar el nombre de la imagen
            all_features.append(features)
        else:
            print(f"⚠️ Máscara no encontrada para {image_name}")
    except Exception as e:
        print(f"Error al procesar {image_name}: {e}")

# Convertir a DataFrame y guardar en CSV
if all_features:
    df = pd.DataFrame(all_features)
    df.to_csv(output_csv, index=False)
    print(f"Características extraídas y guardadas en {output_csv}")
else:
    print("⚠️ No se generaron características. Revisa las imágenes y máscaras.")
