import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("ruta_del_modelo")
tflite_model = converter.convert()

with open("modelo.tflite", "wb") as f:
    f.write(tflite_model)
