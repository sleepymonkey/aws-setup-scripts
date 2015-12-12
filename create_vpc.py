#!/usr/bin/env python


import aws_api_connections

from config.config_reader import cfg

def create_vpc_in_region():
    vpc_conn = aws_api_connections.get_vpc_connection_obj()


    # create the main virtual private cloud
    vpc = vpc_conn.create_vpc(cfg['vpc_main_cidr'])  #'10.0.0.0/16')
    vpc_conn.modify_vpc_attribute(vpc.id, enable_dns_support=True)
    vpc_conn.modify_vpc_attribute(vpc.id, enable_dns_hostnames=True)

    # make sure the vpc is actually ready for the next set of operations
    # this may be overkill and can probably be deleted...
    #vpc_instance = vpc_conn.get_all_vpcs(vpc_ids=[vpc.id])[0]
    #print "vpc status: ", vpc_instance.state
    #while not vpc_instance.state == 'available':
    #    print "status is NOT available.  sleeping 5 seconds."
    #    time.sleep(5)


    # creating a brand new route table prevents association with internet gw and created subnets.
    # i'm probably doing something wrong, but the only way i got this to work is to utilize the
    # default/main route table generated as part of vpc creation
    # route_table = vpc_conn.create_route_table(vpc.id)
    route_table = None
    route_table_list = vpc_conn.get_all_route_tables()
    for rt in route_table_list:
        if rt.vpc_id == vpc.id:
            route_table = rt
            break

    print "using route table from newly created vpc: ", route_table

    # testing to see if this is needed for route/subnet association.  wtf
    #network_acl = vpc_conn.create_network_acl(vpc.id)


    # create an internet gateway and add a route to the internet to our route table
    gateway = vpc_conn.create_internet_gateway()
    vpc_conn.attach_internet_gateway(gateway.id, vpc.id)
    vpc_conn.create_route(route_table.id, '0.0.0.0/0', gateway.id)


    # create the 2 subnets in this VPC
    subnet_1 = vpc_conn.create_subnet(vpc.id, cfg['subnet_1_cidr'], availability_zone=cfg['az_1'])
    subnet_2 = vpc_conn.create_subnet(vpc.id, cfg['subnet_2_cidr'], availability_zone=cfg['az_2'])

    # now add routes to each of our subnets
    vpc_conn.associate_route_table(route_table.id, subnet_1.id)
    vpc_conn.associate_route_table(route_table.id, subnet_2.id)

    print 'created VPC: ', vpc.id
    return vpc


if __name__ == "__main__":
    create_vpc_in_region()
