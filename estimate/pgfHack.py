""""
the pgf backend of matplotlib has a bug where bars
of a bar chart are only half filled ...
"""
def fix_pgf_file(filename):
    in_file = open(filename)
    out_file = open(filename.replace(".pgf", "-fix.pgf"), "w")

    bullshit_counter = 0
    for line in in_file:
        if line.startswith("\pgfpathlineto{\pgfqpoint{"):
            bullshit_counter += 1

        elif line.startswith("\pgfpathmoveto{\pgfqpoint{"):
            if bullshit_counter >= 2:
                # print("detected: " + line)
                line = line.replace("pgfpathmoveto", "pgfpathlineto")
                # print("fixed: " + line)
            bullshit_counter = 0

        else:
            bullshit_counter = 0

        out_file.write(line)