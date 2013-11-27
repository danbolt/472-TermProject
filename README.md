# CSC 472 Term Project
#### Quake MDL Importer/Exporter Scripts for Blender
Written by Daniel Savage and Eric Chan

Copyright 2013 FrostTree Games

## Overview
This project is a pair of import/export scrips used to load an save 3D models and animations found in the Quake MDL format. Quake is a first-person shooter video game developed by id Software. The purpose of this project is primarily an educational exercise, so if you are considering using the MDL format for your next project, we suggest looking up more official scripts. The ones by Bill Currie are quite nice and supported by Blender.

## Installation and Running
To use the scripts with your copy of Blender, add the directory `io_quakemdl` and its contents to the `addons` directory for your copy of Blender. This can vary from system to system. On our particular flavour of Mac OS X, this happens to be:

    /Applications/blender.app/Contents/MacOS/2.68/scripts/addons
    
Now open (or restart) Blender. You should be able to enable the importer/exporter from your user settings. Another method of activiating the importer is by entering the following lines to the interactive Python console:

    import io_quakemdl
    io_quakemdl.register()
