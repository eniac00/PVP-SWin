#!/usr/bin/env python3

from PIL import Image, ImageDraw
from itertools import combinations_with_replacement
import random

# this function takes in a sequence and color code for each combination
# and  makes a image using that color code dictionary and saves its with the given name
# for example: sequence -> "ATG" will follow as below
#  A T G
# A
# T
# G
# @param imageWidth {Integer} -> desired images width
# @param imageHeight {Integer} -> desired images height
# @param seqColoCode {Dictionary} -> dictionary containing possible combination and respective color code(RGB)
#                                    for example: { "AT": (255, 0, 255), "AG": (255, 0, 0) }
# @param seq {String} -> sequence as a string
# @param imgName {String} -> image name to be saved with


def Sequence_to_Image(imageWidth, imageHeight, seqColoCode, sequence, imgName):

    # Create a blank image with white background
    image = Image.new("RGB", (imageWidth, imageHeight), "white")
    draw = ImageDraw.Draw(image)

    # Define the dimensions of the matrix
    matrix_size = len(sequence)
    cell_width = imageWidth // matrix_size
    cell_height = imageHeight // matrix_size


    # Draw the matrix
    for i in range(matrix_size):
        for j in range(matrix_size):
            # Define the coordinates of the current cell
            string = sequence[j]+sequence[i]
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            if string in seqColoCode.keys():
                draw.rectangle([x1, y1, x2, y2], fill=seqColoCode[string])
            else:
                string = string[::-1]

                if string in seqColoCode.keys():
                    draw.rectangle([x1, y1, x2, y2], fill=seqColoCode[string])
                else:   # if after reversing the string and key still couldnot be found
                        # then use default (0, 0, 0)
                    draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0))

    # Save the image as a file
    image.save("./" + imgName + ".png")


# This function is being used by the function 'Color_Code_Generator_Stable'
# @param i {Integer} a integer value that will be used to generate a RGB value
# @return {Tuple} containing (R, G, B) color code

def Generate_Sequential_Color(i):
    r = (i // 16) % 16 * 16
    g = (i // 4) % 16 * 16
    b = i % 16 * 16
    return r, g, b


# Used for generating stable color code that will not change (every execution will remain same)
# @param amino_acids {List} amino_acids name (e.g. A, T, G e.t.c)
#                           makes combination using 2 amino acids at a time with replacement means "AA", "TT" is also a valid option
# @return {Dictionary} dictionary containg the color code of each combination

def Color_Code_Generator_Stable(amino_acids):

    comb = combinations_with_replacement(amino_acids, 2)
    seq_list = []
    colors = set()

    for i in list(comb):
        seq_list.append(''.join(map(str, i)))

    cnt = 0

    while len(colors) < len(seq_list):
        color = Generate_Sequential_Color(cnt*13)

        if (color == (0, 0, 0)):
            pass
        else:
            colors.add(color)

        cnt += 1

    colors = list(colors)
    color_code = dict(zip(seq_list, colors))

    return color_code


# Used for generating unstable color code that will change in every execution (cause, Random Number)
# @param amino_acids {List} amino_acids name (e.g. A, T, G e.t.c)
#                           makes combination using 2 amino acids at a time with replacement means "AA", "TT" is also a valid option
# @return {Dictionary} dictionary containg the color code of each combination

def Color_Code_Generator_Unstable(amino_acids):

    comb = combinations_with_replacement(amino_acids, 2)
    seq_list = []
    colors = set()

    for i in list(comb):
        seq_list.append(''.join(map(str, i)))

    while len(colors) < len(seq_list):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        color = r, g, b

        if (color == (0, 0, 0)):
            pass
        else:
            colors.add(color)

    colors = list(colors)

    color_code = dict(zip(seq_list, colors))

    return color_code


# Driver of the previous functions or the main entry point
# @param imageWidth {Integer} -> desired images width
# @param imageHeight {Integer} -> desired images height
# @param seq {String} -> sequence as a string
# @param imgName {String} -> image name to be saved with

def Image_Generator(imageWidth, imageHeight, sequence, imgName):
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    color_code = Color_Code_Generator_Stable(amino_acids)
    Sequence_to_Image(imageWidth, imageHeight, color_code, sequence, imgName)

