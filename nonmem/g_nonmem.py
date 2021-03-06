from grisu.Grython import serviceInterface as si
from grisu.frontend.control.login import LoginManager
from grisu.frontend.model.job import JobObject
from grisu.model import GrisuRegistryManager
from java.io import File
from javapath import isfile
import sys

files_file = sys.argv[1]
jobname_template = 'nonmem'
commandline = 'ls -lah'

# for production we want a longer intervall, otherwise the backend gets too much load
jobstate_check_intervall = 5

target_dir = '/home/markus/Desktop'

def read_files(files_file):
    # read all files from the text file
    files_to_upload = []
    for line in open(files_file).readlines():
        line = line.strip()
        if line:
            if isfile(line):
                files_to_upload.append(line)
            else: 
                print 'Not a file: '+line
                sys.exit(1)
    return files_to_upload

files_to_upload = read_files(files_file)

if not si:
    LoginManager.initEnvironment()
    si = LoginManager.login('bestgrid', True)

filemanager = GrisuRegistryManager.getDefault(si).getFileManager()

job = JobObject(si)
job.setSubmissionLocation('pan:pan.nesi.org.nz')
job.setTimestampJobname(jobname_template)
job.setCommandline(commandline)

# add input files
for file in files_to_upload:
    job.addInputFileUrl(file)
    

jobname = job.createJob('/nz/nesi')
print 'Submitting job...'
job.submitJob()
print 'Jobname: '+jobname

print 'Waiting for job to finish...'
job.waitForJobToFinish(jobstate_check_intervall)

job_directory = job.getJobDirectoryUrl()
print 'Job finished, jobdirectory: '+job_directory

print 'Downloading results'
target = filemanager.downloadUrl(job_directory, File(target_dir), False)

print 'Download finished, download folder: '+target.getPath()







