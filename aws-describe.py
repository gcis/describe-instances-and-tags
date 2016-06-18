from __future__ import print_function
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

#Lets check tags and build the array for the describe request
tag_filters = []
def simplify_tags(tagname) :
   if tagname == 'asg' :
      return 'tag:aws:autoscaling:groupName'
   else :
      return 'tag:' + tagname

for i in range(len(args.tags)) :
   splitted = args.tags[i].split('=')
   if len(splitted) == 2 :
      data = {}
      data['Name'] = simplify_tags(splitted[0])
      values = splitted[1].split(',')
      data['Values'] = []
      for j in range(len(values)) :
         data['Values'].append(values[j])
      tag_filters.insert(len(tag_filters), data) 
   else :
      print('Tags were not written in the right way, You must specify tag_name=tag_value')

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
   print('')
   av_tags = []
   response = client.describe_tags()
   for i in range(len(response['Tags'])) :
      if response['Tags'][i]['Key'] not in av_tags :
         av_tags.append(response['Tags'][i]['Key'])
         print(response['Tags'][i]['Key'], '-->', end=' ')
         for j in range(len(response['Tags'])) :
            if response['Tags'][j]['Key'] == response['Tags'][i]['Key'] : 
               print(response['Tags'][j]['Value'], end=' | ')
         print('')
         print('-------------------------------------------------------------')
else :
   response = client.describe_instances(
      Filters = tag_filters
   )
   print(response)



