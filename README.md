# PROJET ITK-VTK : Kidney Segmentation & Visualization

### **Author** :
- #### **Login Epita** : ***shubhamkumar.patel***
- #### **Addresse Epita** : ***shubhamkumar.patel@epita.fr***


## Implementation :
- ### Segmentation:
  - It is handled by ITK with `Handle_ITK(params: OriginalFile)`, which is a function that takes care of the segmentation of kidneys from the abdomen.mha file

- ### Visualization:
  - It is handled by VTK with `Handle_VTK(params: OriginalFile, ResultFile, Mode)`, which is a function that takes care of the visualization of segmented kidneys as well as the abdomen itself as 3D volumes. `OriginalFile` is the `abdomen.mha` & `ResultFile` is the `result.mha` which will be generated once `Handle_ITK(OriginalFile)` is called.
  - You can select modes 0, 1, 2 
    - Mode = 0 :  Display segmented and original volumes (DEFAULT)
    - Mode = 1 :  Display original volume 
    - Mode = 2 :  Display segmented volume resulting from Handle_ITK

## Results :

#### Rendering results were saved as images with png format and can be found in the [***results***](results) directory.
#### **The file [***RENDU FINALE.png***](results/RENDU%20FINALE.png) is the choosen final render for the projet.**


In order to replicated the results the projet can be launched by following the instruction below:
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python main.py`

***Tested on machine using Python 3.8***
This should launch a window and should display a 3D Volume of the abdomen among with the Kidneys displayed in a distinct purple color
