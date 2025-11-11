# Rama experimental: Fine-Tuning para detección de cultivos y enfermedades

## Objetivo
Explorar y documentar el proceso de entrenamiento / fine-tuning de un modelo de IA específico para:
- Detección de tipos de cultivos (crop classification)
- Identificación de enfermedades en los cultivos

## Alcance
Esta rama es exclusivamente experimental y NO forma parte del contenido del ramo "Proyecto de Programación". No incluye lógica, endpoints ni estructura funcional del proyecto original. Se reutiliza el mismo repositorio solo por conveniencia para facilitar un futuro merge cuando el modelo esté listo.

## Importante
- El código aquí puede ser inestable, incompleto o desechable.
- No se garantiza compatibilidad inmediata con la rama principal.
- No mezclar todavía dependencias ni configuraciones del proyecto académico.
- Esta rama actúa como sandbox de investigación.

## Justificación del uso del mismo repositorio
Se mantiene en el mismo repositorio para:
- Evitar duplicar estructura base (licencias, configuración mínima)
- Acelerar integración futura mediante un merge dirigido
- Mantener trazabilidad del experimento junto al producto final

No implica que esta rama pertenezca al alcance formal del proyecto del ramo. Su uso es aislado y orientado a experimentación.

## Contenido esperado (plan)
- Scripts de preparación de dataset (normalización)
- Pruebas con distintos modelos base (ej: EfficientNet, YOLO)
- Pipeline de entrenamiento (config, augmentations)
- Evaluación (precision, recall, F1)
- Exportación de modelo (ONNX / / formato compatible backend)
- Posibles prototipos de inferencia

## Futura integración
Cuando el modelo alcance madurez:
1. Limpieza de artefactos experimentales
2. Selección de versión de modelo final
3. Merge → incorporación en servicios (ej: plant_service)
4. Ajuste de endpoints y documentación API

## Advertencia
Nada aquí debe asumirse como definitivo para producción. Es un espacio de aprendizaje y prueba.

---