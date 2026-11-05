import imageio, argparse

keys = [
    ("input","i","path","specifies the input file path",True),
    ("output","o","str","output file path",True),
    ("repeat-n","n","int","the n last frames that are repeated",True),
    ("count","c","int","the amount the repeat section is repeated",True),
]

help_text = """
# gif-end-repeater.py

Usage: gif-end-repeater.py <flags>
Args:
""".strip()

args = argparse.get_args(keys,help_text)

input_gif_path = args["input"]
output_gif_path = args["output"]

frames = []
durations = []

repeat_frames_n = args["repeat-n"]
repeat_count = args["count"]

def write_frame(reader,index):
    global durations,frames
    meta = reader.get_meta_data(index)
    if meta["mode"] == "P":
        return
    durations.append(meta["duration"])
    frames.append(reader.get_data(index))

with imageio.get_reader(input_gif_path) as reader:
    length = reader.get_length()
    repeat_start = length - repeat_frames_n

    # write regular frames
    for index in range(0, repeat_start):
        write_frame(reader, index)
    
    for _ in range(repeat_count):
        for i in range(repeat_frames_n):
            index = repeat_start + i
            write_frame(reader, index)


imageio.mimsave(output_gif_path, frames, "gif", duration=durations)
print(f"Wrote {len(frames)} frames!")