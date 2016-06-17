import boto3
import sys, argparse
import json


parser = argparse.ArgumentParser(description='Describe AWS Ec2 resources')
parser.add_argument('-d', '--describe-tags', action='store_true', help='describe tags parameter', default=False)
parser.add_argument('-t', '--tags', action='store', nargs='+', help='tag or tags to descibe', default=[])
parser.add_argument('-ip', '--get-ip-address', action='store_true', help='returns just ip addresses', default=False)
parser.add_argument('-n', '--get-instance-name', action='store_true', help='returns just ip addresses', default=False)
parser.add_argument('-id', '--get-instance-id', action='store_true', help='returns just ip addresses', default=False)
parser.add_argument('-sg', '--get-security-group', action='store_true', help='returns just ip addresses', default=False)
parser.add_argument('-v', '--verbose', action='store_true', help='returns just ip addresses', default=False)
parser.add_argument('-r', '--region', action='store_true', help='region', default=False)

args = parser.parse_args()
print args

#Lets check tags and build the array for the describe request
tag_filters = []
def simplify_tags(tagname) :
   if tagname == 'asg' :
      return 'tag:aws:autoscaling:groupName'
   else :
      return tagname

for i in range(len(args.tags)) :
   splitted = args.tags[i].split('=')
   if len(splitted) == 2 :
      data = {}
      data['Name'] = simplify_tags(splitted[0])
      data['Values'] = splitted[1]
      json_data = json.dumps(data)
      tag_filters.append(json_data) 
   else :
      print 'Tags were not written in the right way, You must specify tag_name=tag_value'

print tag_filters

client = boto3.client(
   'ec2',
   region_name=args.region_name
)

if args.describe_tags :
   response = client.describe_tags()
   print response
else :
   response = client.describe_instances(
      Filters = tag_filters
   )


# inputfile = ''
# outputfile = ''
# try:
#    opts, args = getopt.getopt(argv,"divt:o:",["describe-tags","ip-address","verbose","tag=","ofile="])
# except getopt.GetoptError:
#    print 'test.py -i <inputfile> -o <outputfile>'
#    sys.exit(2)
# for opt, arg in opts:
#    if opt in ("-d", "--describe-tags"):
#       print 'describe tags'
#       sys.exit()
#    elif opt in ("-i", "--ifile"):
#       inputfile = arg
#    elif opt in ("-o", "--ofile"):
#       outputfile = arg
# print 'Input file is "', inputfile
# print 'Output file is "', outputfile


