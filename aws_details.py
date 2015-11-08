#!/usr/bin/python

from pprint import pprint
from boto import ec2

awsky = {'AasdaA' : 't0asdG',\
	 'AKdfawqZ7AA' : 'tasfdsadasda',\
         'asfsafqwfqad' : '7sadadawDm' }

i = 0
opts = {}

for key in awsky:
    AWS_ACCESS_KEY_ID = key
    AWS_SECRET_ACCESS_KEY = awsky[key]    

    regions = ['us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1',
                		'ap-southeast-1','ap-southeast-2','ap-northeast-1']

    if key == "AasdaA":
        print "ABC"
    elif key == "AKdfawqZ7AA":
        print "HEL"
    else:
        print "IT"
       
    for reg in regions:
    
  	ec2_region = ec2.get_region(aws_access_key_id=AWS_ACCESS_KEY_ID,\
				aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name=reg)
        ec2conn = ec2.connection.EC2Connection(aws_access_key_id=key,\
				aws_secret_access_key=awsky[key],region=ec2_region)
        reservations = ec2conn.get_all_instances()

        for r in reservations:
            for inst in r.instances:
		print inst
                opts[i] = (inst.id, inst.instance_type, inst.tags['Name'], inst.state)
                print "\t%d:" % i + "%s - %s - \"%s\" - %s " % opts[i]
                i += 1
