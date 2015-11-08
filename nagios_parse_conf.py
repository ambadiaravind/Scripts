#!/usr/bin/python

import os

nagios_conf = '/home/aravind/nagios.cfg'
conf = {}
a = []

def parse_config(file) :
    """ accepts a filehandle and returns the object definitions """
    definitions=[]
    config = [ x for x in open(file).readlines()\
                         if not x.startswith('#') if x != '\n']
    config = ''.join(config)

    # dump comments
    try:
        config = config[config.index('define'):]
    except ValueError:
        return()


    # cut into chunks
    config = config.split('define ')
    # config now has one definition per element
    x=0

    # Clean lines up
    for definition in config :
        config[x]=definition.strip()
	# dump everything after the }
        config[x]=config[x][:config[x].find('}')+1]
        x=x+1

    for entry in config:
        try:
            config.remove('')
        except ValueError: break

    return (config)


def hash_objects(obj_list):
    """accept a list of object definitions and return them as a dictionary"""

    object_base=[]

    for entry in obj_list:
        # remove pesky trailing } explode the object definition for easy pickin's
        exp_obj = entry.split('\n')
        object = {}
        object['type'] = exp_obj[0][:exp_obj[0].index('{')].strip()
        # pop off the type field so as not to interfere with loop
        exp_obj.pop(0)
        for attrib in exp_obj:
            attrib = attrib.lstrip()
            attribname = attrib.split()[0]
            # some values have spaces in them so we just grab the rest of the line
            attribvalue = attrib[len(attribname):]

            # remove comments
            attribvalue = attribvalue.split(';')[0]
            attribvalue = attribvalue.strip()
            # in case closing brace is on the line with values
            attribvalue = attribvalue.split('}')[0]
            if attribname == '}' : continue
            if attribname == '#' : continue
            #poke values into hash
            object[attribname] = attribvalue

        # add complete object to list of objects
        object_base.append(object)

    return(object_base)

def get_values(file):
    objects = []
    parsed = parse_config(file)

    if parsed:
        objects.extend(parsed)

    hashed = hash_objects(objects)

    for a in hashed:
#	print a
        if a['type'] == 'hostgroup':
#	    print a
	   for mem in a['members']:
		print mem

for f in open(nagios_conf).readlines():
    if f.startswith('#'):
        continue
    else:
        if f != '\n':
            main_conf = f.rstrip().split('=')
            conf.setdefault(main_conf[0], [  ]).append(main_conf[1])
try:
    for file in conf['cfg_file']:
        if os.path.exists(file):
            get_values(file)
except:
    print "No configuration files included"

try:
    for dir in conf['cfg_dir']:
        if os.path.exists(dir):
            for file in os.listdir(dir):
                file = "%s/%s"%(dir,file)
                if os.path.exists(file):
                    get_values(file)
except:
    print "No configuration directory included"
