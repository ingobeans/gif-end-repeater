import sys, os

def get_args(keys:[(str,str,str,str,bool|None)],help:str)->dict[str,str]:
    out = {}
    args = sys.argv[1::]
    args.reverse()
    while len(args):
        key = args.pop()
        if not key.startswith("-"):
            print(f"WARN: Unknown argument: {repr(key)}")
            continue

        # check for help
        if key == "--help" or key == "-h":
            print(help)
            for key in keys:
                print(f"\t--{key[0]} <{key[2]}> ({key[1]}): {key[3]}{"*" if key[4] else ""}")
            exit(0)

        found = None
        if key.startswith("--"):
            # find flag in keys
            for i,k in enumerate(keys):
                if key[2::] == k[0]:
                    found = i
        
        # peek at next value
        if len(args) == 0:
            print(f"WARN: No value given for key: {repr(key)}")
            continue

        next_value = args[len(args)-1]
        if next_value.startswith("-"):
            print(f"WARN: No value given for key: {repr(key)}")
            continue

        else:
            # for only single -
            for i,k in enumerate(keys):
                if key[1::] == k[1]:
                    found = i
        
        next_value = args.pop()

        if found == None:
            print(f"WARN: Unknown arg: {repr(key)}")
            continue

        found_key = keys[found]

        # match type
        good = False
        try:
            match found_key[2]:
                case "str":
                    good = True
                case "int":
                    next_value = int(next_value)
                    good = True
                case "float":
                    next_value = float(next_value)
                    good = True
                case "bool":
                    next_value = next_value.lower()
                    values = [("yes",True),("true",True),("y",True),("no",False),("n",False),("false",False)]
                    for k,v in values:
                        if k == next_value:
                            good = True
                    if not good:
                        print(f"WARN: Boolean value of {repr(key)} couldn't be parsed ({repr(next_value)})")
                        continue
                case "path":
                    if not os.path.exists(next_value):
                        print(f"WARN: Path doesn't exist: {next_value}")
                        continue
                    good = True
                case _:
                    print(f"WARN: Unknown arg type of key {repr(found_key[0])}: {repr(found_key[2])}")
                    continue
        except:
            continue

        if not good:
            print(f"WARN: Wrong type of arg: {repr(key)} ({repr(next_value)}) - should be {found_key[2]}")
            continue

        out[found_key[0]] = next_value

    # check that all required args are included
    missing = []
    for key in keys:
        if not key[0] in out:
            missing.append(key[0])
    
    if len(missing):
        print(f"ERROR: Missing keys: {repr(missing)}")
        exit(0)

    return out