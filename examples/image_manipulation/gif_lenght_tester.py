import os
from PIL import Image
def find_duration(img_obj):
    img_obj.seek(0)  # move to the start of the gif, frame 0
    tot_duration = 0
    # run a while loop to loop through the frames
    while True:
        try:
            frame_duration = img_obj.info['duration']  # returns current frame duration in milli sec.
            tot_duration += frame_duration
            # now move to the next frame of the gif
            img_obj.seek(img_obj.tell() + 1)  # image.tell() = current frame
        except EOFError:
            return tot_duration # this will return the tot_duration of the gif
if __name__ == '__main__':
    filepath = input('Enter the file path for the gif:')
    if os.path.exists(filepath):
        img = Image.open(filepath)
        gif_duration = find_duration(img)
        print(f'Duration of {os.path.basename(filepath)} is {gif_duration/1000} s')  # divide by 1000 to convert to seconds
    else:
        print('Invalid path entered!')

#gifs50MS/A_4550_138