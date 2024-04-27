# About SECAD

SECAD will allow you to open a blueprint and display it in the view. You will be able to move, add, and delete blocks and save.

This project has just started. I don't have a list of features yet.

The first stage is to get the CAD window to move in steps correctly and snap correctly to blocks.

Building SECAD.

You need Qt 5.15 and Visual Studio 2019 with Qt as an extension. I'm developing in VS2019 as I'm more familier with it then Qt Creator.

You need to install ZLib, I used the vcpgk tool and followed the instructions for installing it. https://vcpkg.io/

After you build SECAD and run it, you need to change where the library is. Under View | Preferences you will find the current path for the Parts Library. You change it to your folder or the project one. Point to the ldraw folder.