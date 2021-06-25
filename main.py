import itk
import vtk
import matplotlib.pyplot as plt

FILENAME = "abdomen.mha"
RESULTNAME = "result.mha"

def display(img, L):
    '''
    Parameters
    ----------
    img : TYPE Image
        DESCRIPTION.
            3D Image Array similar to Numpy arrays 
    L : TYPE List
        DESCRIPTION.
            List containing two coordinates for locating the kidneys in the 3D vector space
    Returns
    -------
    None.
    '''    
    # Display image with matplotlib to pick a coordinate
    plt.ion()
    plt.figure(figsize=(10,10))
    plt.imshow(img[L[0][0], :, :], cmap="gray")
    plt.scatter(L[0][1], L[0][2], color='r', marker='+')
    plt.show()

    plt.ion()
    plt.figure(figsize=(10, 10))
    plt.imshow(img[L[1][0], :, :], cmap="gray")
    plt.scatter(L[1][1], L[1][2], color='r', marker='+')
    plt.show()


def Handle_ITK(FILENAME):
    '''
    Parameters
    ----------
    FILENAME : TYPE String
        DESCRIPTION.
            Path to the file we want to process (it should be a .mha file)
    Returns
    -------
    cast : Image of type Unsigned Char obtained after applying a segmentation on the input image
        DESCRIPTION.

    '''
    # Read Image using provided FILENAME
    input_image = itk.imread(FILENAME)
    # Provided image is of type Short therefore we use itk.SS
    image_type = itk.Image[itk.SS, 3]

    # Perform a Threshold Filtering operation on image inorder to Extract/Segment kidneys from abdomen.mha
    thresh = itk.ConnectedThresholdImageFilter[image_type, image_type].New(input_image)
    
    # 400 & 185 are values for up and lower threshold were obtained experimentally ,
    # by try out different values in search of a better segmentation
    thresh.SetUpper(400)
    thresh.SetLower(180)
    thresh.AddSeed([160, 230, 10]) # Coordinates of a pixel from the left Kidney
    thresh.AddSeed([355, 335, 95]) # Coordinates of a pixel from the right Kidney
    thresh.Update()
    
    # TODO: Need to try out some techniques to fill in the holes maybe using opening and closing techniques
    ###
    
    # Finally we need to perform a conversion of type from Short to Unsigned char using itk.UC
    cast_image_type = itk.Image[itk.UC, 3]
    cast = itk.RescaleIntensityImageFilter[input_image, cast_image_type].New(thresh.GetOutput())
    cast.SetOutputMinimum(0)    # Min pixel value is et to 0
    cast.SetOutputMaximum(255)  # Max pixel value is et to 100
    cast.Update()
    
    # Writing thresholded image into file RESULTNAME
    itk.imwrite(cast.GetOutput(), RESULTNAME)
    return cast


def Handle_VTK(input_image, result_image, coordinates, mode=0):
    '''
    Parameters
    ----------
    input_ : TYPE 
        DESCRIPTION.
    res : TYPE Itk Image
        DESCRIPTION.
            Image returned by Handle_ITK(FILENAME) function
    coordinates : TYPE List
        DESCRIPTION.
            List containing two coordinates for locating the kidneys in the 3D vector space
    mode : TYPE integer
        DESCRIPTION.
            - 0 Default - Volume & Segmented Image are overlayed on each other
            - 1 Deactivated Overlay & only displays input image as a volume
            - 2 Deactivated Overlay & only displays segmented image as a volume
    Returns
    -------
        None.
    '''
    # Load colors palette
    colors = vtk.vtkNamedColors()
    
    # Source
    # cube = vtk.vtkCubeSource()
    image = vtk.vtkMetaImageReader()
    image.SetFileName(input_image)

    # Mapper for Source data
    cube_mapper = vtk.vtkSmartVolumeMapper()
    cube_mapper.SetInputConnection(image.GetOutputPort())
    
    # Volume Properties
    prop = vtk.vtkVolumeProperty()
    opacity_func = vtk.vtkPiecewiseFunction()
    opacity_func.AddPoint(25, 0.0)
    opacity_func.AddPoint(255, 0.1)
    prop.SetScalarOpacity(opacity_func)
    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(25, 0, 0, 0)
    color.AddRGBPoint(255, 0.75, 0.75, 0.75)
    prop.SetColor(color) 
    
    # Volume / Actor
    cube_volume = vtk.vtkVolume()
    cube_volume.SetMapper(cube_mapper)
    cube_volume.SetProperty(prop)
    
    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.0, 0.0, 0.0)
    renderer.AddActor(cube_volume)
    renderer.SetBackground(colors.GetColor3d('peru'))
    light = vtk.vtkLight()
    light.SetIntensity(100)
    light.SetFocalPoint(0.5, 1.5, 0)
    light.SetColor(1.0, 0.0, 0.0)
    light.SetPosition(10, 5, 5)
    renderer.AddLight(light)
    renderer.SetUseFXAA(True);

    # Render Itk Result obtained after segmenting the Kidneys
    # Source
    # cube = vtk.vtkCubeSource()
    res_image = vtk.vtkMetaImageReader()
    res_image.SetFileName(result_image)

    # Mapper for Source data
    res_cube_mapper = vtk.vtkSmartVolumeMapper()
    res_cube_mapper.SetInputConnection(res_image.GetOutputPort())
    
    # Volume Properties
    res_prop = vtk.vtkVolumeProperty()
    res_opacity_func = vtk.vtkPiecewiseFunction()
    res_opacity_func.AddPoint(25, 0.0)
    res_opacity_func.AddPoint(255, 1)
    res_prop.SetScalarOpacity(opacity_func)
    res_color = vtk.vtkColorTransferFunction()
    res_color.AddRGBPoint(25, 0, 0, 0)
    res_color.AddRGBPoint(255, 0.5, 0.5, 0.95)
    res_prop.SetColor(res_color) 
    res_prop.SetSpecular(0.9)
    res_prop.SetSpecularPower(10)
   
    
    # Volume / Actor
    res_cube_volume = vtk.vtkVolume()
    res_cube_volume.SetMapper(res_cube_mapper)
    res_cube_volume.SetProperty(res_prop)
    
    # FINAL RENDERER : Combining segmented kidneys and the rest of the abdomen 
    final_renderer = vtk.vtkRenderer()
    final_renderer.AddActor(cube_volume)
    final_renderer.AddActor(res_cube_volume)
    final_renderer.SetBackground(colors.GetColor3d('peru'))
    final_renderer.SetBackground2(colors.GetColor3d('peru'))
    final_renderer.SetUseFXAA(True);

    # Rendering Window
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("Simple VTK Abdomen - Kidney Segmentation")
    render_window.SetSize(600, 600)
    render_window.SetMultiSamples(500)
    render_window.AddRenderer(final_renderer)
    
    # Create an interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    
    # Initialize the interactor and start the rendering loop
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

if __name__ == '__main__':
    print(itk.Version.GetITKVersion())
    print(vtk.vtkVersion.GetVTKVersion())
    res = Handle_ITK(FILENAME)
    # coordinates =  [[10, 160, 230], [95, 355, 335]]
    # display(res.GetOutput(), coordinates)
    Handle_VTK(FILENAME, RESULTNAME, coordinates)
