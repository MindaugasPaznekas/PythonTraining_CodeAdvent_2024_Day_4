# learning python while trying to solve a task: https://adventofcode.com/2024/day/4
from tarfile import LENGTH_LINK

#define input 2D array of chars
# Easy array [4 entries]
# ARRAY = [
#     ['.', '.', 'X', '.', '.', '.'],
#     ['X', 'S', 'A', 'M', 'X', '.'],
#     ['.', 'A', '.', '.', 'A', '.'],
#     ['X', 'M', 'A', 'S', '.', 'S'],
#     ['.', 'X', '.', '.', '.', '.']
# ]
# Harder input with 18 Matches
ARRAY = [
    ['M', 'M', 'M', 'S', 'X', 'X', 'M', 'A', 'S', 'M'],
    ['M', 'S', 'A', 'M', 'X', 'M', 'S', 'M', 'S', 'A'],
    ['A', 'M', 'X', 'S', 'X', 'M', 'A', 'A', 'M', 'M'],
    ['M', 'S', 'A', 'M', 'A', 'S', 'M', 'S', 'M', 'X'],
    ['X', 'M', 'A', 'S', 'A', 'M', 'X', 'A', 'M', 'M'],
    ['X', 'X', 'A', 'M', 'M', 'X', 'X', 'A', 'M', 'A'],
    ['S', 'M', 'S', 'M', 'S', 'A', 'S', 'X', 'S', 'S'],
    ['S', 'A', 'X', 'A', 'M', 'A', 'S', 'A', 'A', 'A'],
    ['M', 'A', 'M', 'M', 'M', 'X', 'M', 'M', 'M', 'M'],
    ['M', 'X', 'M', 'X', 'A', 'X', 'M', 'A', 'S', 'X']
]
#Input from file. Answer 2517 was correct
# with open("input.txt", "r") as file:
#     ARRAY = [list(line.strip()) for line in file]

# number of rows
NUM_ROWS = len(ARRAY)
#Presume that inputs are same lenght. Find how many columns in array
NUM_COLS = len(ARRAY[0])

#define what we are looking for in the array
KEY = 'MAS'
REV_KEY = KEY[::-1] # reverse key we are looking for

NUM_DIAGONALS = NUM_ROWS + NUM_COLS - 1
print(f"Array rows: {NUM_ROWS}, columns {NUM_COLS}, diagonals: {NUM_DIAGONALS}")

# print same as input
print ("Input array is: ")
for line in ARRAY:
    print(line)

output = ARRAY
WANTED_CHARS = list(KEY)
DOT = '.'

X_MAS = [
    [ # combination 0
        [KEY[0], DOT, KEY[0]],
        [DOT, KEY[1], DOT],
        [KEY[2], DOT, KEY[2]],
    ],
    [  # combination 1
        [KEY[0], DOT, KEY[2]],
        [DOT, KEY[1], DOT],
        [KEY[0], DOT, KEY[2]],
    ],
    [  # combination 2
        [KEY[2], DOT, KEY[0]],
        [DOT, KEY[1], DOT],
        [KEY[2], DOT, KEY[0]],
    ],
    [  # combination 3
        [KEY[2], DOT, KEY[2]],
        [DOT, KEY[1], DOT],
        [KEY[0], DOT, KEY[0]],
    ]
]

NUM_PATTERNS = len(X_MAS)
NUM_PATTERN_ROWS = len(X_MAS[0])
NUM_PATTERN_COLS = len(X_MAS[0][0])

for i, array in enumerate(X_MAS):
    print(f"Pattern # {i}")
    for line in array:
        print(line)

# replace unwanted characters with '.' to prepare array for further processing
def replace_unwanted() -> None:
    for row_i, line in enumerate(output):
        for char_i, char in enumerate(line):
            if char not in WANTED_CHARS:
                output[row_i][char_i] = DOT
                #print(f"Found {char} not in {WANTED_CHARS} remove R:C{row_i} {char_i}")

replace_unwanted()

def array_builder(start_row: int, start_col: int, input_arr: []) -> []:
    # TODO out of bounds check
    array = []
    for row_num in range(NUM_PATTERN_ROWS):
        array.append(input_arr[start_row + row_num][start_col: start_col + NUM_PATTERN_COLS])
    print(f"array constructed: {start_row}-{start_row+2}:{start_col}-{start_col + NUM_PATTERN_COLS}")
    for line in array:
        print(line)
    return array
print ("-----------")

def single_pattern_matcher(pattern: [], array: []) -> bool:
    if len(pattern) != len(array) or len(pattern[0]) != len(array[0]):
        raise Exception(f"Arrays provided do not match in dimensions {len(pattern)} != {len(array)}  or {len(pattern[0])} != {len(array[0])}")
    for row_i, row in enumerate(pattern):
        for char_i, char in enumerate(row):
            if char == DOT:
                continue # for now let's continue
            if char != array[row_i][char_i]:
                return False
    return True

def test_all_patterns(array: []) -> bool:
    for pattern_index, pattern_array in enumerate(X_MAS):
        if single_pattern_matcher(pattern_array, array):
            return True

    return False

def is_possible_star(pos_x, pos_y) -> bool:
    if output[pos_x][pos_y] == DOT:
        return False

    # build all variations of array's from this location
    # print(f"@@ {pos_x}:{pos_y}, from : {pos_x - NUM_PATTERN_ROWS + 1}:{pos_x + NUM_PATTERN_ROWS}")
    # print(f"@@ {pos_x}:{pos_y}, from : {pos_y - NUM_PATTERN_ROWS + 1}:{pos_y + NUM_PATTERN_ROWS}")

    for try_x in range(pos_x - NUM_PATTERN_ROWS + 1, pos_x + NUM_PATTERN_ROWS):
        for try_y in range(pos_y - NUM_PATTERN_COLS + 1, pos_y + NUM_PATTERN_COLS):
            if try_x < 0 or try_x >= NUM_ROWS or try_y < 0 or try_y >= NUM_COLS: # check bounds
                continue
            print(f"position to try {pos_x}:{pos_y}, test now: {try_x}:{try_y} - actual test now:")
            segment = array_builder(try_x if try_x <= (NUM_ROWS - NUM_PATTERN_ROWS) else NUM_ROWS - NUM_PATTERN_ROWS,
                                    try_y if try_y <= (NUM_COLS - NUM_PATTERN_COLS) else NUM_COLS - NUM_PATTERN_COLS,
                                    output)
            if test_all_patterns(segment):
                print (f"found match in position {pos_x}:{pos_y}")
                return True
    return False

# try cleaning up substrings, throwing out impossible chars
for row_i in range(NUM_ROWS):
    for col_i in range(NUM_COLS):
        if not is_possible_star(row_i, col_i):
            output[row_i][col_i] = DOT


# print same as input
print ("Output array is: ")
for line in output:
    print(line)