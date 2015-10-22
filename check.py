from subprocess import PIPE, Popen
import sys

import re

from os import listdir
from os.path import isfile, join

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def numeric_compare(x, y):
    x = re.findall('\d+', x)
    y = re.findall('\d+', y) 
    return int(x[0]) - int(y[0])

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'test test_file directory'

    dirname = sys.argv[2]

    files = [join(dirname,f) for f in listdir(dirname) if isfile(join(dirname, f))]
    
    tests = [f for f in files if f.split('/')[-1][0] == 't']
    tests = sorted(tests, cmp=numeric_compare)
    
    answers = [f for f in files if f.split('/')[-1][0] == 'a']
    answers = sorted(answers, cmp=numeric_compare)

    if not len(answers) == len(tests):
        print 'Tests directory is not okay'

    target = sys.argv[1]

    tests_qty = len(tests)

    for f in tests:
        
        test = open(f).readline()
        answer = open(answers[tests.index(f)]).read()

        instance = Popen(target, stdin = PIPE, stdout = PIPE, bufsize = 1)
        instance.stdin.write(test)
        instance_answer = instance.stdout.read()

        if instance_answer == answer:
            print '[' + bcolors.OKGREEN + 'PASSED' + bcolors.ENDC + ']' + ' Test #' + str(tests.index(f) + 1)
            tests_qty -= 1
        else:
            print '[' + bcolors.FAIL + 'FAILED' + bcolors.ENDC + ']' + ' Test #' + str(tests.index(f) + 1)
            print '---------------------------------------'
            print 'Test: ' + test[:-1]
            print 'Expect: ' + answer[:-1]
            print 'Output: ' + instance_answer[:-1]
            print '---------------------------------------'

    print str(len(tests) - tests_qty) + '/' + str(len(tests))
