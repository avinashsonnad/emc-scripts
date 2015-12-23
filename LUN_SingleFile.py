import re
import os
import sys
import time

def module_folderpath_creation():	
	if "../modules" not in sys.path:
		sys.path.append("../modules"

		
		# function (depends on rli3 definition above)
def watch_async_progress(result_record, method_name):
    print result_record	
    if type(result_record) == dict and result_record.has_key('async_progress'):
        status = {'OPERATION': 'storage_' + method_name,
                  'PROGRESS': 0}
        while result_record['async_progress'] != None:
            status['PROGRESS'] = result_record['async_progress']
            print status
            time.sleep(2)

            result_list = ["10.32.70.203", "5988", "admin", "#1Password", "310"]
            # append job_id
            result_list.append(result_record['async_handle'])
            try:
                result_record = emc_get_async_progress(result_list)
                print "async_handle", result_record
            except Exception, e:
                print e
                return None

    if result_record.has_key('async_progress'):
        del result_record['async_progress']

    if result_record.has_key('async_handle'):
        print "async_handle", result_record['async_handle']
        del result_record['async_handle']

    print "result: ", result_record
    return result_record

	
# create a LUN	
def create_lun():
	li_array = ["10.32.70.203", "5988", "admin", "#1Password", "SYMMETRIX+000195900310"]
	print 'Invoking emcsps.emc_create_lun begin ...'
	li3 = list(li_array)
	#li3.extend(["SMI_POOL", "1073741824", "1"])
	#li3.extend(["HUI_THIN", "meta", "30737418240", "1", "meta_member_size=10,m,,,a = b ,    d=    c    ,   e   =  d   e  ff   d    ,meta_conf=stripe,m==,,,,"])
	li3.extend(["HUI_THIN", "meta", "30737418240", "1", None])
	#li3.extend(["RAID5", "1073741824", "0"])

	lun_id = None
	lr3 = None
	try:
		print li3
		lr3 = emc_create_lun(li3)
	except Exception, e:
		print e

	if lr3 is not None:
		lr3 = watch_async_progress(lr3, 'create')
		if lr3 is not None:
			for key in lr3.keys():
				print "%20s %30s" % (key, lr3[key])
			if lr3.has_key('id'):
				lun_id = lr3['id']

	print 'emcsps.emc_create_lun Done'
	print
	return lun_id
	
#create clone
def create_clone(lun_id):
	print 'Invoking emcsps.emc_create_clone begin ...'
	li3 = list(li_array)
	#li3.append("000CF")
	#li3.append("000CF_clone")
	li3.append("00278")
	li3.append("00278e1")

	#lun_id = None
	lr3 = None
	try:
		print li3
		lr3 = emc_clone(li3)
	except Exception, e:
		print e

	if lr3 is not None:
		print "LR3: ", lr3
		lr3 = watch_async_progress(lr3, 'create')
		if lr3 is not None:
			for key in lr3.keys():
				print "%20s %30s" % (key, lr3[key])
			if lr3.has_key('id'):
				lun_id = lr3['id']

	print 'emcsps.emc_clone Done'
	print
	

def present():
	args = ["10.110.26.143", "5988", "admin", "#1Password", "CLARiiON+APM00123901876"]
	args.append(LUNA)
	args.append(AGNAME)
	print "Invoking start present"
	print emc_start_present(args)

	args.pop()
	args.pop()
	args.append(LUNB)
	args.append(AGNAME)
	print emc_start_present(args)
	
	
def unpresent():
	args = ["10.110.26.143", "5988", "admin", "#1Password", "CLARiiON+APM00123901876"]
	args.append(LUNA)
	args.append(AGNAME)
	print "Invoking stop present"
	print emc_stop_present(args)

	args.pop()
	args.pop()
	args.append(LUNB)
	args.append(AGNAME)
	print "Invoking stop present"
	print emc_stop_present(args)

def remove_lun(lun_id)
	# remove the specified LUN
	args = sys.argv[:]

	# any arguments will bypass remove operation
	li3 = list(li_array)
	lr3 = None
	if lun_id is not None:
		try:
			li3.append(lun_id)
			print li3
			lr3 = emc_remove_lun(li3)
		except Exception, e:
			print e

	if lr3 is not None:
		lr3 = watch_async_progress(lr3, 'remove')
		if lr3 is not None:
			for key in lr3.keys():
				print "%20s %30s" % (key, lr3[key])

	print 'emcsps.emc_remove_lun Done'
	print
		
# main
module_folderpath_creation()
from emcsps import *
li = ["10.32.70.203", "5988", "admin", "#1Password"]
print 'Invoking emcsps.emc_get_arrays begin ...'
lun_id_created = create_lun()
create_clone(lun_id_created)
present()
unpresent()
remove_lun()
