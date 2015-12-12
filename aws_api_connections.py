#!/usr/bin/env python

import boto.ec2
import boto.vpc
import boto.rds
import boto.ec2.elb

from config.config_reader import cfg


#conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)


def get_vpc_connection_obj():
    c = boto.vpc.connect_to_region(region_name=cfg['aws_region'],
                                   aws_access_key_id=cfg['aws_access_key'],
                                   aws_secret_access_key=cfg['aws_secret_key'])
    return c


def get_ec2_connection_obj():
    c = boto.ec2.connect_to_region(region_name=cfg['aws_region'],
                                   aws_access_key_id=cfg['aws_access_key'],
                                   aws_secret_access_key=cfg['aws_secret_key'])
    return c


def get_rds_connection_obj():
    c = boto.rds.connect_to_region(region_name=cfg['aws_region'],
                                   aws_access_key_id=cfg['aws_access_key'],
                                   aws_secret_access_key=cfg['aws_secret_key'])
    return c


def get_elb_connection_obj():
    c = boto.ec2.elb.connect_to_region(region_name=cfg['aws_region'],
                                   aws_access_key_id=cfg['aws_access_key'],
                                   aws_secret_access_key=cfg['aws_secret_key'])
    return c


