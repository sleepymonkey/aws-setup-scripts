#!/usr/bin/env python

from boto.ec2.elb import HealthCheck

from aws_api_connections import get_elb_connection_obj
from aws_utils import get_vpc_subnets
from aws_utils import get_security_group
from config.config_reader import cfg


def create_elastic_load_balancer():
    elb_conn = get_elb_connection_obj()


    # setup availability zones to which this lb forwards requests
    ports = [(80, cfg['webapp_instance_port'], 'http'), (443, cfg['webapp_instance_port'], 'http')]
    subnets = get_vpc_subnets()
    elb_sg = get_security_group(cfg['webapp_elb_sg_name'])


    # create the load balancer.  NB:  zones must be None when associating elb to non-default vpc
    elb = elb_conn.create_load_balancer(name=cfg['elb_name'], zones=None, listeners=ports,
                                        subnets=subnets, security_groups=[elb_sg.id])


    # Add the health check configuration to the ELB.
    hc = HealthCheck(
        interval=10,
        healthy_threshold=2,
        unhealthy_threshold=3,
        target='HTTP:' + str(cfg['webapp_instance_port']) + cfg['health_check_url']
    )

    elb.configure_health_check(hc)

    print 'elastic load balancer created: ', elb
    print 'elastic load balancer dns: ', elb.dns_name

    return elb


if __name__ == "__main__":
    create_elastic_load_balancer()
