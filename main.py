import imageio

input_gif_path = "input.gif"

frames = []
durations = []

with imageio.get_reader(input_gif_path) as reader:
    length = reader.get_length()
    for i in range(length):
        meta = reader.get_meta_data(i)
        if meta["mode"] == "P":
            continue
        durations.append(meta["duration"])
        frames.append(reader.get_data(i))

imageio.mimsave("output.gif",frames,"gif",duration=durations)