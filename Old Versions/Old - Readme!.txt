This document contains a detailed guide on how to get inconstant up and running, since the process
shown in the original video (https://www.youtube.com/watch?v=QcchT0qrWF4&t=1s) doesn't work anymore,
as well as some useful and important information

SETUP
1. Make sure you have python correctly installed (0:19-0:58 in the original video)
2. Extract the "inconst.zip" file (you can move the extracted folder to wherever you want to store it)
3. Inside the extracted folder, navigate into the "Startup" folder and create a shortcut of the
   "incostant.pyw" file
4. Open the run window by searching "run" on windows or by holding the windows key on your keyboard 
   and pressing the "R" key afterwards (1:19-1:22 in the video)
5. Type "shell:startup" and click "OK" (1:22-1:26 in the video)
6. Copy (or cut) the shortcut you created into this shell:startup folder that opened
   (you can rename the shortcut if you want)
7. Go back to the "Startup" folder inside the extracted folder and open the "incostant.pyw" 
   file with "IDLE" through the right click menu (1:42-1:49 in the video,
   you can also open it any other edditor like notepad)
8. Get the sunrise and sunset times by googling it (or looking out the window)
   and then replace the ones in the ones already in the file with yours
   (1:49-2:16 in the video, make sure to save the change)
9. Now just double click the "inconstant.pyw" file (or restart your computer) and enjoy

INFO
*THE ORIGINAL PICTURES WERE MADE BY MATT VINCE AT https://www.mattvince.com/, go check out his art
*I dont have the exact original files since i made some changes to the files, but it should work
 just fine if not better. The biggest change is the pictures. I increased the number of pictures
 so that it is less apparent when they change and I upscaled them a lot using "Waifu2x" for 
 better quality.
*DO NOT change the structure of the Inconst folder or rename anything inside without changing the
 python code or it will stop working
*The python script seems to have problems, at least for some people. Someone mentioned it in the
 comments and i experienced it too. For some reason, the wallpaper will sometimes calculate the wrong
 hour and set the wrong wallpaper from that point, behaving as if there was a time offset. closing
 the python process in the task manager and reopening inconstant.pyw or restarting your computer
 fixes it (you might have a black screen wallpaper for some time), but its not a permanent fix
 since the problem will happen again. if someone fixes this, please contact me