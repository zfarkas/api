#!/usr/bin/env python

# Copyright (C) 2015 MTA SZTAKI

"""
Common code used in use-case scripts for OCCO

Author: adam.visegradi@sztaki.mta.hu
"""

import occo.util.config as config
import occo.util as util
import occo.infobroker
import occo.infobroker.cloud_provider
import occo.infobroker.uds
import occo.cloudhandler
import occo.cloudhandler.backends.boto
import occo.infraprocessor
import yaml

def init():
    #
    ## Find and load main config file
    #
    cfg = config.DefaultConfig(dict(cfg=None))
    cfg.add_argument(name='--cfg', dest='cfg_path', type=util.cfg_file_path)
    cfg.add_argument('node_def')
    cfg.parse_args()

    if not cfg.cfg_path:
        possible_locations = util.file_locations('occo.yaml',
            '.',
            util.curried(util.rel_to_file, basefile=__file__),
            util.cfg_file_path)

        cfg.cfg_path = util.path_coalesce(*possible_locations)

    with open(cfg.cfg_path) as f:
        cfg.configuration = yaml.load(f)

    #
    ## Setup logging
    #
    import os
    import logging
    import logging.config
    logging.config.dictConfig(cfg.configuration['logging'])

    log = logging.getLogger('occo')
    log.info('Staring up; PID = %d', os.getpid())

    #
    ## Bootstrap infastructure
    #
    infra = cfg.configuration['infrastructure']
    infra['infobroker'].sub_providers = infra['sub_providers']


    return cfg
