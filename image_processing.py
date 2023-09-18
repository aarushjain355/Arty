import cv2
import numpy as np
import matplotlib.pyplot as plt

def read_file_name(file_name):

    img = cv2.imread(file_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


#create edge mask
def edge_mask(img, line_size, blur_value):

    # Input : GrayScale Image 
    # Output : Edges of Images
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)

    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges



## reduce color palate

def color_quantization(img, k):

    # Transform the image
    data = np.float32(img).reshape((-1, 3))
     # Determine Criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.01)
    # Implementing K-means
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    results = center[label.flatten()]
    result = results.reshape(img.shape)
    return result



# combine edge mask with quantiz img

def cartoon(blurred, edges, num):
    c = cv2.bitwise_and(blurred, blurred, mask=edges)
    c_rgb = cv2.cvtColor(c, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f"Image{num}.jpg", c_rgb)
    


def process_image(file_name, num):

    file_name = file_name
    img = read_file_name(file_name)

    line_size, blur_value = 7,7
    edges = edge_mask(img, line_size, blur_value)

    img = color_quantization(img, k=9)


    ## reduce noise

    blurred = cv2.bilateralFilter(img, d=3, sigmaColor=200, sigmaSpace=200)

    cartoon(blurred, edges, num)

