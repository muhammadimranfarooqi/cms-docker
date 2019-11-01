#!/usr/bin/env python
from argparse import ArgumentParser
from get_image_config import get_docker_images
from docker_utils import has_parent_changed
import glob, os
from os.path import dirname
import json

def create_file(img):
  print('Writing to file ....')
  file_name = (img.get('IMAGE_NAME').replace('/', '_').replace(':', '_') + '.txt')
  with open(file_name,'w+') as file:
    for key, value in img.items():
      line = str(key) + '=' + str(value) + '\n'
      file.write(line)
  file.close()
  print('{} file created'.format(file_name))

parser = ArgumentParser(description='Check if docker image based on the same layers as the parent image')
parser.add_argument('-r', dest='repo', type=str, help="Provide specific repository for docker images.")
parser.add_option("-f", "--force",    dest="force",     action="store_true", help="Force re-build", default=False)
args = parser.parse_args()
repos = []
if args.repo:
  repos.append(args.repo)
else:
  dir = os.path.dirname(dirname(os.path.abspath(__file__)))
  for file in glob.glob(dir + '/**/*.yaml*'):
    repos.append(os.path.basename(dirname(file)))

for reponame in repos:
  for img in get_docker_images(reponame):
    buildimg = args.force
    if not buildimg:
      inher= img.get('IMAGE_NAME')
      parent = img.get('BASE_IMAGE_NAME')
      buildimg = has_parent_changed(parent, inher, reponame)
   if buildimg:
      create_file(img)
