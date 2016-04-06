#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initial stab at ISPAQ script.

This version runs from command line arguments only and assumes that we are 
connected to the internet.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import argparse

from ispaq.irismustangmetrics import *

###from ispaq.utils.misc import *

from ispaq.concierge.user_request import UserRequest
from ispaq.concierge.concierge import Concierge

from ispaq.business_logic.simple_metrics import generate_simple_metrics

import pandas as pd

import sys

from os.path import expanduser

import obspy

__version__ = "0.0.2"


def main(argv=None):
    
    # Parse arguments ----------------------------------------------------------
    
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s ' + __version__)
    # parser.add_argument('--example-data', action='store_true', default=False,
    #                     help='use example data from local disk')
    parser.add_argument('--start', action='store', required=True,
                        help='starttime in ISO 8601 format')
    parser.add_argument('--end', action='store', required=False,
                        help='endtime in ISO 8601 format')
    parser.add_argument('-M', '--metrics', required=True,
                        help='name of metric to calculate')
    parser.add_argument('-S', '--sncls', action='store', default=False,
                        help='Network.Station.Location.Channel identifier (e.g. US.OXF..BHZ)')
    parser.add_argument('-P', '--preferences-file', default=expanduser('~/.irispref'),
                        type=argparse.FileType('r'), help='location of preference file')
    parser.add_argument('-O', '--output-loc', default='.',
                        help='location to output ')

    # TODO:  additional configurable elements like sigfigs should be in the preferences file
    # parser.add_argument('--sigfigs', type=check_negative, default=6,
    #                     help='number of significant figures to round metrics to')

    args = parser.parse_args(argv)
    

    #     Create UserRequest object     ---------------------------------------
    #
    # The UserRequest class is in charge of parsing arguments issued on the
    # command line, loading and parsing a preferences file, and setting a bunch
    # of properties that capture the totality of what the user wants in a single
    # invocation of the ISPAQ top level script.

    try:
        user_request = UserRequest(args.start, args.end, args.metrics, args.sncls, args.preferences_file)
        ###print(user_request.json_dump(pretty=True))
    except Exception as e:
        if str(e) == "Not really an error.":
            pass
        else:
            raise

    # Create Concierge (aka Expediter) -----------------------------------------
    #
    # The Concierge class uses the completely filled out UserRequest and has the
    # job of expediting requests for information that may be made by any of the
    # business_logic methods. The goal is to have business_logic methods that can
    # be written as clearly as possible without having to know about the intricacies
    # of ObsPy.
  
    try:
        concierge = Concierge(user_request)
    except Exception as e:
        if str(e) == "Not really an error.":
            pass
        else:
            raise


    # Generate Simple Metrics --------------------------------------------------

    try:
        simple_df = generate_simple_metrics(concierge, verbose=True)
        try:
            print('Dumping to a file')
            simple_df = simpleMetricsPretty(simple_df, sigfigs=6)
            print(simple_df)
        except:
            print('Exception to dump to a file')
    except Exception as e:
        print(str(e))


    # Generate SNR Metrics -----------------------------------------------------

    #try:
      #snr_output = ispaq.business_logic.generate_SNR_metrics(concierge)
      #try:
          ## Dump output to a file
      #except:
          ##
    #except:
          ##


    # Generate [increasingly complex/time-consuming metrics] -------------------

    #try:
      #complex_output = ispaq.business_logic.generate_complex_metrics(concierge)
      #try:
          ## Dump output to a file
      #except:
          ##
    #except:
          ##
    
        
    # Cleanup ------------------------------------------------------------------

if __name__ == "__main__":
    main()