#!/usr/bin/env python

from create_vpc import create_vpc_in_region
from create_vpc_security_groups import create_all_security_groups
from create_rds import create_new_db_instance
from create_load_balancer import create_elastic_load_balancer


def generate_all_services():
    create_vpc_in_region()
    create_all_security_groups()
    create_new_db_instance()
    create_elastic_load_balancer()


if __name__ == "__main__":
    generate_all_services()
