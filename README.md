# image-grab
The script uses a python dictionary which includes the regular expressions to grab the image and the image information from a url. Now there is only one python file, wallpaper.py, and the database contains three sources.
+ http://photography.nationalgeographic.com/photography/photo-of-the-day/
+ http://xkcd.com/
+ http://abstrusegoose.com/
+ http://www.newyorker.com/cartoons/daily-cartoon

<h4>How to use:</h4>
Usage:<br>
python wallpaper.py [--source web] [--path folder] [--mode mode]<br>
python wallpaper.py --help<br>

Args:<br>
  --source: web can be either one of ng, xkcd, ag, or nyr. ng stands for National Geographic photo of the day, xkcd is xkcd.com, ag is the absrusegoose.com, and nyr is The New Yorker's daily cartoon.<br>
  --path: folder is a folder in your computer you want to save the image and image information.<br>
  --mode: mode can be either one of wallpaper, download_only, or image_only. wallpaper grabs the image and the information and changes the wallpeper using feh. download_only only grabs the image and the information. image_only only grabs the image.<br>

<h4>Possible Extentions:</h4>
+ Add more image sources.
+ Make the grabber more sophisticated, using natural language processing, so one doesn't need regular expressions.
