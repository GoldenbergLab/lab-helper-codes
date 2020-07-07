### 1. Picture formatter

This code has 4 main functions which can be applied to a single image or a whole directory of images name changer: takes a picture and changes the number index of the picture according to the rule, which is right now, if a picture is for e.g. A01 it will add 50 to it to make it A51.
You can change the roles for labeling according to your needs size changer: takes an image and changes the size proportionally. Right now it creates images of the widht 141pixels background_color_changer: takes a picture and changes the background to grey

**remover:** removes files from directory

**LOOPS AT THE BOTTOM:** They can be used to process a whole batch/directory

**LOOP 1:** changes all names by creating a copy with the new name. It also removes the old version with the old name

**LOOP 2:** changes the background and the size of all files


 **For tasks related to image Morphs**
 This code transforms the original morphs that you get from fantamorph into the right SIZE, LABEL, and BACKGROUND
 In case that some pictures are to bright change the variables such as sensitiyity in the function background_color_changer
 Mind that the input picture size has to be around 500 * 650
 otherwise you have to adjust the x, y, w, h = 140, 100, 200, 550 values in background_color_changer
 I will change that requirement at some point :D
