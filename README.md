<h1 align="center">
  
 Deepcatcher Deepfake Detection Model

 </h1>

<i align="center">

![Covers Subjects](https://github.com/NKAmazing/Deepcatcher_Detection/assets/83615373/06a781c3-7561-43f3-a8b4-27c43c4ff85b)

An AI solution made to detect fake images generated with AI using Deep learning.

</i>

## About
Deepcatcher is a software solution designed to detect images manipulated with Artificial Intelligence, commonly referred to as Deepfakes. The application employs a robust Machine Learning model to provide accurate predictions of image authenticity. Users interact with Deepcatcher through a responsive web interface, where they can upload images for analysis.
The application also incorporates a user registration system, enabling users to log in, save their prediction results, and submit feedback or reports on the predictions made. This comprehensive approach ensures not only high accuracy in detecting fake images but also a user-friendly experience that facilitates ongoing interaction and improvement through user feedback. The combination of advanced AI techniques and a simplified web interface positions Deepcatcher as a valuable tool in the fight against digital image manipulation.

## Architecture

<h3 align="left">
  
<img src="https://github.com/NKAmazing/Deepcatcher_Detection/assets/83615373/5d7d9617-b7f0-4490-b8ba-8dd3133c7c4f" alt="Arquitectura de Deepcatcher" width="800">

</h3>

### Detection Model
Artificial Intelligence model trained from a pre-trained convolutional neural network (cnn) to guarantee greater results in metrics and performance of use.

**Features**
* Direct Connection: The detection model is loaded through a direct connection between the Frontend service and the model service. This is facilitated by TensorFlow tools that allow quick loading of a model in a Python script.
* Pretrained with Transfer Learning: The model leverages a pretrained CNN to enhance its ability to detect deepfake images
* Scalable: Designed to be scalable, allowing for the analysis of a large volume of images simultaneously.
* Multi-platform Compatibility: Supports deployment across multiple platforms and environments, ensuring flexibility in deployment options.
  
### Backend
Consists of a REST API created with the framework Django, providing a RESTful API to manage the main functionalities of the application.

**Features**
* User Registration Tool: Allows the creation and management of user accounts.
* Prediction History Tool: Records and allows the consultation of predictions made by users.
* User Reporting Tool: Users can make reports related to the predictions or any other aspect of the application.
* SQL Database: User data, predictions, and reports are stored in an SQL database, ensuring data persistence and accessibility.
  
### Frontend
Multi-page Web Interface built with Streamlit, an open-source Python framework for data scientists and AI/ML engineers to deliver interactive data apps, which allows the quick and easy creation of web interfaces.

**Features**
* File Management Microservice: Facilitates the management of files that users upload for predictions.
* Deepcatcher Web Pages: Provide the user interface to interact with the various functionalities of the application, such as uploading files for detection, viewing prediction history, and reports.

## Repository Structure

The repository is structured as follows:
```
    .
    ├── app                      # App Folder: Contains the Streamlit web environment that loads the model, predicts incoming images, and communicates with the API, which is located in a separate repository.
    ├── detection_model          # Detection Model Folder: Contains the trained model implemented in a Python notebook. 
    ├── .gitignore               # File to allow Git to ignore any kind of files in the repository.
    ├── README.md                # Documentation file that stores a brief explanation about the project                
    └── requirements.txt         # Software Dependencies and Libraries that provides support for the software functionalities.
```

## Credits
- Student: [<i>**Nicolas Mayoral**</i>](https://github.com/NKAmazing)
- Specialist Tutor in Charge: <i>**Mariela Asensio**</i>
- Institution: [<i>Universidad de Mendoza - Facultad de Ingenieria</i>](https://um.edu.ar/ingenieria/)

![um-cover](https://user-images.githubusercontent.com/83615373/235419081-c36fcb36-c412-4317-b40a-7cad5e937339.png)
