import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

def orient_vertical(img):
    width = img.shape[1]
    height = img.shape[0]  # Fix the typo here (height should be img.shape[0])
    if width > height:
        img = imutils.rotate(img, angle=270)

    return img

def sharpen_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    dilated = cv2.dilate(blurred, rectKernel, iterations=2)
    edged = cv2.Canny(dilated, 75, 200, apertureSize=3)
    return edged

def binarize(img, threshold):
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(binary, rectKernel, iterations=2)
    return dilated

def find_receipt_bounding_box(binary, img):
    contours, hierarchy = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,  # Use RETR_EXTERNAL to get only outer contours
        cv2.CHAIN_APPROX_SIMPLE
    )
    largest_cnt = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_cnt)
    box = np.intp(cv2.boxPoints(rect))
    boxed = cv2.drawContours(img.copy(), [box], 0, (0, 255, 0), 20)
    return boxed, largest_cnt, rect

def find_tilt_angle(rect):
    angle = rect[2]
    print("Angle_0 = ", round(angle, 1))

    if angle < -45:
        angle += 90
        print("Angle_1:", round(angle, 1))
    else:
        uniform_angle = abs(angle)
    print("Uniform angle = ", round(uniform_angle, 1))

    return rect, uniform_angle

def adjust_tilt(img, angle):
    if angle >= 5 and angle < 80:
        rotated_angle = 0
    elif angle < 5:
        rotated_angle = angle
    else:
        rotated_angle = 270+angle

    tilt_adjusted = imutils.rotate(img, rotated_angle)
    delta = 360-rotated_angle
    return tilt_adjusted, delta


def crop(img, largest_contour):
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped = img[y:y+h, x:x+w]
    return cropped


def enhance_txt(img, binarization_threshold = 0.98):
    w = img.shape[1]
    h = img.shape[0]
    w1 = int(w*0.05)
    w2 = int(w*0.95)
    h1 = int(h*0.05)
    h2 = int(h*0.95)
    ROI = img[h1:h2, w1:w2]  # 95% of center of the image
    threshold = np.mean(ROI) * binarization_threshold  # % of average brightness

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (1, 1), 0)
    edged = 255 - cv2.Canny(blurred, 100, 150, apertureSize=7)

    thresh, binary = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
    return binary


raw_path = 'assets/Bbowl_03_20_22_2.jpg'
raw_img = cv2.imread(raw_path)

rotated = orient_vertical(raw_img)

edged = sharpen_edge(rotated)

threshold = 100
binarized = binarize(edged, threshold)

boxed, largest_cnt, rect = find_receipt_bounding_box(binarized, rotated)

rect, angle = find_tilt_angle(rect)

tilted, delta = adjust_tilt(boxed, angle)

cropped = crop(tilted, largest_cnt)

enhanced = enhance_txt(cropped, binarization_threshold=0.9)
enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)

adj_img = enhanced_rgb

plt.imshow(adj_img)
plt.show()


plt.imsave('enhanced.jpg', enhanced_rgb)