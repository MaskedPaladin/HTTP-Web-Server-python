def check(filepath):
    code = False
    codeBody = ""
    with open(filepath, "r") as f:
        lines = f.readlines()
        for l in lines:
            if l.replace(" ","").replace("\n", "") == "code[":
                code = True
                continue
            if "]" in l:
                code = False
            if code == True:
                codeBody+=l
    toDo = ""
    forFlag = False
    forStartIndex = None



    for l in codeBody.split("\n"):
        if l[0:2] == "for":
           forFlag = True 
