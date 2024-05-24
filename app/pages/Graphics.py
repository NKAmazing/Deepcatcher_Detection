# import streamlit as st
# import numpy as np
# import tensorflow as tf
# import matplotlib.pyplot as plt

# # Model paths
# model_paths = ['../detection_model/models/model_0.h5', '../detection_model/models/model_1.h5', '../detection_model/models/model_2.h5', '../detection_model/models/model_3.h5']

# # Load the model
# model = tf.keras.models.load_model(model_paths[3])

# def get_model_data(model, train_batch):
#     # Obtenemos los valores de pérdida y exactitud
#     loss, accuracy = model.evaluate(train_batch)
#     return loss, accuracy

# def train_batch_generator():
#     train_dir = '../detection_model/data/dataset/train'
#     target_size = (96, 96)
#     batch_size = 32
#     datagen = tf.keras.preprocessing.image.ImageDataGenerator(horizontal_flip=True, vertical_flip=False, rescale=1./255)

#     train_batch = datagen.flow_from_directory(train_dir, class_mode="binary", target_size=target_size, batch_size=batch_size, subset="training")
#     return train_batch

# def plotter(loss, accuracy):
#     st.write(
#         """
#         En esta sección se mostrarán los gráficos de exactitud y pérdida del modelo de detección de imágenes falsas.
#         """
#     )
#     # Crear un gráfico de exactitud
#     plt.figure(figsize=(8, 6))
#     plt.plot(accuracy, label='Exactitud')
#     plt.xlabel('Época')
#     plt.ylabel('Exactitud')
#     plt.title('Gráfico de Exactitud')
#     plt.legend()
#     plt.savefig('exactitud.png')

#     # Crear un gráfico de pérdida
#     plt.figure(figsize=(8, 6))
#     plt.plot(loss, label='Pérdida')
#     plt.xlabel('Época')
#     plt.ylabel('Pérdida')
#     plt.title('Gráfico de Pérdida')
#     plt.legend()
#     plt.savefig('perdida.png')

#     st.image('exactitud.png', caption='Gráfico de Exactitud')
#     st.image('perdida.png', caption='Gráfico de Pérdida')


# if __name__ == '__main__':
#     st.title('Gráficos del Modelo de Detección de Imágenes Falsas')

#     train_batch = train_batch_generator()
#     loss, accuracy = get_model_data(model, train_batch)

#     page_names_to_funcs = {
#         "Inicio": None,
#         "Gráficos Plotting": lambda: plotter(loss, accuracy)
#     }

#     graph_name = st.sidebar.selectbox("Selecciona un gráfico", page_names_to_funcs.keys())
#     page_names_to_funcs[graph_name]()

