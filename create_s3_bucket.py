#!/usr/bin/env python

import sys

from aws_api_connections import get_s3_connection_obj


def create_s3_bucket(bucket_name):


    s3_conn = get_s3_connection_obj()
    bucket = s3_conn.create_bucket(bucket_name)

    print 'bucket created: ', bucket
    return bucket


if __name__ == "__main__":
    # must pass the bucket name to this script
    argLength = len(sys.argv)
    if argLength < 2:
        print "\nyou must pass bucket name as single argument"
        print "usage: ", sys.argv[0], " some-bucket-name \n"
        exit(1)

    create_s3_bucket(sys.argv[1])
