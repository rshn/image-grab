"""
wallpaper.py
  This code changes your wallpapaer using National Geographic, xkcd, abtruse goose, ...
  and feh. It grabs the image and its meta information from these webpages and saves it in a path.
  It uses a dictionary of regular expressions to grab different things from a web page.
  This dictionary is saved in the file config.json.
  You can add any image source you want. Add url, check their html code and add the appropriate regular expressions and you are done.

Usage:
  python wallpaper.py [--source ng/xkcd/ag] [--path path] [--mode wallpaper/download_only/image_only]

  --source argument is the key for the dictionary, i.e. which url and regular expressions ('/' means either one). Default is 'ng'.
  --path argument is where the image and text files get saved. Default is '.'.
  --mode argument decides on one of three modes, ('/' means either one)
    wallpaper: grab image and text and set the wallpaper,
    download_only: grab the image and text but do not set the wallpaper,
    image_only: just grab the image and be done.

Copyright 2015 Roshan Tourani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import re
from urllib2 import urlopen
from urllib import urlretrieve
import HTMLParser
import os
import sys
import argparse
import json


# Loading a json file which stores the configs for different sources.
# You only need to edit this file to add new image sources.
with open('config.json') as json_data_file:
    args_dict = json.load(json_data_file)

def html_grab(url):
  """
  Returns a string of html code, after stripping the '\n's.
  """
  try:
    return urlopen(url, timeout = 2).read().replace('\n', '')
  except urllib2.URLError:
    print ''.join(['Cannot access: ', url, '\nCheck your connection or change the timeout.'])

def img_grab(url, html_code, img_src_re, path):
  """
  Grabs the image source url from html_code string, using the regular expression img_src_re,
  and saves the image in path folder.
  Args:
    url: The url address string, for the html code where the image is.
    html_code: The html code string. The reason this function gets html_code as input is to only read open the url once.
    img_src_re: The regular expression string for grabbing the src of the img tag in the html code.
    path: Where the image is saved after retrieval.
  """
  try:
    img_src = re.search(img_src_re, html_code).group(1)
    if img_src[0:2] == '//': img_src = ''.join(['http:', img_src])
    elif img_src[0] == '/': img_src = ''.join([url, img_src])
    img_filename = img_src.split('/')[-1]
    urlretrieve(img_src, ''.join([path, img_filename]))
    print ''.join(['>> Image downloaded and saved at ', path, img_filename])
  except:
    print ''.join(['>> This is not a correct regular expression: "', img_src_re, '"\nWas trying on this html:', url, '\nUnable to grab the image.'])

  return img_filename

def txt_grab(url, html_code, img_meta_re, path, img_filename):
  """
  Grabs the image's meta information from html_code string, using the regular expressions in the img_meta_re list,
  and saves them as a text file in the path folder. The name of the text file is the same as the name of the image file with .txt extension.
  Args:
    url: The url address string, for the html code where the image is. This function only uses to give a reference if something goes wrong.
    html_code: The html code string. The reason this function gets html_code as input is to only read open the url once.
    img_meta_re: A list of regular expression strings to grab the needed meta information about the image like title or caption.
    path: Where a text file including all grabbed information is saved.
    img_filename: To make the text filename and the image filename similar. The text is saved under the same name with .txt extension.
  """
  img_meta = []
  for grab in img_meta_re:
    try:
      img_meta.append(re.search(grab, html_code).group(1))
    except:
      print ''.join(['>> This is not a correct regular expression: "', grab, '"\nWas trying on this html:', url,'\nInstead the regular expression text is copied.'])
      img_meta.append(grab)

  text = '\n'.join(img_meta)  
  text = HTMLParser.HTMLParser().unescape(text)
  txt_filename = ''.join([img_filename.split('.')[0], '.txt'])
  f = open(''.join([path, txt_filename]), 'w')
  f.write(text)
  f.close()
  print ''.join(['>> Image meta information downloaded and saved in ', path, txt_filename])

def img_set(path, img_filename):
  """
  This function needs feh to run. It sets the wallpaper using path/img_filename file.
  """
  os.system(''.join(['feh --bg-center ', path, img_filename]))

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args_list = sys.argv[1:]

  # argparse + error handling
  # --source {ng, xkcd, ag, ...} option
  # --mode {wallpaper, download_only, image_only} option
  # --path {folder} option
  parser = argparse.ArgumentParser(description =
      'Grabbing image and its description from online sources such as xkcd, abstrusegoose, National Geographic, and so on.'
      )
  parser.add_argument('--source', default = 'ng', choices=['ng', 'xkcd', 'ag'], help = 'The source of the image/caption. Choose from ng, xkcd, or ag. The default is ng.')
  parser.add_argument('--mode', default = 'wallpaper', choices=['wallpaper', 'download_only', 'image_only'], help = 'Use to only download without setting the wallpaper, or to download only the image. Choose one or multiple of {wallpaper, download_only, image_only}. The default is wallpaper')
  parser.add_argument('--path', default = './', help = 'The folder that the image/text will be saved. The default is the current folder.')
  parsed = parser.parse_args(args_list)
  
  source = parsed.source
  mode = parsed.mode
  path = parsed.path
  url = args_dict[source]['url']
  img_src_re = args_dict[source]['img_src_re']
  img_meta_re = [args_dict[source]['img_title_re'], args_dict[source]['img_date_re'], args_dict[source]['img_credit_re'], args_dict[source]['img_caption_re']]

  print ''.join(['using: ', url, ', mode: ', mode, ', saving in: ', path])

  os.chdir(path)

  html_code = html_grab(url)
  img_filename = img_grab(url, html_code, img_src_re, path)

  if mode == 'download_only' or mode == 'wallpaper':
    txt_grab(url, html_code, img_meta_re, path, img_filename)
  if mode == 'wallpaper':
    img_set(path, img_filename)


if __name__ == '__main__':
    main() 
