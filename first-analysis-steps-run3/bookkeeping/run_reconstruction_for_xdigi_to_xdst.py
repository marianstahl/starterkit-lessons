###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Run the reconstruction on an xdigi file with PersistReco through a
pass-through line (defined with `algs=[]`). This will produce an xdst file
containing the reconstructed objects and MC info.

Run e.g. like this:
Moore/run gaudirun.py --option='from Moore import options; options.input_files=["/data/home/mstahl/starterkit/BcpToBs0Pip/00143671_00000001_1.xdigi"];options.output_file="/data/home/mstahl/starterkit/BcpToBs0Pip/00143671_00000001_1.dst"' run_reconstruction_for_xdigi_to_xdst.py
or use the shell script (produce_xdsts.sh).
"""
from Moore import (options, run_moore)
from Moore.tcks import dump_hlt2_configuration
from Moore.lines import Hlt2Line
from RecoConf.reconstruction_objects import reconstruction
from RecoConf.global_tools import (stateProvider_with_simplified_geom, trackMasterExtrapolator_with_simplified_geom)
from RecoConf.hlt2_global_reco import reconstruction as hlt2_reconstruction, make_fastest_reconstruction
from RecoConf.hlt1_tracking import default_ft_decoding_version

options.input_type = "ROOT"
options.input_raw_format = 0.5

default_ft_decoding_version.global_bind(value=6)

options.evt_max = -1
options.simulation = True
options.data_type = "Upgrade"
options.dddb_tag = "dddb-20210617"
options.conddb_tag = "sim-20210617-vc-mu100"

options.output_type = "ROOT"
options.msg_svc_format = "% F%56W%S%7W%R%T %0W%M"

def pass_through_line(name="Hlt2Line"):
    """Return a HLT2 line that performs no selection but runs and persists the reconstruction
    """
    return Hlt2Line(name=name, prescale=1, algs=[], persistreco=True)

def make_lines():
    return [pass_through_line()]

public_tools = [trackMasterExtrapolator_with_simplified_geom(), stateProvider_with_simplified_geom()]
with reconstruction.bind(from_file=False), hlt2_reconstruction.bind(make_reconstruction=make_fastest_reconstruction):
    config = run_moore(options, make_lines, public_tools)
dump_hlt2_configuration(config, "hlt2_passthrough_persistreco_BcpToBs0Mup.tck.json")