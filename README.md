# PROJET ITK-VTK : Kidney Segmentation

### **Author** :
- #### **Login Epita** : ***shubhamkumar.patel***
- #### **Addresse Epita** : ***shubhamkumar.patel@epita.fr***


## Implementation :
- ### Segmentation:
  - It is handled by ITK with Handle_ITK(param: FILENAME or FILEPATH), which is a function that takes care of the segmentation of kidneys from the abdomen.mha file

- ### Visualization:
  - It is handled by VTK with Handle_VTK(params: OriginalFile, ResultFile, Mode), which is a function that takes care of the visualization of segmented kidneys as well as the abdomen itself as 3D volumes.
  - You can select modes 0, 1, 2 
    - MODE 0 :  Display segmented and original volumes 
    - MODE 1 :  Display original volume 
    - MODE 2 :  Display segmented volume resulting from Handle_ITK

## Results :
#### Rendering results were saved as images with png format and can be found in the ***results*** directory.
#### **The file named ***RENDU FINALE.png*** is the choosen final render for the projet.**


In order to replicated the results the projet can be launched by following the instruction below:
- virtualenv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python main.py

***Tested on machine using Python 3.8***
This should launch a window and should display a 3D Volume of the abdomen among with the Kidneys displayed in a distinct purple color
