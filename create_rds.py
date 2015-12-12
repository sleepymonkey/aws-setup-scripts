#!/usr/bin/env python

import aws_api_connections
from aws_utils import get_vpc_subnets

from config.config_reader import cfg


def get_db_security_group(vpc_conn):
    sg_list = vpc_conn.get_all_security_groups()
    for sg in sg_list:
        if sg.name == cfg['database_sg_name']:
            return sg

    raise Exception("ERROR! database security group with name " + cfg['database_sg_name'] + " was not found!")


def create_new_db_instance():
    # boto.set_stream_logger('boto')  # get obnoxious amount of debug info...

    print 'creating new mysql database RDS instance in region: ', cfg['aws_region']
    vpc_conn = aws_api_connections.get_vpc_connection_obj()
    rds_conn = aws_api_connections.get_rds_connection_obj()


    # get the existing list of subnets (typically 2)
    subnet_ids = get_vpc_subnets()

    # build the subnet group for this db instance, deleting any existing group first if it exists
    subnet_group_list = rds_conn.get_all_db_subnet_groups()
    for subnet_group in subnet_group_list:
        if subnet_group.name == cfg['db_subnet_name']:
            print "existing db subnet group will be deleted: " + subnet_group.name
            rds_conn.delete_db_subnet_group(cfg['db_subnet_name'])

    rds_conn.create_db_subnet_group(cfg['db_subnet_name'], 'group of private subnets in vpc', subnet_ids)


    # find the db security group we defined as part of the creating the vpc security groups
    db_security_group = get_db_security_group(vpc_conn)
    print "utilizing db security group: " + str(db_security_group)


    # with subnet group and db security group collected, issue the call to create the rds instance
    rds_conn.create_dbinstance(cfg['db_instance_id'], 10, 'db.t2.micro', cfg['db_user'], cfg['db_pwd'],
                               engine='MySQL',
                               port=3306,
                               db_name=cfg['db_name'],
                               availability_zone=None,
                               multi_az=False,
                               engine_version='5.6',
                               auto_minor_version_upgrade=False,
                               vpc_security_groups=[db_security_group.id],
                               db_subnet_group_name = cfg['db_subnet_name'])


if __name__ == "__main__":
    create_new_db_instance()
