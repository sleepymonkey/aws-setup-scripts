#!/usr/bin/env python

from aws_api_connections import get_vpc_connection_obj
from aws_utils import get_region_non_default_vpc
from aws_utils import get_security_group

from config.config_reader import cfg


# global vpc connection used throughout this script
conn = get_vpc_connection_obj()


def create_all_security_groups():
    vpc = get_region_non_default_vpc()
    vpc_id = vpc.id

    # db sg has dependency on webapp sg, so need to delete it first
    delete_security_group(cfg['database_sg_name'])
    delete_security_group(cfg['webapp_sg_name'])
    delete_security_group(cfg['webapp_elb_sg_name'])

    create_webapp_sg(vpc_id)
    create_database_sg(vpc_id)
    create_elastic_load_balancer_sg(vpc_id)


def delete_security_group(sg_name):
    sg = get_security_group(sg_name)
    if sg:
        print "deleting security group: " + sg.name
        sg.delete()


def create_webapp_sg(vpc_id):
    w_sg = conn.create_security_group(cfg['webapp_sg_name'], 'security group for web application', vpc_id=vpc_id)
    print "web app security group just created. name: %s  id: %s" % (w_sg.name, w_sg.id)

    # ingress rules
    w_sg.authorize(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip=cfg['vpc_main_cidr'])  #'10.0.0.0/16')
    w_sg.authorize(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip=cfg['user_home_ip'] + '/32')
    w_sg.authorize(ip_protocol='tcp', from_port=cfg['webapp_instance_port'], to_port=cfg['webapp_instance_port'], cidr_ip=cfg['vpc_main_cidr'])  #'10.0.0.0/16')
    w_sg.authorize(ip_protocol='tcp', from_port=cfg['webapp_instance_port'], to_port=cfg['webapp_instance_port'], cidr_ip=cfg['user_home_ip'] + '/32')

    # egress rules
    # stupid.  the only way to remove the default 'All' egress rule...
    conn.revoke_security_group_egress(w_sg.id, '-1', from_port="0", to_port="65535", cidr_ip='0.0.0.0/0')
    conn.authorize_security_group_egress(w_sg.id, 'tcp', from_port=80, to_port=80, cidr_ip='0.0.0.0/0')
    conn.authorize_security_group_egress(w_sg.id, 'tcp', from_port=443, to_port=443, cidr_ip='0.0.0.0/0')
    conn.authorize_security_group_egress(w_sg.id, 'tcp', from_port=3306, to_port=3306, cidr_ip=cfg['subnet_1_cidr'])  #'10.0.0.0/24')
    conn.authorize_security_group_egress(w_sg.id, 'tcp', from_port=3306, to_port=3306, cidr_ip=cfg['subnet_2_cidr'])  #'10.0.1.0/24')


def create_database_sg(vpc_id):
    db_sg = conn.create_security_group(cfg['database_sg_name'], 'security group for rds', vpc_id=vpc_id)
    print "rds security group just created. name: %s  id: %s" % (db_sg.name, db_sg.id)

    # stupid.  the only way to remove the default 'All' egress rule...
    conn.revoke_security_group_egress(db_sg.id, '-1', from_port="0", to_port="65535", cidr_ip='0.0.0.0/0')

    # only allow instances associated with the webapp security group to access our db instance
    webapp_sg = get_security_group(cfg['webapp_sg_name'])
    db_sg.authorize(ip_protocol='tcp', from_port=3306, to_port=3306, cidr_ip=None, src_group=webapp_sg)



def create_elastic_load_balancer_sg(vpc_id):
    elb_sg = conn.create_security_group(cfg['webapp_elb_sg_name'], 'security group for elastic load balancer', vpc_id=vpc_id)
    print "elastic lb security group just created. name: %s  id: %s" % (elb_sg.name, elb_sg.id)

    elb_sg.authorize(ip_protocol='tcp', from_port=80, to_port=80, cidr_ip='0.0.0.0/0')
    elb_sg.authorize(ip_protocol='tcp', from_port=443, to_port=443, cidr_ip='0.0.0.0/0')


def print_permission(rules):
    for rule in rules:
        print "protocol: " + str(rule.ip_protocol)
        print "from port " + str(rule.from_port)
        print "to port " + str(rule.to_port)


if __name__ == "__main__":
    create_all_security_groups()
