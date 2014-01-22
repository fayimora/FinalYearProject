import glob, os

rel = glob.glob("data/relevant/*")[:1800]
irr = glob.glob("data/irrelevant/*")[:1800]

for f in rel:
  os.system("cp " + f + " mpurver/relevant")

for f in irr:
  os.system("cp " +  f + " mpurver/irrelevant")

