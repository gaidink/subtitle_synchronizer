#!/usr/bin/python

"""
Program: Synchronized subtile file (.srt) with video.
Coder: Gaidin Kamei
Date: 09/06/16
"""


def is_srt(file_name):
    """ Receive file name as an argument.

        Check if the given file is subtitle (.srt) file or not.
    """
    if ".srt" in file_name != -1 and file_name[len(file_name)-4:]:
        return True
    else:
        return False


def time_add(t_formatted, t_sec):
    """ Formatted time (e.g 01:34:03) and time is second
        (e.g 67) are taken as an arguments.

        This function return the sum of the two times in formatted form.
    """
    t_formatted = t_formatted.split(":")
    t_secF = int(t_formatted[0])*3600 + int(t_formatted[1])*60 + \
        int(t_formatted[2])

    t_sum = t_secF + t_sec

    (minute, second) = divmod(t_sum, 60)
    (hour, minute) = divmod(minute, 60)
    time = str(hour).zfill(2) + ":" + str(minute).zfill(2) + \
        ":" + str(second).zfill(2)

    return time


def correction(file_name, error):
    """ File name and error should be entered as an arguments.

        The user get their time based faulty subtitle file
        corrected after running this program.
    """
    import os
    original_fhandler = open(file_name, "r")
    synchronized_file = os.path.dirname(file_name) + "/synchronized.srt"
    synchronized_fhandler = \
        open(synchronized_file, "w")
    for line in original_fhandler:
        if line.find("-->") != -1:
            # print line
            interval = line.split(" --> ")

            t1 = interval[0]
            t1 = t1.split(",")
            start = t1[0]
            precision_start = t1[1]

            t2 = interval[1]
            t2 = t2.split(",")
            stop = t2[0]
            precision_stop = t2[1]

            start_corrected = time_add(start, error)
            stop_corrected = time_add(stop, error)

            line = str(start_corrected) + "," + precision_start + \
                " --> " + str(stop_corrected) + "," + precision_stop
            # print line

        synchronized_fhandler.write(line)
    synchronized_fhandler.close()
    original_fhandler.close()

border = "--------------------------------------------------------------\
-----------------\n"
print border
try:
    file_name = raw_input(" Drag subtitle file here --> ")
    file_name = file_name.strip().replace("\\", "")
    file_test = open(file_name, 'r')
    if is_srt(file_name) is False:
        exit()
except:
    print "\n WARNING: The submitted file is NOT subtitle file.\n Retry!"
    print border
    exit()


try:
    state = raw_input("\nDoes the subtitle delay? (y/n): ")
    if state == "y":
        condition = "delays"
    if state == "n":
        condition = "advances"

    error = int(raw_input("The subtitle %s (in sec) by: " % condition))
    if state == "y":
        error = -(error)
except:
    print "\n WARNING: Only interger input are accepted.\n Retry!"
    print border
    exit()

try:
    correction(file_name, error)
except:
    print "\n WARNING: The content of submitted subtitle file has syntax error"
    print border
    exit()

print "\n The subtitle has been synchronized and saved in the file \
(synchronized.srt) in the same directory of the original."
print border
