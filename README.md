# image-grab
The script uses a python dictionary which includes the regular expressions to grab the image and the image information from a url. Write now there is only on python file, wallpaper.py.
Usage: python wallpaper.py [--source web] [--path folder] [--mode mode]
Args:
  source: web can be either one of ng, xkcd, or ag. ng stands for National Geographic photo of the day, xkcd is xkcd.com, and ag is the absrusegoose.com.
  path: folder is a folder in your computer you want to save the image and image information.
  mode: mode can be either one of wallpaper, download_only, or image_only. wallpaper grabs the image and the information and changes the wallpeper using feh. download_only only grabs the image and the information. image_only only grabs the image.

Possible Extentions:
+ Add more sources.
+ Make the dictionary args_dict a database file, like json, instead of a global dictionary variable.
+ Make the grabber more sophisticated, using natural language processing, so one doesn't need regular expressions.
