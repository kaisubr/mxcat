import argparse
import sys
import xml.etree.ElementTree as ET

# Sample usage ----
# View help message:        python mxcat.py -h | less 
# Concatenate files:        python mxcat.py file*.mscx > catted.mscx
# Preview result:           python mxcat.py file*.mscx | less -S
# Numbered lines:           python mxcat.py file*.mscx | cat -n
# Search debug comments:    python mxcat.py out*.mscx --debug | grep "\[DEBUG]\"
# -----------------

parser = argparse.ArgumentParser(description='Concatenate Musescore XML files and print on the standard output; mxcat behaves similarly to UNIX cat, where you may redirect output to another file. You can pipe to cat if you want access to cat-like options (such as -n, -v, and so on)')

parser.add_argument('names', metavar='files', type=str, nargs='+', help='Files to concatenate.')
parser.add_argument('--output', metavar='output', type=str, nargs=1, help="File to write to. Exists for cross-compatability and multiple output. You can also use the UNIX redirection > output.mscx, instead of this argument.", default=[0])
parser.add_argument('--staff', metavar='staves', type=str, nargs=1, default=["0"], help='Colon and comma-separated staff-numbers to print across multiple files, for instance --staff 0:1,2,3,4:5,6 will create three files where the first file prints all parts, the second file prints staves 1, 2, 3, and 4, while the third file prints staves 5 and 6. The staff 0 indicates to mxcat that it will print all parts. To save files, also ensure that --output is set to a value. **Colon-separated file output is experimental.** If multiple files are given, mxcat will merge the files before printing.')
parser.add_argument("--count", action='store_true', help='Print number of staffs in the score, and exit. If multiple files are given, only the first file will be parsed.')
parser.add_argument('--debug', action='store_true', help='Print debug comments into output, which is grep-able with [DEBUG].', default=False)

# get arguments 
args = parser.parse_args()

# args.names with nargs + as list
files = args.names
files_to_print = list(args.staff)[0].split(":") # sorted(list(
debug = args.debug
only_count = args.count
writeto = args.output[0]
of = []
if str(writeto) != "0":
    for k in files_to_print:
        of.append(open(writeto.split(".")[0] + "_" + k + ".mscx", "w+"))

def ecr(text, i=0, end="\n"):
    if str(writeto) == "0":
        print(text, end=end)
    else:
        of[i].write(str(text) + end)
        of[i].flush()


def warn(*args, i=0):
    if debug:
        ecr("<!--\n[DEBUG] ", end="", i=i)
        for a in args:
            ecr(str(a), end=" ", i=i)
        ecr("\n-->", i=i)


# get header + metadata portion as lines list
def get_headline(fname):
    ls = []
    tfile = open(fname, "r")
    parseable = False
    for line in tfile:
        ls.append(line.rstrip())
        if "<Part>" in line:
            parseable = True
            break
    if not parseable:
        raise SyntaxError("The mscx file is not parseable, since no Part tag was found.")
    return ls


# get staff data as list. 0th index is dummy.
def get_staff(fname):
    staff_metadata = ["0"]
    rootst = ET.parse(fname).getroot() # museScore

    for staff in rootst.findall('Score/Part/Staff'):
        staff_metadata.append(str(ET.tostring(staff), 'utf-8'))

    return staff_metadata


# header from first score:
root = ET.parse(files[0]).getroot()
staff_meta = get_staff(files[0])
num_staffs = len(staff_meta) - 1

if only_count:
    ecr(num_staffs)
    sys.exit()


def print_score(file_with_titles, stf_print, i=0):
    global num_staffs
    # PRINT score metadata AND <Part>
    larr = get_headline(file_with_titles)
    for line in larr:
        ecr(line, i=i)

    warn("Staff count:", num_staffs, "detected in", file_with_titles, i=i)
    # PRINT staff metadata
    if int(stf_print[0]) == 0:
        warn("Printing all staffs 1 to ", num_staffs, i=i)
        for num in range(1, num_staffs + 1):
            ecr(staff_meta[int(num)], i=i)
    else:
        for num in stf_print:
            warn("Printing staff metadata for staff", num)
            ecr(staff_meta[int(num)], i=i)


    # PRINT closing Part tag
    ecr("</Part>", i=i)


    # Add opening tags for each staff
    staff_data = []
    staff_data.append("")
    for num in range(1, num_staffs + 1):
        try:
            actual_num = stf_print.index(str(num)) + 1 # if staffs are [1,4] then we want ["", id=1, id=2, id=3, id=2]
            staff_data.append('<Staff id="' + str(actual_num) + '">\n')
        except ValueError:
            staff_data.append('<Staff id="' + str(num) + '">\n')
            # raise ValueError("Staff number" + num + "was not found in file")

    # bodies (extract each staff data from each file)
    for f in files:
        warn("Parsing body of", f, i=i)

        num_staffs = len(get_staff(f)) - 1
        
        root = ET.parse(f).getroot()
        for sf_id in range(1, num_staffs + 1):
            # 1, 2 for 2 staffs.
            for staff in root.findall('Score/Staff'):
                if str(sf_id) == str(staff.get("id")):
                    strl = str(ET.tostring(staff), 'utf-8').split("\n")
                    
                    # Don't want first and last items (<Staff id=> and </Staff>)
                    for item in strl:
                        if (not item.lstrip().startswith('<Staff id=')) and (not item.lstrip().startswith("</Staff>")):
                            staff_data[sf_id] += item + "\n"
        del root


    # Add closing tag to end of each staff in list data.
    for val in range(1, num_staffs + 1):
        staff_data[val] += "\n</Staff>"


    # PRINT the staffs.
    if int(stf_print[0]) == 0:
        warn("Printing all staffs", i=i)
        for data in staff_data:
            ecr(data, i=i)
    else:
        for st in stf_print:
            warn("Printing staff", st, i=i)
            ecr(staff_data[int(st)], i=i)

    # PRINT footer
    ecr("</Score>\n</museScore>", i=i)


# Print the score.
for out in range(0, len(files_to_print)):
    print_score(files[0], files_to_print[out].split(","), i=out)
    warn("Finished generating file", out, "which contains staffs", files_to_print[out], i=out)


# Close any files.
for k in of:
    if k is not None:
        k.close()
