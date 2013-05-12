import os
import subprocess
import sys

#The video in which videos are taken
video_directory = "/media/videos/Movies"

#The files that should be converted to mp4
video_extensions = ('.mkv','.avi','.mpg','.wmv','.mov','.m4v','.3gp','.mpeg','.mpe','.ogm','.flv','.divx')

def convert_to_mp4(input_file, dry_run=False):
    """
    Converts a file to mp4. Requires ffmpeg and libx264

    input_file: The file to convert
    dry_run: Whether to actually convert the file
    """
    output_file = input_file + '.mp4'
    ffmpeg_command = 'ffmpeg -loglevel quiet -i "%s" -vcodec libx264 -b 700k -s 480x368 -acodec libfaac -ab 128k -ar 48000 -f mp4 -deinterlace -y -threads 4 "%s" ' % (input_file,output_file)

    if not os.path.exists(output_file):
        if not os.path.exists(input_file):
            print "%s was queued, but does not exist" % input_file
            return

        if dry_run:
            print "%s" % input_file
            return

        print "Converting %s to MP4\n" % input_file

        #ffmpeg
        print subprocess.call(ffmpeg_command,shell=True)

        #qtfaststart so it streams
        print subprocess.call('qtfaststart "%s"' % output_file,shell=True)

        #permission fix
        print subprocess.call('chmod 777 "%s"' % output_file,shell=True)

        print "Done.\n\n"

    elif not dry_run:
        print "%s already exists. Aborting conversion." % output_file

def convert_all_to_mp4(dry_run=False):
    """
    Converts all files in a folder to mp4

    dry_run: If set to True, only outputs the file names
    """
    for root, dirs, files in os.walk(video_directory):
        for name in files:
            if name.lower().endswith(video_extensions):
                convert_to_mp4(os.path.join(root, name),dry_run);

def pretend_convert_all_to_mp4():
    convert_all_to_mp4(True)

def remove_converted_files(dry_run=False):
    """
    Removes converted files from the directory

    dry_run: If set to True, only outputs the file names
    """
    for root, dirs, files in os.walk(video_directory):
        for name in files:
            #If a video with the same name appended with .mp4 exists, delete it
            #Please not that the converted video isn't checked, and that the file may exist
            #even though the conversion failed.
            if name.lower().endswith(video_extensions) and os.path.exists('%s.mp4' % os.path.join(root, name)):
                if(dry_run):
                    print "%s" % os.path.join(root, name)
                else:
                    subprocess.call("rm %s" % os.path.join(root, name),shell=True)
                    print "%s deleted" % os.path.join(root, name)


def pretend_remove_converted_files():
    remove_converted_files(True)


def remove_useless_files(dry_run=False):
    """
    Removes files that are not videos (i.e. nfos, readmes, screenshots...)

    dry_run: If set to True, only outputs the file names
    """
    for root, dirs, files in os.walk(video_directory):
        for name in files:
            if not name.lower().endswith(video_extensions) and not name.lower().endswith(('.mp4','.php','.py','.iso')):
                if(dry_run):
                    print "%s" % os.path.join(root, name)
                else:
                    subprocess.call("rm '%s'" % os.path.join(root, name),shell=True)
                    print "%s deleted" % os.path.join(root, name)


def pretend_remove_useless_files():
    remove_useless_files(True)


def flatten_directory():
    """
    Removes subdirectories after moving the files to the root dir

    dry_run: If set to True, only outputs the file names
    """
    subprocess.call("find -L %s -mindepth 2 -type f -exec mv -t %s -i '{}' + && find -L %s -type d -empty -exec rmdir {} \;" % (video_directory,video_directory,video_directory),shell=True)


try:
    locals()[sys.argv[1]]()
except:
    print "Command not specified or not found. Options are flatten_directory, remove_useless_files, pretend_remove_useless_files, remove_converted_files, pretend_remove_converted_files, convert_to_mp4, convert_all_to_mp4, pretend_convert_all_to_mp4"
