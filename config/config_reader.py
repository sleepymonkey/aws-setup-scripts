#!/usr/bin/env python

import os
import sys
import ConfigParser
import StringIO


try:
    config_file = os.environ['AWS_CONFIG_FILE']
except:
    print '\nyou must specify a config file location as env variable AWS_CONFIG_FILE'
    print 'e.g. export AWS_CONFIG_FILE=/tmp/aws-config \n'
    sys.exit(2)


# sigh.  configparser requires at least one 'section', so fake that here.  annoying.
bunk_section = 'root'
cfg_str = '[' + bunk_section + ']\n' + open(config_file, 'r').read()
cfg_fp = StringIO.StringIO(cfg_str)

# config = ConfigParser.RawConfigParser()
config = ConfigParser.ConfigParser()
# config = ConfigParser.SafeConfigParser()
config.readfp(cfg_fp)


# with the parsing out of the way, create a simple map that calling scripts will import
cfg = {}
keys = config.options(bunk_section)
for key in keys:
    # try:
        cfg[key] = config.get(bunk_section, key, 0)
        # if dict1[option] == -1:
    # except:
    #     print("exception on %s!" % key)
    #     cfg[key] = None


print "cfg dict: ", cfg