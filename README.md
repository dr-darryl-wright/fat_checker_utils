# fat_checker_utils
Utilities for the Etch-A-Cell Fat Checker Citizen Science project: https://www.zooniverse.org/projects/dwright04/etch-a-cell-fat-checker

## Installation


Clone this repo
```
$ git clone https://github.com/dr-darryl-wright/fat_checker_utils.git
```

install dependencies
```
$ pip install numpy Pillow panoptescli
```

## Prepare images and manifest 

To prepare data for upload (generate blank images and manifest) run fat_checker_utils/image_and_manifest_preparation.py.  The script assumes image file naming such that the images are ordered according to their location in the volume.  For example:
```
$ ls modified\ area\ 1/
   ROI1_10nmx10nmx50nm001.jpg
   ROI1_10nmx10nmx50nm002.jpg
   ROI1_10nmx10nmx50nm003.jpg
   ROI1_10nmx10nmx50nm004.jpg
   ...
```
where ROI1_10nmx10nmx50nm001.jpg is an image of the slice directly preceding ROI1_10nmx10nmx50nm002.jpg which in turn precedes ROI1_10nmx10nmx50nm003.jpg etc. The script will create blank images.  The script assumes a batch size of 5 images per subject and creates blank images at the top and bottom of the volume accordingly.  **The script also has some hardcoded filename checking to handle differences in the image naming conventions.**  The metadata associated with each image is also hardcoded and should be reviewed to check it is correct for new subject sets.

```
$ python image_and_manifest_preparation.py --path <path to images> --volume_identifier <unique volume identifier>
```

e.g. 
```
$ python image_and_manifest_preparation.py --path /home/alice/data/modified\ area\ 1/ --volume_identifier 3R_ROI1
```

After running this script 4 blank images (identified as e.g. ROI1_10nmx10nmx50nm000*_blank*.jpg) and a manifest .csv file that is required by the panoptes commandline interface for subject set upload.

## Upload data to Zooniverse project with panoptes commadline interface

For each batch of new images a subject set needs to be created.  If the panoptes commandline interface is installed (see Installation above) run

```
$ panoptes subject-set create <project id number> "subject set name"
```

e.g.
```
$ panoptes subject-set create 11994 "3R_ROI1_modified_area_1"
```

you will be prompted for your Zooniverse login credentials.  This will return something like
```
    4667 3R_ROI1_modified_area_1
```

the number is the subject set id number, which is needed in the next step.

Next, using the manifest created above and subject set id number upload the images to this subject set by running

```
$ panoptes subject-set upload-subjects 4667 manifest.csv
```

make sure you are in the same directory as the manifest when running this command.
