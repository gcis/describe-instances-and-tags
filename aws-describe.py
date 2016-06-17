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
parser.add_argument('-r', '--region', action='store', help='region', default=None)

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

#setting the region is specified or using the default config if not
if args.region is not None :
   client = boto3.client(
      'ec2',
      region_name=args.region_name
   )
else : 
   client = boto3.client('ec2')

#making the request
if args.describe_tags :
   response = client.describe_tags()
   print response
else :
   response = client.describe_instances(
      Filters = tag_filters
   )



