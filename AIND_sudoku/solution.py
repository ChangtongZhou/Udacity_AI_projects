assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    # pass

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
reversed_cols = cols[::-1]

# Make diagonal units
dl_units = [[rows[i]+cols[i] for i in range(len(rows))]]
dr_units = [[rows[i]+reversed_cols[i] for i in range(len(rows))]]
unitlist = row_units + col_units + square_units + dl_units + dr_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Version 1
    # potential  twins
    possible_twins = [box for box in values.keys() if len(values[box]) == 2]

    # Naked twins who are peers
    naked_twins = [[box1, box2] for box1 in possible_twins for box2 in peers[box1] \
                    if set(values[box1]) == set(values[box2])]

    for i in range(len(naked_twins)):
        # Get a pair of naked_twins
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        # check peers that are both in peers1 and peers2
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_intersect = peers1 & peers2
        # Delete the two digits in naked twins from all common peers.
        for peer in peers_intersect:
            # Get the 2 number value from the naked twins
            twin_val = values[box1]
            trans = str.maketrans("", "", twin_val)
            if len(values[peer]) > 1:
                values = assign_value(values, peer, values[peer].translate(trans))
    return values


    # Version 2
    # for nt in naked_twins:
    #     # Find the units that contains these two naked twins
    #     the_unit = [u for u in unitlist if nt[0] in u and nt[1] in u]
    #     for unit in the_unit:
    #         twin_val = values[nt[0]]
    #         trans = str.maketrans("", "", twin_val)
    #         for box in unit:
    #             # if the box is not one of the naked twins from the unit
    #             if box != nt[0] and box != nt[1] and len(values[box]) > 2:
    #                 values[box] = values[box].translate(trans)
    #     if len([box for box in values.keys() if len(values[box]) == 0]):
    #         return False
    #
    # return values
        # For each pair of naked twins,



def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    res = dict(zip(boxes, grid))

    for key, value in res.items():
        # print (value)
        if value == '.':
            res[key] = '123456789'

    return res


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # pass
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

    # pass

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    # pass

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked_twins
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    # pass


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    # pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid = grid_values(grid)
    # values = search(values)
    return search(grid)
    # return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'

    # values = grid_values(diag_sudoku_grid)
    # display(values)
    # print(values)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
