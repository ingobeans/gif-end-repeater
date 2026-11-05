import imageio

input_gif_path = "input.gif"

frames = []
durations = []

repeat_frames_n = 6
repeat_count = 10

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


imageio.mimsave("output.gif", frames, "gif", duration=durations)
print(f"Wrote {len(frames)} frames!")