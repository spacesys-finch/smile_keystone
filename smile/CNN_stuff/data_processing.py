import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px
import pandas as pd

# a seperate file named data_from which stores location of whatever dataset you want analyzed
from data_from import indian_pine, indian_pine_wavelength_separation, spectral_monuments_min, spectral_monuments_max

metadata = indian_pine_wavelength_separation

# The data that is being analyzed (.npy file), and the file that the data will be written into 
data = np.load(indian_pine)

# ---------- Aux Functions (These functions pobs won't be called, but they're used for the other functions) ---------- #
file_path = indian_pine

def normalize_pixels(array_to_normalize: np.array, maximum_pixel: int):
    '''
    I have to normalize the pixels because its in watts per square meter per steradian (whut) 
    
    Function takes two parameters: 
    array_to_normalize is a numpy array. It is the array with values in watts per square meter per steradian (this function is more or less attatched to the create_band_sheet function)
    maximum_pixel is an integer that is the maximum value in watts per square meter per steradian 
    '''
    
    # Gets the size of the data that will be created so we can iterate all the data
    data_shape = data.shape

    # Creates the array that we will be putting data into once the data is normalized. Creates an array that is the same size as the data but with all 0s
    normalized_array = np.zeros((data.shape[0], data.shape[1]))

    # normalizes the data 
    for number1 in range(0, data_shape[0]):
        for number2 in range(0, data_shape[1]):
            to_put = (array_to_normalize[number1][number2] / maximum_pixel) * 255

            normalized_array[number1][number2] = to_put

            print(normalized_array[number1][number2])

    return normalized_array

# Specific band for a certain pixel
def pixel_wavelength_information(result=[int, int, int]):
    '''
    Takes a pixel and prints out a particular wavelength for it in the specified band. Takes 3 integers in a list, first two inputs (result[0] and result[1]) 
    correspond to the spot they take up on the image, and the third input (result[2]) corresponds to the wavelength band that you want to use
    '''
    
    # result[0] is the x component and result[1] is the y component and result [2] is the specific wavelength you want to see
    return (data[result[0]][result[1]][result[2]])

# Gets all the wavelength data for a particular pixel
def pixel_information(result=[int, int]):
    '''
    Takes a pixel and prints out all the wavelengths for that particular pixel. result[0] corresponds to x location and result[1] corresponds to y location on the image
    '''
    
    # result[0] is the x component and result[1] is the y component
    return (data[result[0]][result[1]])

# ----- Real Functions (this is the stuff that'll get used I think) ----- #

def cook_a_line(wavelength:int, height: int):
    '''
    Gets you a graph for a line at a certain height at a certain wavelength. 
    
    wavelength: Represents the wavelength band you are selecting
    height: I think its from the top down???? so maybe it should be depth??? idk ill figure it out in the future
    '''
    
    # Gets the size of the data that will be created so we can iterate all the data
    data_shape = data.shape
    
    to_graph_array = []
    numbers = []
    
    for pixel_number in range(data_shape[1]):
        first = pixel_information([height, pixel_number])
        pixel_informations = pixel_wavelength_information([height, pixel_number, wavelength])
        
        to_graph_array.append(pixel_informations)
        numbers.append(pixel_number)
        
    plt.title("Band Graph")
    plt.xlabel("Location")
    plt.ylabel("Brilliance")
    plt.plot(numbers, to_graph_array)
    plt.show()

def create_band_sheet(wavelength: int, selection: int):
    # WORKS PROPERLY!!
    '''
    Creates a big fat 145 * 145 numpy array of all the pixels at a certain band/wavelength, then creates an image using Pillow 
    
    Parameter 1: wavelength integer is the index of the wavelength you want to call (might change this over so you can put in the actual 
    wavelength, but that is a something for another time :D)
    
    Parameter 2: 1 indicates it is normalized to 255, 2 indicates use brilliance values
    '''
    
    # Sets the thing to infinity so none of that "..." truncating funny business happens
    np.set_printoptions(threshold=np.inf)
    
    # Gets the shape of the data, only ever tried this on the indian pines dataset but hopefully it'll work for anything 
    data_shape = data.shape
    
    # this and the "thing += 1" in the nested for loop below counts the number of pixels, should match up to data_shape[0] * data_shape[1], if it doesn't ya done goofed up 
    #thing = 0
    
    # Makes an array with data_shape[0] * data_shape[1] pixels to put numbers into 
    my_array = np.zeros((data_shape[0], data_shape[1]))
    
    # This gets the highest watt per square meter per steradian for the normalization function
    maximum_pixel_brilliance = 0
    
    # iterates through the elements in the array and puts it into my_array, units are in watts per square unit per steradian
    for number1 in range(0, data_shape[0]):
        for number2 in range(0, data_shape[1]):
                      
            # Specifies the pixel you want the information for, and the band you want it from
            to_get = [number1, number2, wavelength]
            
            # Passes above information into the pixel_wavelength_information, and it gets the (brilliance?) of a pixel
            to_put = pixel_wavelength_information(to_get)
            
            # To find the maximum brightness pixel, the max is compared
            maximum_pixel_brilliance = max(maximum_pixel_brilliance, to_put)
            
            # The numpy array at [number1][number2] becomes the value that was found in the variable to_put
            my_array[number1][number2] = to_put

    # Normalizes the array using the normalize_pixels function
    if selection == 1:
        normalized_array = normalize_pixels(my_array, maximum_pixel_brilliance)
 
        plt.imshow(normalized_array)

        # img.show()
        plt.show()
    else: 
        plt.imshow(my_array)
        plt.show()

def woaw_beautiful(pixel_x:int, pixel_y:int):
    '''
    
    Gets all the wavelengths for a pixel and graphs it out
    
    pixel_x = x location of pixel 
    pixel_y = y location of pixel 
    
    Same as the pixel_graph function, except made in plotly, which gives more interactivitiy abilities and I can also graph the vertical lines
    
    Uses something called plotly to run, must be run in a interactive window (or jupyter)
    
    Import ipykernel and pip install --upgrade nbformat and hopefully it works
    
    
    '''

    # Gets the brilliance values for all the wavelengths of the pixel location provided
    thing = pixel_information([pixel_x, pixel_y])

    # Shape of the data 
    data_shape = thing.shape

    # Two lists that are appended to, creating the stuff that will be used to graph later
    thing_1 = []
    thing_2 = []

    # Goes over every wavelength and adds its brillaince value to thing_2, the wavelength is added to thing_1
    for thinint in range(data_shape[0]):
        thing_1.append(thinint * metadata[1] + metadata[0])
        thing_2.append(thing[thinint])

    # Makes a panda table with the lists created above to be made into a list later 
    df = pd.DataFrame({"Wavelength": thing_1, "Brilliance": thing_2})

    # Graph created 
    fig = px.line(df, x="Wavelength", y="Brilliance")

    # Iterates over all the minimum wavelengths and puts them onto the graph 
    for minimum_wavelength in spectral_monuments_min:

        # Used to make sure the list is longer than 1, it is is, a rectangle is added
        try:

            # DO NOT DELETE THIS, this triggers an error if its only a single element (variable isn't used that butat's how its supposed to be) 
            items = len(minimum_wavelength)
       
            # Rectangle added to the figure
            fig.add_vrect(x0=minimum_wavelength[0], x1=minimum_wavelength[1], opacity=0.1, line_width=0, fillcolor="red")
            
        # If the length of minimum wavelength gives an error, it is not a list, so it only makes a line 
        except TypeError:
            
            # Line added to the figure 
            fig.add_vline(x=minimum_wavelength, line_width=0.5, line_dash="dash", line_color="red", opacity=0.75)
            
    for maximum_wavelength in spectral_monuments_max:

        # Used to make sure the list is longer than 1, it is is, a rectangle is added
        try:
            
            # DO NOT DELETE THIS, this triggers an error if its only a single element (variable isn't used that butat's how its supposed to be) 
            items = len(maximum_wavelength)
            
            # Rectangle added to the figure
            fig.add_vrect(x0=maximum_wavelength[0], x1=maximum_wavelength[1], opacity=0.1, line_width=0, fillcolor="blue")
            
        # If the length of minimum wavelength gives an error, it is not a list, so it only makes a line 
        except TypeError:
            
            # Line added to the figure 
            fig.add_vline(x=maximum_wavelength, line_width=0.75, line_dash="dash", line_color="blue", opacity=0.75)

    # Figure is displayed 
    fig.show()


def pixel_graph(pixel_x:int, pixel_y:int): 
    # WORKS PROPERLY!!
    '''
    Gets all the wavelengths for a pixel and graphs it out
    
    pixel_x = x location of pixel 
    pixel_y = y location of pixel 
    '''

    # Gets the brilliance values for all the wavelengths of the pixel location provided
    thing = pixel_information([pixel_x, pixel_y])

    # Gets the shape of the thing
    data_shape = thing.shape
    
    # Lists to be graphed 
    thing_1 = []
    thing_2 = []

    # Graphs the wavelength in thing_1 and brilliance in thing_2
    for thinint in range(data_shape[0]):
        thing_1.append(thinint * metadata[1] + metadata[0])
        thing_2.append(thing[thinint])

    # Makes the stuff into a numpy to be graphed
    thing_1 = np.array(thing_1)
    thing_2 = np.array(thing_2)
    
    # Graphs the stuff 
    plt.title("Pixel Graph")
    plt.xlabel("Wavelength Band")
    plt.ylabel("Brilliance")
    plt.plot(thing_1, thing_2)
    plt.show()   
    
# If none is specified as the input for this function, this function will ask you what function you want to call later on, if it is specified, it'll call it automatically
# this is better for automation
def calling_function(to_call=None, list_of_numbers = [None, None, None]):
    '''
    This function currently doesn't do anything 
    
    This function calls other functions, such as pixel_information and pixel_wavelength_information (above)
    
    The "to_call"
    '''
    print("Something happened!")
    
    # The "indian_pine_array.npy" file has the dimensions (145, 145, 200), so its a 145 by 145 image (145 squared pixels) with 200 wavelenghths per pixel
    
    # Makes it so python doesn't truncate it and make those "..." when there's more data let's you see all the data basically
    np.set_printoptions(threshold=np.inf)
    
    # This list contains all the actual wavelengths, the numbers here will just be placeholders for until I actually get the wavelengths provided
    # These numbers can be considered the "bands" of the data, where band 1 (first element in the list) corresponds to the first wavelength
    wavelength_list = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
        61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 
        71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 
        81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 
        91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 
        101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 
        111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 
        121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 
        131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 
        141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 
        151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 
        161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 
        171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 
        181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 
        191, 192, 193, 194, 195, 196, 197, 198, 199, 200
    ]
    
    # Tells you the dimensions of the image
    # print(data.shape)
    
    # Provides all the wavelength data for the first pixel in the first column 
    # print(data[0][0])
    
    numba = True
    
    # Writes every row into the text file you provided in "file_path"
    with open(file_path, 'w') as file:
        for row in data: 
            if numba: 
                # print(row[0][0])
                numba = False
            row = str(row)
            file.write(str(row))
            
# Prints out all the functions that are callable from calling_function, as well as their docstrings and what they need
def halp(): 
    print("\n")
    
    # A dictionary of all the functions, and references the function it is meant to represent
    my_functions = {
        "pixel_information": pixel_information, 
        "pixel_wavelength_information": pixel_wavelength_information,
        "create_band_sheet": create_band_sheet, 
    }
    
    for defined_function in my_functions.keys(): 
        print(defined_function + ": " + my_functions[defined_function].__doc__)

def make(): 
    pass     

# tbh I don't think I'm ever gonna finish the below function not much point in making it easy to use if you can just type the function name in
def caller(): 
    # This function calls the other functions
    continue_calling = True

    while continue_calling: 
        command = input('What function do you want? "Stop" for Stopping (unexpected!) and "Help" for a list of commands')
        if command == "Stop": 
            continue_calling = False
            continue
        elif command == "Help":
            halp()

create_band_sheet(3, 2)
cook_a_line(5, 70)
pixel_graph(30, 30)
woaw_beautiful(100, 100)