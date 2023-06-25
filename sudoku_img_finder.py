import cv2
from tensorflow import keras
import numpy as np
import imutils as im


"""Crops image to only have the board"""
def crop_image(img, boardCords, size=900):
    pts1 = np.float32([boardCords[0], boardCords[3], boardCords[1], boardCords[2]])
    pts2 = np.float32([[0, 0], [size, 0], [0, size], [size, size]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (size, size))
    return result


"""Finds the board in the image if there is one"""
def find_sudoku(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edges = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = im.grab_contours(keypoints)
    newImage = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)
    contours = sorted(contours, key=cv2.contourArea)
    contours.reverse()
    contours = contours[:10]
    boardCords = None
    for contour in contours:
        sidedShape = cv2.approxPolyDP(contour, 15, True)
        if len(sidedShape) == 4:
            boardCords = sidedShape
            break
    boardCropped = crop_image(img, boardCords)
    if boardCords is not None:
        print("Found Board in Image")
    else:
        raise Exception("No Board in Image or Not Found")
    return boardCropped, boardCords


"""Splits image into 81 images"""
def find_boxes(boardImg):
    rows = np.vsplit(boardImg, 9)
    boxes = []
    for ele in rows:
        cols = np.hsplit(ele, 9)
        for box in cols:
            box = cv2.resize(box, (48, 48)) / 255.0
            boxes.append(box)
    return boxes


def make_2d_array(original, m, n):
    res = [[0] * n for _ in range(m)]
    if len(original) != m * n:
        return []
    for i in range(m):
        for j in range(n):
            res[i][j] = original[i * n + j]
    return res


def print_grid(grid):
    for row in grid:
        print(row)


if __name__ == '__main__':
    from keras.models import load_model
    from solver import solve

    boardImg = cv2.imread("sudoku1.jpg")
    cv2.imshow("BEFORE", boardImg)
    boardCropped, boardCords = find_sudoku(boardImg)
    cv2.imwrite("board.jpg", boardCropped)
    boxes = find_boxes(cv2.cvtColor(boardCropped, cv2.COLOR_BGR2GRAY))
    model = load_model('model-OCR.h5')
    boxes = np.array(boxes).reshape(-1, 48, 48, 1)
    predicts = model.predict(boxes)
    numbers = [x for x in range(0, 10)]
    grid = []
    for labels in predicts:
        ind = np.argmax(labels)
        grid.append(ind)
    grid = make_2d_array(grid, 9, 9)
    print("Unsolved Grid:")
    print_grid(grid)
    solve(grid)
    print("Solved Grid:")
    print_grid(grid)

