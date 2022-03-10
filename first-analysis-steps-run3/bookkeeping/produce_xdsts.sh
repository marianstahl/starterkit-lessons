## Small bash script to produce xdsts in parallel. A single input file will be processed. It is read in from a ascii file given as argument to the script
## USAGE : source produce_xdsts.sh <pfn_filename>

outdir='/data/home/mstahl/starterkit'
for i in {1..32}
do
  file=$(head -$i $1 | tail -1)
  filestub=${file##*/}
  xdstname=${filestub/xdigi/xdst}
  Moore/run gaudirun.py --option 'from Moore import options; options.input_files=["'$file'"]; options.output_file="'$outdir'/xdsts/'$xdstname'"' 'run_reconstruction_for_xdigi_to_xdst.py' 2>&1 | tee $outdir/logs/$filestub.log &
done
