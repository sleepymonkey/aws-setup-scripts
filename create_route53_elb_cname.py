#!/usr/bin/env python

import sys

from aws_api_connections import get_route53_connection_obj
from aws_api_connections import get_elb_connection_obj
from config.config_reader import cfg
from boto.route53.record import ResourceRecordSets


def formatDomain(domain):
    if not domain.endswith('.'):
        print 'adding period to end of domain name'
        domain += '.'

    return domain


def create_cname_to_elb(cname, elb_name=None, app_domain=None):
    cname = formatDomain(cname)

    if not elb_name:
        print 'elastic load balancer name not passed to script.  querying aws based on configuration file'
        elb_name = cfg['elb_name']
        if not elb_name:
            raise Exception("ERROR! elastic load balancer name not specified on cmd line or in configuration file")


    elb_conn = get_elb_connection_obj()
    elb = elb_conn.get_all_load_balancers(load_balancer_names=[elb_name])[0]
    print 'elb: %s' % elb

    elb_dns_name = elb.dns_name

    if not app_domain:
        app_domain = formatDomain(cfg['app_domain_name'])
    print 'adding cname to domain: %s' % app_domain

    route53 = get_route53_connection_obj()
    hosted_zone = route53.get_zone(app_domain)
    print 'hosted zone discovered: %s' % hosted_zone
    print 'zone id: %s' % hosted_zone.id
    zone_id = hosted_zone.id

    changes = ResourceRecordSets(route53, zone_id)

    change = changes.add_change("CREATE", cname, "CNAME", ttl=60)
    change.add_value(elb_dns_name)

    # try:
    changes.commit()
    # except Exception, e:
    #     logging.error(e)




        # elb_id =
        # if not elb_id:
        #     raise Exception("ERROR! domain name not specified on cmd line or in configuration file")


    # ok we have a domain name.  it must end with a period before setting it up as a hosted zone




    print 'creating route53 hosted zone from domain name %s' % cname

    #


# pass domain on the command line to override config file value.  will fall back to config file if nothing passed here
if __name__ == "__main__":
    argLength = len(sys.argv)
    if argLength < 2:
        print "\nyou must pass new cname and optionally your elastic lb name as arguments"
        print "usage: ", sys.argv[0], " cname elb_name"
        print "e.g.: ", sys.argv[0], " staging.brs.com  brs-web-lb\n"
        exit(1)

    if argLength == 2:  # just passing cname but no elb identifier
        create_cname_to_elb(sys.argv[1])
    else:  # passed both cname and elb id
        create_cname_to_elb(sys.argv[1], sys.argv[2])
