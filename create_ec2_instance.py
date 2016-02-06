#!/usr/bin/env python


from aws_api_connections import get_ec2_connection_obj
from config.config_reader import cfg
from aws_utils import get_security_group
from aws_utils import get_vpc_subnets


def create_ec2_from_ami():

    ec2 = get_ec2_connection_obj()

    # TODO!!!  need to check for existence of this key before blindly creating it...
    print 'creating ec2 ssh key pair with name %s' % cfg['ec2_ssh_key_name']
    key = ec2.create_key_pair(cfg['ec2_ssh_key_name'])
    key.save(cfg['ec2_ssh_key_local_path'])
    print 'just saved private key pem file to %s' % cfg['ec2_ssh_key_local_path']


    security_group = get_security_group(cfg['webapp_sg_name'])
    print 'utilizing security group: %s' % security_group
    print 'security group id: %s' % security_group.id
    subnet_list = get_vpc_subnets()

    ec2.run_instances(cfg['ec2_ami'],
                      key_name=cfg['ec2_ssh_key_name'],
                      security_group_ids=[security_group.id],
                      subnet_id=subnet_list[0],
                      instance_type=cfg['ec2_instance_type'])


if __name__ == "__main__":
    create_ec2_from_ami()



# *way* more examples of shit i need to do...
# https://github.com/garnaat/paws/blob/master/ec2_launch_instance.py.