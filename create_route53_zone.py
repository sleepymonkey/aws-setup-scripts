#!/usr/bin/env python

import sys

from aws_api_connections import get_route53_connection_obj
from config.config_reader import cfg


def create_hosted_zone(domain=None):

    if not domain:
        print 'domain not passed to script.  attempting to read from configuration file'
        domain = cfg['app_domain_name']
        if not domain:
            raise Exception("ERROR! domain name not specified on cmd line or in configuration file")

    # ok we have a domain name.  it must end with a period before setting it up as a hosted zone
    if not domain.endswith('.'):
        print 'adding period to end of domain name'
        domain += '.'

    print 'creating route53 hosted zone from domain name %s' % domain
    route53 = get_route53_connection_obj()
    zone = route53.create_zone(domain)


# pass domain on the command line to override config file value.  will fall back to config file if nothing passed here
if __name__ == "__main__":
    argLength = len(sys.argv)
    if argLength > 1:
        create_hosted_zone(sys.argv[1])
    else:
        create_hosted_zone()
