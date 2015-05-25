# sentinel
The Sentinel is an open-source surveillance camera for students and other poor people. 
Over time, it will be sculpted into a tool that college students can hang in their dorms and library cubicles, 
and it will monitor a small perimeter around itself. This is not a full-blown surveillance system for large houses, 
but for tiny apartments and dorm rooms.
To run, do the following:
1. Copy your config file to a different folder on your Raspberry Pi, and edit it. I keep my config file at /etc/sentinel/ (I create the sentinel directory in /etc/)
2. Add the new path of the config file to the sentinel.py.
3. Create a pickle file with the present time stored in the format specified in the code(its a Python datetime object).
4. Modify motion configure file:
   You will find the motion.conf file in /etc/motion/.
   Edit the same by adding the following lines.
    # Command to be executed when a picture (.ppm|.jpg) is saved (default: none)
    # To give the filename as an argument to a command append it with %f
    on_picture_save sudo python /home/pi/sentinel/sentinel.py


 
5. Live happily ever after.


