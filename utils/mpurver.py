import glob, os

rel = glob.glob("data/relevant/*")[:1800]
irr = glob.glob("data/irrelevant/*")[:1800]
print "Done globbing"

for f in rel:
  os.system("cp %s data_3600/relevant" % f)
print "Done copying relevant files"

for f in irr:
  os.system("cp %s data_3600/irrelevant" % f)
print "Done copying irrelevant files"
