#!/usr/bin/python

import os
import subprocess
import sys, getopt

def convert_to_mp4(input_file, dry_run=False):
    """
    Converts a file to mp4. Requires ffmpeg and libx264

    input_file -- The file to convert
    dry_run -- Whether to actually convert the file
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

def convert_all_to_mp4(input_dir, allowed_extensions, dry_run=False):
    """
    Converts all files in a folder to mp4

    input_dir -- The directory in which to look for files to convert
    allowed_extensions -- The file types to convert to mp4
    dry_run -- If set to True, only outputs the file names
    """
    for root, dirs, files in os.walk(input_dir):
        for name in files:
            if name.lower().endswith(allowed_extensions):
                convert_to_mp4(os.path.join(root, name),dry_run);

def remove_converted_files(directory, allowed_extensions, dry_run=False):
    """
    Removes converted files from the directory

    directory -- The path from which to remove files
    allowed_extensions -- The file extensions to remove
    dry_run -- If set to True, only outputs the file names
    """
    for root, dirs, files in os.walk(directory):
        for name in files:
            #If a video with the same name appended with .mp4 exists, delete it
            #Please not that the converted video isn't checked, and that the file may exist
            #even though the conversion failed.
            if name.lower().endswith(allowed_extensions) and os.path.exists('%s.mp4' % os.path.join(root, name)):
                if(dry_run):
                    print "%s" % os.path.join(root, name)
                else:
                    subprocess.call("rm %s" % os.path.join(root, name),shell=True)
                    print "%s deleted" % os.path.join(root, name)

def remove_useless_files(directory, ignored_extensions, dry_run=False):
    """
    Removes files that are not videos (i.e. nfos, readmes, screenshots...), or that cannot be converted (.iso) and scripts (.py)

    directory -- The path from which to remove files
    ignored_extensions -- The file extensions to ignore
    dry_run -- If set to True, only outputs the file names
    """
    for root, dirs, files in os.walk(directory):
        for name in files:
            if not name.lower().endswith(ignored_extensions) and not name.lower().endswith(('.mp4','.py','.iso')):
                if(dry_run):
                    print "%s" % os.path.join(root, name)
                else:
                    subprocess.call("rm '%s'" % os.path.join(root, name),shell=True)
                    print "%s deleted" % os.path.join(root, name)

def flatten_directory():
    """
    Removes subdirectories after moving the files to the root dir

    dry_run -- If set to True, only outputs the file names
    """
    subprocess.call("find -L %s -mindepth 2 -type f -exec mv -t %s -i '{}' + && find -L %s -type d -empty -exec rmdir {} \;" % (video_directory,video_directory,video_directory),shell=True)
  
def main(argv):
    #Whether the script should actually perform the conversions or just list the files
    dry_run = False

    #Whether a dir or a single file should be converted
    single_file = False

    #The video in which videos are taken. This can be overriden with the -i argument
    path = os.getcwd()

    #The files that should be converted to mp4
    allowed_extensions = ('.mkv','.avi','.mpg','.wmv','.mov','.m4v','.3gp','.mpeg','.mpe','.ogm','.flv','.divx')

    try:
       opts, args = getopt.getopt(argv,"hnpcd:f:",["dry-run","dir=","purge","cleanup","file=","help"])
    except getopt.GetoptError:
        print 'Invalid arguments specified. Use the --help argument for more information.'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'Converts videos to mp4 files suitable for mobile and web playback.'
            sys.exit()

        # Dry run
        if opt in ("-n", "--dry-run"):
            dry_run = True

        # Input directory or file
        if opt in ("-d", "--dir"):
            path = arg
            single_file = False
        elif opt in ("-f", "--file"):
            path = arg
            single_file = True

        # Keep only converted files
        if opt in ("-p", "--purge"):
            remove_converted_files(path, allowed_extensions, dry_run)
            sys.exit()
        elif opt in ("-c", "--cleanup"):
            remove_useless_files(path, allowed_extensions, dry_run)
            sys.exit()

    if single_file:
        convert_to_mp4(path,dry_run)
    else:
        convert_all_to_mp4(path,allowed_extensions,dry_run)

if __name__ == "__main__":
    main(sys.argv[1:])
