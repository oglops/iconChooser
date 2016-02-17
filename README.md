# iconChooser
chooser maya icons in a gui

this is used to get icon names ( both maya internal icons which you won't be able to find actual png files) and icons from XBMLANGPATH which may contains png icon files in your studio.

you can type icon names in the QLineEdit search box to search ( re supported i guess becuase it's a QCompleter )

i also want to drag an icon from my ui to shelf , or to an existing shelfButton, but don't know how to do that.

pyqt4 needed.

This is moved from [creativecrash](http://www.creativecrash.com/maya/script/maya-icon-chooser).


Usage
------------------
import iconChooser.iconChooser as ic
reload(ic)
iconChooser.iconChooser.main()


release history
------------------
ver 0.0.2 updated to support maya 2014 , and speed up by using qlabel
ver 0.0.3 center dispaly icons and not scale them up
ver 0.0.4 fix large icons not scaled down bug, now < 32 pixel icons will be kept to original size,  > 32 pixel width large .png images will be scaled to 32*32
ver 0.0.5 use api v2, new style signal/slot, cleanup code
ver 0.0.6 fallback to api v1
