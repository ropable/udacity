import os
import math
import random
import string
import subprocess
import time

def files_in_dir_to_list(dir):
    "return a list with the names of all the files in the dir directory"
    dir_list = os.listdir(input_file_dir)
    file_list = [filename for filename in dir_list]
    return file_list

input_file_dir = "/home/username/input_files/"
output_file_dir = "/home/username/fuzzer_output/"

"the applications and files to fuzz"
apps = ["/Applications/Seashore.app/Contents/MacOS/Seashore"]
file_list = files_in_dir_to_list(input_file_dir)

"the smaller the FuzzFactor, the more we corrupt the file"
FuzzFactor = 500
num_tests = 1000
sleep_delay = 2.8

eta = sleep_delay*num_tests
print 'Fuzz will run for %0.1fs (i.e., %0.1f mins or %0.1f hrs)'%(eta,eta/60,eta/3600)

t1 = time.time()
for i in range(num_tests):
    print "i=",i

    "file and app to use in fuzz"
    app = random.choice(apps)
    file_choice = random.choice(file_list)
    fuzzed_filename = input_file_dir + file_choice
    buf = bytearray(open(fuzzed_filename, 'rb').read())

    "Army of Monkeys 5-line fuzzer"
    numwrites=random.randrange(math.ceil((float(len (buf)) / FuzzFactor)))+1
    for j in range (numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)

    "save the fuzzed file in the local directory"
    fuzz_output = "".join(['fuzz_',file_choice])
    open(fuzz_output, 'wb').write(buf)

    "try to open it"
    process = subprocess.Popen([app, fuzz_output])
    time.sleep(sleep_delay)
    crashed = process.poll()
    if not crashed:
        process.terminate()
    else:
        "app crashed.. save the fuzzed file"
        fuzzed_filename = "".join([output_file_dir,"crash_",str(i),"_",file_choice])
        open(fuzzed_filename, 'wb').write(buf)

    "remove the fuzzed file"
    cmd_rm = "rm -rf "+fuzz_output
    os.system(cmd_rm)

t2 = time.time()
print '%s took %0.3f s' % ('fuzzing', (t2-t1))
