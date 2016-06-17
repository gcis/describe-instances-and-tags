import boto3
import sys, getopt

def main(argv=None):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"divt:o:",["describe-tags","ip-address","verbose","tag=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-d", "--describe-tags"):
         print 'describe tags'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile

if __name__ == "__main__":
   sys.exit(main())
   
