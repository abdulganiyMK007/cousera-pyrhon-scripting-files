"""
Coursera Python Data Representation Project Week 4
"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    '''            
    Inputs:
        line1 - first single line string
        line2 - second single line string
    Output:
        Returns the index where the first difference between
        line1 and line2 occurs.

        Returns IDENTICAL if the two lines are the same.
    '''
    least_len = 0
    if len(line1) != len(line2):
        is_same_len = False

        if len(line1) < len(line2):
            least_len = len(line1)
        else:
            least_len = len(line2)
    else:
        least_len = len(line1)
        is_same_len = True

    diff_index = IDENTICAL
    is_same_letter = True

    for count_index in range(least_len):
        is_same_letter = line1[count_index] == line2[count_index]
        if not is_same_letter:
            diff_index = count_index
            break

    if diff_index == IDENTICAL:
        if is_same_len:
            return IDENTICAL
        else:
            return least_len
    else:
        return diff_index


def singleline_diff_format(line1, line2, idx):
    '''
    Inputs:
        line1 - first single line string
        line2 - second single line string
        idx   - index at which to indicate difference
    Output:
        Returns a three line formatted string showing the location
        of the first difference between line1 and line2.

        If either input line contains a newline or carriage return,
        then returns an empty string.

        If idx is not a valid index, then returns an empty string.
    '''
    is_clean_line1 = line1.find("\n") == -1 and line1.find("\r") == -1
    is_clean_line2 = line2.find("\n") == -1 and line2.find("\r") == -1
    is_valid_diff_index = singleline_diff(line1, line2) == idx

    if is_clean_line1 and is_clean_line2 and is_valid_diff_index:
        separator_line = "=" * idx + "^"
        return line1 +"\n"+ separator_line +"\n"+ line2 +"\n"
    else:
        return ""


def multiline_diff(lines1, lines2):
    '''        
    Inputs:
        lines1 - list of single line strings
        lines2 - list of single line strings
    Output:
        Returns a tuple containing the line number (starting from 0) and
        the index in that line where the first difference between lines1
        and lines2 occurs.
        
        Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    '''
    least_len = 0
    if len(lines1) != len(lines2):
        is_same_len = False

        if len(lines1) < len(lines2):
            least_len = len(lines1)
        else:
            least_len = len(lines2)
    else:
        least_len = len(lines1)
        is_same_len = True

    count_index = 0
    for count_index in range(least_len):
        diff_index = singleline_diff(lines1[count_index], lines2[count_index])
        if (diff_index != IDENTICAL):
            return (count_index, diff_index)

    if (is_same_len):
        return (IDENTICAL, IDENTICAL)
    else:
        if count_index != 0:
            count_index += 1
        return (count_index, 0)


def get_file_lines(filename):
    '''
    Inputs:
        filename - name of file to read
    Output:
        Returns a list of lines from the file named filename.  Each
        line will be a single line string with no newline ('\n') or 
        return ('\r') characters.

        If the file does not exist or is not readable, then the
        behavior of this function is undefined.
    '''
    with open(filename, "rt") as datafile:
        data = datafile.readlines()
        datafile.close()

    for count_index in range(len(data)):
        data[count_index] = data[count_index].rstrip()
    return data


def file_diff_format(filename1, filename2):
    '''
    Inputs:
        filename1 - name of first file
        filename2 - name of second file
    Output:
        Returns a four line string showing the location of the first
        difference between the two files named by the inputs.

        If the files are identical, the function instead returns the
        string "No differences\n".

        If either file does not exist or is not readable, then the
        behavior of this function is undefined.
    '''
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)

    diff_tuple = multiline_diff(lines1, lines2)
    diff_line = diff_tuple[0]
    diff_index = diff_tuple[1]

    if diff_line == IDENTICAL:
        return "No differences\n"
    else:
        line = "Line "+ str(diff_line) +":\n"

        if diff_line >= len(lines1):
            line1 = ""
        else: 
            line1 = lines1[diff_line]

        if diff_line >= len(lines2):
            line2 = ""
        else: 
            line2 = lines2[diff_line]

        line += singleline_diff_format(line1, line2, diff_index)
        return line

