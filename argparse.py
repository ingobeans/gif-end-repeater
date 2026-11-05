import sys

def get_args(keys:[(str,str)],help:str)->dict[str,str]:
    out = {}
    args = sys.argv[1::]
    args.reverse()
    while len(args):
        key = args.pop()
        if not key.startswith("-"):
            print(f"WARN: Unknown argument: {repr(key)}")
            continue

        # peek at next value
        next_value = args[len(args)-1]
        if next_value.startswith("-"):
            out[key] = None
            continue

        found = None
        if key.startswith("--"):
            # find flag in keys
            for k in keys:
                if key[2::] == k[0]:
                    found = k[0]
        else:
            # for only single -
            for k in keys:
                if key[1::] == k[1]:
                    found = k[0]

        next_value = args.pop()
        out[found] = next_value

    return out