# OpenMosseCam
Open camera GUI for Raspberry pi

Installation instructions:
The python programs in this project are designed to work out of the box with the StereoPi and Raspberry Pi compute board. Copy the programs you want onto your desired image or Raspbian and run.

Hardware requirements:
- Raspberry Pi Compute board
- StereoPi board
- At least one (preferably two) raspberry pi compatible camera modules
- SD card with Raspbian image

Operation instructions:
You can control Stereo MosseCam from the command line of the GPIO (including via a GPIO LCD screen or TFT).

The user interface uses four navigation buttons/prompts which trigger different functions according to the active display (see below).

Viewfinder:
1) Capture (photo/video)
2) Toggle GUI overlay display
3) Settings Menu
4) Gallery

Settings Menu:
1) Return to viewfinder
2) Next setting value up
3) Next setting value down
4) Next setting

Gallery:
1) Return to viewfinder
2) Next image/video up
3) Next image/video down
4) Delete image/video

Changes from previous version:
- Began rewriting the program without Pygame (only using picamera and OpenCV)
- Created Scriptable_MosseCam_Presentation.py to visualise and record scripted events in Stereo MosseCam
- Created a specialised version of MosseCam for video applications only with more control over specialised video settings.
