# learning python while trying to solve a task: https://adventofcode.com/2024/day/4

#define input 2D array of chars
# Harder input with 9 Matches
# ARRAY = [
#     ['M', 'M', 'M', 'S', 'X', 'X', 'M', 'A', 'S', 'M'],
#     ['M', 'S', 'A', 'M', 'X', 'M', 'S', 'M', 'S', 'A'],
#     ['A', 'M', 'X', 'S', 'X', 'M', 'A', 'A', 'M', 'M'],
#     ['M', 'S', 'A', 'M', 'A', 'S', 'M', 'S', 'M', 'X'],
#     ['X', 'M', 'A', 'S', 'A', 'M', 'X', 'A', 'M', 'M'],
#     ['X', 'X', 'A', 'M', 'M', 'X', 'X', 'A', 'M', 'A'],
#     ['S', 'M', 'S', 'M', 'S', 'A', 'S', 'X', 'S', 'S'],
#     ['S', 'A', 'X', 'A', 'M', 'A', 'S', 'A', 'A', 'A'],
#     ['M', 'A', 'M', 'M', 'M', 'X', 'M', 'M', 'M', 'M'],
#     ['M', 'X', 'M', 'X', 'A', 'X', 'M', 'A', 'S', 'X']
# ]
#Input from file. Answer 1960 was correct
with open("input.txt", "r") as file:
    ARRAY = [list(line.strip()) for line in file]

# number of rows
NUM_ROWS = len(ARRAY)
#Presume that inputs are same lenght. Find how many columns in array
NUM_COLS = len(ARRAY[0])

#define what we are looking for in the array
KEY = 'MAS'
REV_KEY = KEY[::-1] # reverse key we are looking for
DOT = '.'
print(f"Array rows: {NUM_ROWS}, columns {NUM_COLS}")
# print same as input
print ("Input array is: ")
for line in ARRAY:
    print(line)

# Check if position is a valid one
def is_valid_pos(pos_x: int, pos_y: int) -> bool:
    return pos_x in range(NUM_ROWS) and pos_y in range(NUM_COLS)

# Check if position is surrounded by a required range of cells in all directions
def is_position_surrounded(pos_x: int, pos_y: int, surrounding_range: int) -> bool:
    for x in range(pos_x - surrounding_range, pos_x + surrounding_range + 1):
        for y in range(pos_y - surrounding_range, pos_y + surrounding_range + 1):
            if is_valid_pos(x, y):
                continue
            return False
    return True

# check if given position is in the middle of proper star
def is_middle_of_a_star(position_x: int, position_y: int) -> bool:
    # start with position, the middle letter cannot be in border position which we need for testing
    if not is_position_surrounded(position_x, position_y, 1):
        return False

    # now create 2 diagonal words in different directions
    left_to_right = ARRAY[position_x - 1][position_y - 1]
    left_to_right += ARRAY[position_x][position_y]
    left_to_right += ARRAY[position_x + 1][position_y + 1]

    right_to_left = ARRAY[position_x - 1][position_y + 1]
    right_to_left += ARRAY[position_x][position_y]
    right_to_left += ARRAY[position_x + 1][position_y - 1]

    #Check that diagonal words match key or reverse key
    for word in [left_to_right, right_to_left]:
        if word == KEY or word == REV_KEY:
            continue
        return False
    # letter is in the middle of an actual start that matches all requirements
    return True

number_of_stars = 0
# try cleaning up substrings, throwing out impossible chars
for row_i in range(NUM_ROWS):
    for col_i in range(NUM_COLS):
        number_of_stars += is_middle_of_a_star(row_i, col_i)
print(f"Little Elf found {KEY} stars in provided puzzle {number_of_stars} times!")
