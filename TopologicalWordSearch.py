#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d
import math
import random
import numpy as np
import pi3d.util.Screenshot
import sys
# ************** VISIBILITY CHECK FUNCTIONS ************************ #

# check if each tower is visible from the "left"
def checkLeft(heightMap,visible_map):
    # Check Left side (top left to bottom right)
    for i in range(heightMap.shape[0]):  # rows
        tallest_tower = 0  # current tallest tower height in row
        for j in range(heightMap.shape[1]): # cols
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if(heightMap[i][j] > tallest_tower+2):
                tallest_tower = heightMap[i][j]
                visible_map[i][j] = True
    return heightMap,visible_map

# check if a tower is visible
def checkLeftAt(heightMap,visible_map,i,j):
    # assert that J is within range
    if j < heightMap.shape[1]:
        tallest_tower = 0  # current tallest tower height in row
        for idx in range(0,j+1):  # cols, un
            curr_tower = heightMap[i][idx]
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if (curr_tower > tallest_tower+2):
                tallest_tower = curr_tower
                visible_map[i][idx] = True
                # if the tower at given index is taller than tallest tower then it is visible
                if idx == j:
                    return True

# check if each tower is visible from the "right"
def checkRight(heightMap,visible_map):
    # Check right side (top right to bottom left)
    for i in range(heightMap.shape[0]): # rows
        tallest_tower = 0  # current tallest tower height in row
        for j in range(heightMap.shape[1]-1,-1,-1): # cols
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if(heightMap[i][j] > tallest_tower+2):
                tallest_tower = heightMap[i][j]
                visible_map[i][j] = True
    return heightMap,visible_map

# check if a tower is visible
def checkRightAt(heightMap,visible_map,i,j):
    # assert that J is within range
    if j < heightMap.shape[1]:
        tallest_tower = 0  # current tallest tower height in row
        for idx in range(heightMap.shape[1]-1,j-1,-1):  # cols, un
            curr_tower = heightMap[i][idx]
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if (curr_tower > tallest_tower+2):
                tallest_tower = curr_tower
                visible_map[i][idx] = True
                # if the tower at given index is taller than tallest tower then it is visible
                if idx == j:
                    return True

# check if each tower is visible from the "bottom"
def checkBottom(heightMap, visible_map):
    # Check bottom side (bottom right to top left)
    for j in range(heightMap.shape[1]-1,-1,-1): # cols
        tallest_tower = 0  # current tallest tower height in row
        for i in range(heightMap.shape[0]-1,-1,-1): # rows
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if(heightMap[i][j] > tallest_tower+2):
                tallest_tower = heightMap[i][j]
                visible_map[i][j] = True
    return heightMap,visible_map

# check if a tower is visible
def checkBottomAt(heightMap,visible_map,i,j):
    # assert that J is within range
    if i < heightMap.shape[0]:
        tallest_tower = 0  # current tallest tower height in row
        for idx in range(heightMap.shape[0]-1,i-1,-1):  # cols, un
            curr_tower = heightMap[idx][j]
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if (curr_tower > tallest_tower+2):
                tallest_tower = curr_tower
                visible_map[idx][j] = True
                # if the tower at given index is taller than tallest tower then it is visible
                if idx == i:
                    return True

# check if each tower is visible from the "top"
def checkTop(heightMap, visible_map):
    # Check top side (bottom left to top right)
    for j in range(heightMap.shape[1]):  # cols
        tallest_tower = 0  # current tallest tower height in row
        for i in range(heightMap.shape[0]):  # rows
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if(heightMap[i][j] > tallest_tower+2):
                tallest_tower = heightMap[i][j]
                visible_map[i][j] = True
    return heightMap,visible_map

# check if a tower is visible
def checkTopAt(heightMap,visible_map,i,j):
    # assert that J is within range
    if i < heightMap.shape[0]:
        tallest_tower = 0  # current tallest tower height in row
        for idx in range(0,i+1):  # cols, un
            curr_tower = heightMap[idx][j]
            # if the current tower is taller than the tallest tower in the row, it is seeable
            if (curr_tower > tallest_tower+2):
                tallest_tower = curr_tower
                visible_map[idx][j] = True
                # if the tower at given index is taller than tallest tower then it is visible
                if idx == i:
                    return True

# check all sides to see if all towers are visible
def check_sides(heightMap,visible_map):
    heightMap, visible_map = checkTop(heightMap, visible_map)

    heightMap, visible_map = checkRight(heightMap, visible_map)

    heightMap, visible_map = checkBottom(heightMap, visible_map)

    heightMap, visible_map = checkLeft(heightMap, visible_map)
    return heightMap, visible_map

# check all sides to see if a towers are visible
def check_sides_At(heightMap,visible_map,i,j):
    if checkTopAt(heightMap, visible_map,i,j) or checkRightAt(heightMap, visible_map,i,j) or checkBottomAt(heightMap, visible_map,i,j) or checkLeftAt(heightMap, visible_map,i,j):
        return True
    return False


# ************** WORD CHECK FUNCTIONS ************************ #

# put a single word 'w' into the letter_matrix with 'right' direction and random position
def add_word_right(w,letter_matrix,N):
    w_length = len(w)  # len() function returns the length of the string w
    row = random.randint(0, N - 1)  # all starting rows are ok
    col = random.randint(0, N - w_length)  # since filling to right, starting col can't exceed the N-w_length
    # We need to check if (row,col) is good starting position
    # It is possible that some of the cells is already occupied by other words
    # To avoid making a single function over complicated, let's make another function to check this
    while can_add_word_right(letter_matrix,row, col, w) == False:  # keep trying to find new location if not ok
        row = random.randint(0, N - 1)  # all starting rows are ok
        col = random.randint(0, N - w_length)  # since filling to right, starting col can't exceed the N-w_length
    # at this point, (row,col) is a good candidate to fill in the letters
    for i in range(w_length):
        letter_matrix[row][col + i] = w[i]

# checks if we can add word 'w' with starting position (row,col). Return True or False
def can_add_word_right(letter_matrix,row, col, w):
    for i in range(len(w)):
        # It's okay if a cell is not set (still '?')
        # It's also okay a cell is set but it's set to the same letter as the i'th letter in the word w
        # This will allow words to overlap - a desirable effect
        if letter_matrix[row][col + i] != '?' and letter_matrix[row][col + i] != w[i]:  # not okay conditions
            return False
    return True  # not okay condition never happened, so return okay

# add a word left-right
def add_word_left(w,letter_matrix,N):
    w_length = len(w)
    row = random.randint(0, N - 1)
    col = random.randint(w_length - 1, N - 1)
    while can_add_word_left(letter_matrix,row, col, w) == False:
        row = random.randint(0, N - 1)
        col = random.randint(w_length - 1, N - 1)
    for i in range(w_length):
        letter_matrix[row][col - i] = w[i]

def can_add_word_left(letter_matrix,row, col, w):
    for i in range(len(w)):
        if letter_matrix[row][col - i] != '?' and letter_matrix[row][col - i] != w[i]:
            return False
    return True

#add a word bottom up
def add_word_up(w,letter_matrix,N):
    w_length = len(w)
    row = random.randint(0, N - w_length)
    col = random.randint(0, N - 1)
    while can_add_word_up(letter_matrix,row, col, w) == False:
        row = random.randint(0, N - w_length)
        col = random.randint(0, N - 1)
    for i in range(w_length):
        letter_matrix[row + i][col] = w[i]

def can_add_word_up(letter_matrix,row, col, w):
    for i in range(len(w)):
        if letter_matrix[row + i][col] != '?' and letter_matrix[row + i][col] != w[i]:
            return False
    return True

# Add a word top down
def add_word_down(w,letter_matrix,N):
    w_length = len(w)
    row = random.randint(w_length - 1, N - 1)
    col = random.randint(0, N - 1)
    while can_add_word_down(letter_matrix,row, col, w) == False:
        row = random.randint(w_length - 1, N - 1)
        col = random.randint(0, N - 1)
    for i in range(w_length):
        letter_matrix[row - i][col] = w[i]

def can_add_word_down(letter_matrix,row, col, w):
    for i in range(len(w)):
        if letter_matrix[row - i][col] != '?' and letter_matrix[row - i][col] != w[i]:
            return False
    return True

# ************** Letter Matrix FUNCTIONS ************************ #
# creates NxN letter matrix with all '?'s
def create_letter_matrix(N):
    letter_matrix = []
    for i in range(N): # rows
        letter_row = []
        for j in range(N): # cols
            letter_row.append('?') # Add '?' to the list
        letter_matrix.append(letter_row) # Add a row list to letter_matrix list
    return letter_matrix

# randomly put alphabet letters into cells that is still '?'
def randomize_empty_cells(letter_matrix,N):
    alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # put 26 letters in a string
    for i in range(N):
        for j in range(N):
            if letter_matrix[i][j] == '?': # this cell is still empty
                letter_matrix[i][j] = alphabets[random.randrange(26)] # pick up random index in alphabet string


# ************** Tower Sort FUNCTIONS ************************ #
# get the first half of an array in ascending order
def first_half_sort(arr, n):
    new_arr = []
    # sort a copy of the array
    temp = arr.copy()
    temp.sort()

    # printing first half in ascending
    # order
    for i in range(n // 2):
        new_arr.append(temp[i])

    # printing second half in original order
    for j in range(n-1, n // 2 - 1, -1):
        new_arr.append((arr[j]))
    return new_arr

# get second half of array in descensing order
def second_half_sort(arr,n):
    new_arr = []

    # get first half unsorted
    for i in range(n // 2):
        new_arr.append(arr[i])

    arr.sort()
    # printing second half in descending
    # order
    for j in range(n - 1, n // 2 - 1, -1):
        new_arr.append(arr[j])
    return new_arr

# sort only half the array based on invisible towers
def mid_sort(heightMap,visible_map):
    falsehoods = np.where(~visible_map)
    if (falsehoods.__len__() > 1):
        if falsehoods[0].size > 0 and falsehoods[1].size > 0:
            listOfCoordinates = list(zip(falsehoods[0], falsehoods[1]))
            for coords in listOfCoordinates:
                i=coords[0]
                j=coords[1]
                face = random.randint(0,3)
                if face == 0:
                    # if the unseen tower is in the second half of the row, do second half sort
                    if j > heightMap.shape[0] / 2:
                        heightMap[i] = second_half_sort(heightMap[i], heightMap.shape[0])
                    else:
                        heightMap[i] = first_half_sort(heightMap[i], heightMap.shape[0])
                if face == 1:
                    # if the unseen tower is in the second half of the row, do second half sort
                    if j < heightMap.shape[0] / 2:
                        heightMap[i] = second_half_sort(heightMap[i], heightMap.shape[0])
                    else:
                        heightMap[i] = first_half_sort(heightMap[i], heightMap.shape[0])
                if face == 2:
                    # if the unseen tower is in the second half of the row, do second half sort
                    if i > heightMap.shape[1] / 2:
                        heightMap.T[j] = second_half_sort(heightMap.T[j], heightMap.shape[0])
                    else:
                        heightMap.T[j] = first_half_sort(heightMap.T[j], heightMap.shape[0])
                else:
                    # if the unseen tower is in the second half of the row, do second half sort
                    if i < heightMap.shape[1] / 2:
                        heightMap.T[j] = second_half_sort(heightMap.T[j], heightMap.shape[0])
                    else:
                        heightMap.T[j] = first_half_sort(heightMap.T[j], heightMap.shape[0])

    return heightMap, visible_map

# ************** Height Map Functions FUNCTIONS ************************ #
# To gen a height map We can either
# Generate each tower with a RANDOM height
# Generate each tower with a UNIQUE height
def gen_heightMap(N=7):
    heightMap = np.zeros(shape=(N,N))
    for i in range(N):  # rows
        for j in range(N):  # cols
            height = random.randrange(2,N)  # gen a random height
            heightMap[i][j] = height  # set height
    return check_heightMap(heightMap)

# increment each unsee - able tower height by one until it is visible
def update_falsehoods(heightMap, visible_map):
    falsehoods = np.where(~visible_map)
    if(falsehoods.__len__() > 1):
        if falsehoods[0].size > 0 and falsehoods[1].size > 0:
            listOfCoordinates = list(zip(falsehoods[0], falsehoods[1]))
            for coords in listOfCoordinates:
                i=coords[0]
                j=coords[1]
                heightMap[i][j] += 1
                while not visible_map[i][j]:
                    if check_sides_At(heightMap, visible_map, i, j):
                        break
                    else:
                        heightMap[i][j] += 1

    return heightMap, visible_map



# checking if all cubes in height map are visible
def check_heightMap(heightMap,visible_map=None):
    if visible_map is None:
        # a map to consider which a tower is visible or not
        visible_map = np.zeros(shape=heightMap.shape,dtype=bool)

    # check if all towers are visible from each side
    # this could also be done via flips and transpositions if you wanted to be fancy
    heightMap, visible_map = check_sides(heightMap, visible_map)

    # if not all towers are immediately visible
    if not np.all(visible_map is True):
        # sort towers from the middle
        heightMap, visible_map = mid_sort(heightMap, visible_map)
        # we reset the visible map because we dont keep track of the sorting indices
        visible_map = np.zeros(shape=heightMap.shape, dtype=bool)
        heightMap, visible_map = check_sides(heightMap, visible_map)

    # midsort will not solve the problem of having multiple towers with the same height
    # happens if the heights are not unique

    # to solve this we will grab all non visible towers, and increment them by one individually until seen

    while not np.all(visible_map):
        # Update falsehoods by increasing neighbor size by 1 (this gives the towers some nice height in the center)
        heightMap, visible_map = update_falsehoods(heightMap, visible_map)
        visible_map = np.zeros(shape=heightMap.shape, dtype=bool)
        # check if everything is visible
        heightMap, visible_map = check_sides(heightMap, visible_map)
        # print(visible_map)

    # this should be an matrix of all True values
    print(visible_map)
    print(heightMap)

    return heightMap


# ************** Cube Map Functions FUNCTIONS ************************ #
def draw_cubeMap(cubeMap,heightMap,N=7):
    z = -N/2 # starts here to account for offset
    for i in range(N): # rows
        cube_row = []
        x = -N/2  # starts here to account for offset

        for j in range(N):  # cols
            # 2*z, 2*x is for spacing between blocks
            # h is cut in half to make it look smaller
            # y is cut in 4 because y grows from cube mid point, so it needs to be h/2
            cube = pi3d.Cuboid(x=2*x, y=heightMap[i][j]/4, z=2 * z, h=heightMap[i][j]/2)

            cube_row.append(cube)  # Add cube to the list
            x += 1

        cubeMap.append(cube_row)  # Add a row list to letter_matrix list
        z += 1


# Function to demo the readlines() function
def readFile(fname):
    rd = open(fname, "r")
    # Read list of lines
    out = rd.readlines()
    # Close file
    rd.close()
    return out

def placeWords(fname,letter_matrix, N):
    listOfWords = readFile(fname)
    for line in listOfWords:
        content = line.strip()
        direction = random.randint(0, 4)
        if direction == 0:
            add_word_left(content, letter_matrix, N)
        elif direction == 1:
            add_word_right(content, letter_matrix, N)
        elif direction == 2:
            add_word_up(content, letter_matrix, N)
        else:
            add_word_down(content, letter_matrix, N)


def main(fname = "assets/dictionary/words", N = 12):
    # create display
    DISPLAY = pi3d.Display.create(background=(0.7, 0.3, 0.9, 1))

    # create camera and move it back a bit
    CAM = pi3d.Camera(at=(0.5,N/2,0.0),eye =(0.5,N/2,-2.5*N))

    letter_matrix = create_letter_matrix(N)

    cubeMap = []
    heightMap = gen_heightMap(N)
    draw_cubeMap(cubeMap,heightMap,N)


    # create keyboard listener
    keys = pi3d.Keyboard()


    # load shaders
    shader = pi3d.Shader("uv_bump")
    lshader = pi3d.Shader('uv_light')
    shinesh = pi3d.Shader("uv_reflect")
    matsh = pi3d.Shader("mat_reflect")

    #Place the words in the matrix
    placeWords(fname, letter_matrix, N)


    randomize_empty_cells(letter_matrix,N)
    print(letter_matrix)

    r = 0
    light = pi3d.Light(lightpos=(-3, -10, 5), lightcol=(0.5, 0.5, 0.5), lightamb=(0.5, 0.5, 0.5), is_point=False)
    # set cube details
    for i, cuberow in enumerate(cubeMap):
        for j, cube in enumerate(cuberow):
            string1 = pi3d.FixedString(camera=CAM, font="fonts/FreeSans.ttf", font_size=12,string=letter_matrix[i][j]+("\n"*int(math.ceil(cube.height))),
                                       color="#FFFFFF", justify="C",
                                       f_type="SMOOTH",background_color="#000000")  # EMBOSS, CONTOUR, BLUR, SMOOTH, BUMP
            cube.set_draw_details(lshader, [string1], 1.0)
            cube.set_light(light,0)



    # display loop
    try:

        while DISPLAY.loop_running():
            CAM.relocate(rot=r,distance=[-5,-5,-5])

            #draw loop
            for cuberow in cubeMap:
                for cube in cuberow:
                    cube.draw()

            r += 1

            #only do one rotation
            if r == 360:
                break

            # take a screenshot every 90 degree rotation
            if r % 90 == 0:
                pi3d.util.Screenshot.screenshot("screen_" + str(r) + ".png")

            # handle escape
            if keys.read() == 27:
                break

    finally:  # can also except KeyboardInterrup: for ctrl c specific things
        keys.close()
        DISPLAY.destroy()


if __name__ == '__main__':
    print("Running...")
    if len(sys.argv) < 3:
        main()
    else:
        main(fname=sys.argv[1], N=sys.argv[2])