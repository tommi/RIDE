import sys
import time


def output(sleep=0.2):
    print 'start'
    for i in range(5):
        print 'running iteration %d' % i * 500
        time.sleep(float(sleep))
    print 'done'


def count_args(*args):
    print len(args)

def stderr():
    sys.stderr.write('This is stderr\n')

globals()[sys.argv[1]](*sys.argv[2:])
