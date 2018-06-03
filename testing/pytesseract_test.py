import pytesseract
import cv2
import os
from PIL import Image

"""Note:
    When installing tesseract ensure several things:
    -- pip install pytesseract
    -- Install tesseract from: https://github.com/UB-Mannheim/tesseract/wiki (use 3.05 stable)
    -- System variable path contains parent tesseract directory
    -- Create new environment variable called TESSDATA_PREFIX and point it to the parent tesseract directory
"""
# can change path to image to scan for text
image = cv2.imread("colour_of_magic.png", 0)

thresholding = input("Please enter the thresholding method to use: thresh or blur\n")

if thresholding is "thresh":
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif thresholding is "blur":
    image = cv2.medianBlur(image, 3)

filename = "pytesseract_output.png"
cv2.imwrite(filename, image)
# gets the text from the tesseract model
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
# TODO: write to a file with timestamp?
print(text)
# can remove if not required, for testing
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()