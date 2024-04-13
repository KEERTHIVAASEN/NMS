import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_data(dir_path, target_size=(150,150), batch_size=512):
    data = ImageDataGenerator(rescale=1./255)
    generator = data.flow_from_directory(
        dir_path,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary')
    return generator

def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(150,150,3)),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dense(40, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

def classify_images(model, dir_path):
    file_names = os.listdir(dir_path)
    for file_name in file_names:
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(dir_path, file_name)
            img = Image.open(img_path).resize((150, 150))
            img_array = np.expand_dims(np.asarray(img, dtype=np.float32), axis=0) / 255.0
            classes = model.predict(img_array)
            print(f"{file_name}: {'Dog' if classes[0] > 0.5 else 'Cat'}")

def main():
    train_dir = '/Pred/dogs/train'
    val_dir = '/Pred/dogs/validation'
    test_dir = '/Pred/dogs'

    train_generator = load_data(train_dir)
    val_generator = load_data(val_dir)

    model = create_model()

    model.fit(train_generator, epochs=3, validation_data=val_generator)

    classify_images(model, test_dir)

if __name__ == "__main__":
    main()