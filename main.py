# learning python while trying to solve a task: https://adventofcode.com/2024/day/4

import sys

#define input 2D array of chars
# Easy array [4 entries]
# ARRAY = [
#     ['.', '.', 'X', '.', '.', '.'],
#     ['X', 'S', 'A', 'M', 'X', '.'],
#     ['.', 'A', '.', '.', 'A', '.'],
#     ['X', 'M', 'A', 'S', '.', 'S'],
#     ['.', 'X', '.', '.', '.', '.']
# ]


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

# number of rows
NUM_ROWS = len(ARRAY)
#Presume that inputs are same lenght. Find how many columns in array
NUM_COLS = len(ARRAY[0])

#define what we are looking for in the array
KEY = 'XMAS'
REV_KEY = KEY[::-1] # reverse key we are looking for

NUM_DIAGONALS = NUM_ROWS + NUM_COLS - 1
print(f"Array rows: {NUM_ROWS}, columns {NUM_COLS}, diagonals: {NUM_DIAGONALS}")

# print same as input
print ("Input array is: ")
for line in ARRAY:
    print(line)
#str_to_check = "XMASXMASXXMMAASS"
#print (str_to_check.count(KEY))

def count_matches(key: str, str_to_check: str) -> int:
    if len(str_to_check) < len(key):
        return 0
    # print(f"Found {key}, {str_to_check} times in row:#{str_to_check.count(key)}")
    return str_to_check.count(key)

# loop through lines to look for matching string (lines do not need reversing [reversing it had funny consequences :D])
def search_by_line() -> int:
    found_lines: int = 0
    for index, line in enumerate(ARRAY):
        string: str = ''.join(line)
        count_in_single_line = count_matches(KEY, string)
        count_in_single_line += count_matches(REV_KEY, string)
        if count_in_single_line > 0:
            found_lines += count_in_single_line
            print(f"Found {KEY}, {count_in_single_line} times in row:#{index} {line}")
    return found_lines

# extract wanted column as string
# input: index of column, note must be between 0 and NUM_COLS, otherwise exception will be raised
def get_vertical_line(index: int) -> str:
    if index > NUM_COLS or index < 0:
        raise Exception(f"Unexpected column index passed: {index}, current array contains only: {NUM_COLS}")
    vertical_line: str = ''
    for line in ARRAY:
        vertical_line += line[index]

    return vertical_line

# loop through columns and search for key provided
def search_by_column() -> int:
    found_lines: int = 0
    for index in range(NUM_COLS):
        col = get_vertical_line(index)
        count_in_single_column = count_matches(KEY, col)
        count_in_single_column += count_matches(REV_KEY, col)
        if count_in_single_column > 0:
            found_lines += count_in_single_column
            print(f"Found {KEY}, {count_in_single_column} times in column:#{index} {col}")
    return found_lines

# find string by diagonal index right to left.
def find_diag_line_right_to_left(index: int) -> str:
    if index > NUM_DIAGONALS:
        raise Exception(f"Diagonal index passed: {index}, current array contains only {NUM_DIAGONALS} diagonal lines")
    line = ''
    INITIAL_INDEX_OUT_OF_BOUNDS: bool = index < NUM_COLS
    # for first indexes look for 0...n column while looping through
    for row_i, row in enumerate(ARRAY):
        if index < NUM_COLS:
            line += row[index]
            index += 1
        # if original index was lower than number of columns that means we are doen iterating and will not continue
        # otherwise we will start needlessly adding more chars after bellow logic manipulates the index
        # (applies mostly to larger arrays)
        elif INITIAL_INDEX_OUT_OF_BOUNDS:
            break
        # clear index. This is breaking point where on next row we start reading the line.
        # Initial '0' position was read (when index = was provided so we skip it) already so we will start
        # building the string on next iteration
        elif index == NUM_COLS:
            index = 0
        else: # skip this row, decrement index
            index -= 1
    return line


# find string by diagonal index right to left.
def find_diag_line_left_to_right(index: int) -> str:
    if index > NUM_DIAGONALS:
        raise Exception(f"Diagonal index passed: {index}, current array contains only {NUM_DIAGONALS} diagonal lines")
    line = ''
    # for first indexes look for 0...n column while looping through rows, moving to the left
    # after index goes over NUM_COLS we still loop through rows without accessing column element until it is decremented to "possible" value
    #print(f"start index: {index}")
    for row_i, row in enumerate(ARRAY):
        if index < 0:  # done we cannot move left anymore
            break
        if index >= NUM_COLS:  # skip, index is too far right
            # we decrement index and go one row down next iteration, maybe index will be valid then
            index -= 1 # decrement so we move left within next row
            continue
        line += row[index]
        #print(f"diag: row_i{row_i} {index}: {row[index]} new line: {line}")
        index -= 1  # decrement so we move left within next row
    return line

# loop through columns and search for KEY & REV_KEY
# Return number of times KEY & REV_KEY were counted
def search_diagonally() -> int:
    found_lines: int = 0
    for i in range(NUM_DIAGONALS):
        diagonal_line_r2l = find_diag_line_right_to_left(i)
        diag_count = count_matches(KEY, diagonal_line_r2l)
        diag_count += count_matches(REV_KEY, diagonal_line_r2l)
        if diag_count > 0:
            found_lines += diag_count
            print(f"Found {KEY}, {diag_count} times  in diagonal line, direction right to left, index# {i}: {diagonal_line_r2l}")

        diagonal_line_l2r = find_diag_line_left_to_right(i)
        diag_count = count_matches(KEY, diagonal_line_l2r)
        diag_count += count_matches(REV_KEY, diagonal_line_l2r)
        if diag_count > 0:
            found_lines += diag_count
            print(f"Found {KEY}, {diag_count} times  in diagonal line, direction left to right, index# {i}: {diagonal_line_l2r}")
    return found_lines

# call functions to look for KEY & REV_KEY in ARRAY
def search_array() -> None:
    total_findings: int = 0
    total_findings+= search_by_line()

    total_findings+= search_by_column()

    total_findings+= search_diagonally()

    print(f"Little Elf found {KEY} in provided puzzle {total_findings} times!")

search_array()









# outdated implementations that were optimized

def find_diag_line_left_to_right_outdated(index: int) -> str:
    if index > NUM_DIAGONALS:
        raise Exception(f"Diagonal index passed: {index}, current array contains only {NUM_DIAGONALS} diagonal lines")
    line = ''
    # for first indexes look for 0...n column while looping through
    if index < NUM_COLS:
        for row in ARRAY:
            if  index < 0: # done we cannot move left anymore
                break
            if NUM_COLS > index > -1:
                line += row[index]
            index -= 1 #decrement so we move left within next row
    else :
        row_i = index - NUM_ROWS
        #print(f"START_ROW original index {index}-{NUM_ROWS}={row_i}")
        for col_i in range(NUM_COLS-1, -1, -1):# increment in reverse so we continue to move to the right in the next row
            if  row_i >= NUM_ROWS:
                break
            line+= get_vertical_line(col_i)[row_i]
            row_i += 1 # increment so we move down to take next element
    print(f"return {line}")
    return line

# find string by diagonal index right to left.
def find_diag_line_right_to_left_outdated(index: int) -> str:
    if index > NUM_DIAGONALS:
        raise Exception(f"Diagonal index passed: {index}, current array contains only {NUM_DIAGONALS} diagonal lines")
    line = ''
    print(f"index {index}")
    # for first indexes look for 0...n column while looping through
    if index < NUM_COLS:
        for row_i, row in enumerate(ARRAY):
            print(f"checking  col: {index} row:{row_i}")
            if index < NUM_COLS:
                line += row[index]
            index += 1
    else :
        row_i = index - NUM_ROWS
        for col_i in range(NUM_ROWS):
            print(f"checking  col: {col_i} row:{row_i}")
            if col_i > NUM_COLS or row_i >= NUM_ROWS:
                continue
            line+= get_vertical_line(col_i)[row_i]
            row_i -= 1 # increment so we continue to move to the right in the next row
    print(f"return {line}")

    return line