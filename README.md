# database_marking_tool

Python tool for annotating images used to create PUT Surveillance database. The database can be found at:
http://www.vision.put.poznan.pl/surv_database

## Acknowledgment

This code is used in the project entitled:

*"NEW CONCEPT OF THE NETWORK OF SMART CAMERAS WITH ENHANCED AUTONOMY FOR AUTOMATIC SURVEILLANCE SYSTEM"*

More information about the project can be found: http://www.vision.put.poznan.pl/?page_id=237

## Description

The tool allows loading specified set of images and annotating them by usage of mouse and some keyboard shortcuts. Currently objects can be marked as person, car or cyclist but it is very easy to add additional classes. The program saves the scene description to aa file which can be then loaded. The descriptions can be easly modified between images and description of one image can be easly copied to another image. 

## Languages and tools used

The project is written in Python 2.7.10 and uses following libraries (+ all the prequisitions for those):
* opencv - for image loading / saving, resizing, drawing, creating video, etc.
* lxml - for creating XML fies.

## Modules description
* database_marking_tool.py - main app for loading and annotaing images
* Utils.py - stores all the parameters and offers additional tools for creating the video file or the xml file 
* ObjectInformation.py - class for stroing information about each object marked on the scene
* MouseButton.py - class for storing mouse information

## Running the code
Run the database_marking_tool.py script (put images in appropriate folders or modify paths in the script), annoteate images using mouse clicks and keyboard shortucts (easy to find in the code). To convert all the description files into one XML file run the Utils.py script.

## License

MIT
