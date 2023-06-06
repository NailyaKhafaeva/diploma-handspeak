num_classes = 23
img_rows, img_cols = 28, 28
batch_size = 32

train_data_dir = 'letters/hand_gestures/train'
validation_data_dir = 'letters/hand_gestures/test'

# # train_data_dir = 'numbers/hand_gestures/train'
# # validation_data_dir = 'numbers/hand_gestures/test'

# Аугментация данных
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=30,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=False,
    fill_mode='nearest')

validation_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=30,
    fill_mode='nearest')

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_rows, img_cols),
    batch_size=batch_size,
    color_mode='grayscale',
    class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_rows, img_cols),
    batch_size=batch_size,
    color_mode='grayscale',
    class_mode='categorical')


log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1), padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1), padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1),  padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

print(model.summary())


model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

nb_train_samples = 23420
nb_validation_samples = 11750
epochs = 7

# nb_train_samples = 10179
# nb_validation_samples = 5204
# epochs = 7

history = model.fit(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    callbacks=[tb_callback])

model.save("numbers.h5")