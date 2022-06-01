def check(text):
    opened = False
    document = ""
    sentence = ""
    repeat_times = 0
    for j, line in enumerate(text.split("\n")):
        if line.replace(" ","") == "code{":
            opened = True
            continue
        if line == "}":
            opened = False
        if opened == True:
            current = line.split(" ")
            if current[0].replace("\t","") == "for":
                if current[2] == "in":
                    if "range" in current[3]:
                        brackets = False
                        n = ""
                        for c in current[3]:
                            if c == "(":
                                brackets = True
                                continue
                            if c == ")":
                                brackets = False
                                repeat_times = int(n)
                                break
                            if brackets == True:
                                n+=c
                        for i in range(repeat_times):
                            document+=text.split("\n")[j+1]+"\n"
                        repeat_times = 0
    return document
