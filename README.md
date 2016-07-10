# iconChooser
chooser maya icons in a gui

![screenshot](http://i.imgur.com/wJ59AcO.png)


this is used to get icon names ( both maya internal icons which you won't be able to find actual png files) and icons from XBMLANGPATH which may contains png icon files in your studio.

you can type icon names in the QLineEdit search box to search ( re supported i guess becuase it's a QCompleter )

To do list
* drag an icon from my ui to shelf , or to an existing shelfButton
* search all non-empty icon folders, maybe add all subdirectories as well

pyqt4 needed.

This is moved from [creativecrash](http://www.creativecrash.com/maya/script/maya-icon-chooser).


Usage
------------------
    import iconChooser.iconChooser as ic
    reload(ic)
    iconChooser.iconChooser.main()


on CentOS 7.2 if it errors out saying
    
    # ImportError: No module named DLFCN #
 
you can run the following [to generate DLFCN.py](http://forums.bodhilinux.com/index.php?/topic/4228-python-qt4-designer-pyuic4-no-module-named-dlfcn-solution-found/?p=39490)

    yum install python-tools
    /usr/lib64/python2.7/Tools/scripts/h2py.py /usr/include/dlfcn.h



release history
------------------
ver 0.0.2 updated to support maya 2014 , and speed up by using qlabel
ver 0.0.3 center dispaly icons and not scale them up
ver 0.0.4 fix large icons not scaled down bug, now < 32 pixel icons will be kept to original size,  > 32 pixel width large .png images will be scaled to 32*32
ver 0.0.5 use api v2, new style signal/slot, cleanup code
ver 0.0.6 fallback to api v1
