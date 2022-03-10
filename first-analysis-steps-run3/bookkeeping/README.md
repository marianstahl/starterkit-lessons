# Steps to produce input files for the hands-on session

Currently available Run3 MC is listed in https://its.cern.ch/jira/browse/LHCBGAUSS-1837, where we found $`B_c^+ \to B_s^0 \mu^+ \nu / \pi^+`$ signal MC.
Their event number is 14545006 (semileptonic) 14135000 (hadronic).
Our goal is to run the current Hlt2 reconstruction and persist the reconstructed objects. This allows us to run selection studies an order of magnitude faster.

These are the bookkeeping commands we need upfront (for 14545006):
```sh
source /cvmfs/lhcb.cern.ch/lib/LbEnv
lhcb-proxy-init
lb-dirac dirac-bookkeeping-decays-path 14545006
lb-dirac dirac-bookkeeping-get-files -B '/MC/Upgrade/Beam7000GeV-Upgrade-MagUp-Nu7.6-25ns-BcVegPyPythia8/Sim10aU1/14545006/XDIGI' --OptionsFile=BcpToBs0Mup_LFNs.py
lb-dirac dirac-bookkeeping-genXMLCatalog --Options=BcpToBs0Mup_LFNs.py --NewOptions=BcpToBs0Mup_143675_PFNs.py
```

In the last step we have added the production ID 143675 to the filename to make the file uniquely identifiable. This info comes from the LFN path in the previous command.
Next, we prepare the LFNs for file-by-file parallel processing. This step is a bit cumbersome, and there might be a better way of doing this.
We open the `BcpToBs0Mup_143675_PFNs.py` file and remove everything but the plain PFN (see `BcpToBs0Mup_143675.pfns`).

We then copy over or link the script to run the current Hlt2 reconstruction `run_reconstruction_for_xdigi_to_xdst.py`, the shell script `produce_xdsts.sh` (check if everything is correctly configured for our purpose) and the PFNs `BcpToBs0Mup_143675.pfns` to our stack setup root directory. Then we can launch
```sh
source produce_xdsts.sh BcpToBs0Mup_143675.pfns
```