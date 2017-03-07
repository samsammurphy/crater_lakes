__author__ = "Michael A. Menarguez"
__copyright__ = "Copyright 2015"
__credits__ = "Michael A. Menarguez"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Michael A. Menarguez"
__email__ = "mamenarguez@ou.edu"
__status__ = "Production"

from multiprocessing import Pool
import sys

import ee 
ee.Initialize()

import time
import random
def cancel_task(task):
    print task
    random_time = random.random()
    time.sleep(0.5+random_time*0.5)
    if task.config['state'] in (u'RUNNING',u'UNSUBMITTED',u'READY') :
        print 'canceling %s' % task
        task.cancel()
def get_tasks():
    return ee.batch.Task.list()

def usage():
    print '------------cancel_tasks.py---------------'
    print '---Cancel all running / pending tasks:'
    print '     python cancel_tasks.py'
    print '---Cancel all running / pending tasks containing substring (no regex applied):'
    print '     python cancel_tasks.py substring'
    
if __name__=='__main__':
    if len(sys.argv)>2:
        usage()
        sys.exit(-2);
    tasks = get_tasks()
    tasks = [task for task in tasks if task.config['state'] in (u'RUNNING',u'UNSUBMITTED',u'READY')]

    if len(sys.argv)>1:
        tasks = [task for task in tasks if len(task.config['description'].split(sys.argv[1]))>1]
    print 'cancelling %d tasks' % len(tasks)
    p = Pool(4)
    p.map(cancel_task,tasks)
    for task in tasks:
        cancel_task(task)


