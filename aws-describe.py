from __future__ import print_function
import boto3
import sys, argparse, json, pprint


parser = argparse.ArgumentParser(description='Describe AWS Ec2 resources')
parser.add_argument('-d', '--describe-tags', action='store_true', help='describe tags parameter', default=False)
parser.add_argument('-t', '--set-tags', action='store', nargs='+', help='tag or tags to descibe', default=[])
parser.add_argument('-ip', '--get-ip-address', action='store_true', help='returns ip addresses', default=False)
parser.add_argument('-n', '--get-instance-name', action='store_true', help='returns instance-name', default=False)
parser.add_argument('-id', '--get-instance-id', action='store_true', help='returns instance-id', default=False)
parser.add_argument('-pub', '--get-public-ip', action='store_true', help='returns public ip ', default=False)
parser.add_argument('-r', '--set-region', action='store', help='region', default=None)
parser.add_argument('-j', '--json-raw-output', action='store_true', help='raw output in json', default=False)
parser.add_argument('-mx', '--max-count', action='store', type=int, help='max number of instances to show', default=0)
parser.add_argument('-div', '--divider', action='store', help='character that divides values', default=None)
parser.add_argument('-e', '--end-of-line', action='store', help='character that divides values', default='\n')

args = parser.parse_args()
#assign args to variables
d_tags = args.describe_tags
s_tags = args.set_tags
i_ip = args.get_ip_address
i_name = args.get_instance_name
i_id = args.get_instance_id
i_pip = args.get_public_ip
region = args.set_region
raw_json = args.json_raw_output
max_count = args.max_count
div = args.divider
eol = args.end_of_line

#bootstrap
default_run = not(i_ip or i_name or i_id or i_pip)
instances_to_print = []
def count_parameters() :
   par = 0
   if i_ip : par += 1
   if i_name : par += 1
   if i_id : par += 1
   if i_pip : par += 1
   return par
param_count = count_parameters()

#Lets check tags and build the array for the describe request
tag_filters = []
def simplify_tags(tagname) :
   if tagname == 'asg' :
      return 'tag:aws:autoscaling:groupName'
   else :
      return 'tag:' + tagname

for i in range(len(s_tags)) :
   splitted = s_tags[i].split('=')
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


#Print function for instances
def print_instances(instances_to_print) :
   divider = div if div is not None else ' | '
   divider = divider if param_count > 1 else ''
   print_range = max_count if max_count > 0 else len(instances_to_print)
   for i in range(print_range) :
      instance = instances_to_print[i]
      if raw_json : pprint.pprint(instance)
      else :
         instance_ip = ''
         instance_name = ''
         instance_id = ''
         instance_pip = ''
         if default_run or i_name :
            for k in range(len(instance['Tags'])) :
               curr_tag = instance['Tags'][k]
               if curr_tag['Key'] == 'Name' : 
                  instance_name = curr_tag['Value']
               else :
                  instance_name = 'NO name'
         if default_run or i_ip : instance_ip = instance['PrivateIpAddress']
         if default_run or i_id : instance_id = instance['InstanceId']
         if default_run or i_pip : instance_pip = instance['PublicIpAddress']
         print(instance_name, instance_id, instance_ip, instance_pip, sep=divider, end=eol)
         if default_run or param_count > 1 : print('-------------------------------------------------------------')

#Print Function for tags
def print_tags(tags_response) :
   av_tags = []
   for i in range(len(tags_response)) :
      if tags_response[i]['Key'] not in av_tags :
         av_tags.append(tags_response[i]['Key'])
         print(tags_response[i]['Key'], '-->', end=' ')
         for j in range(len(tags_response)) :
            if tags_response[j]['Key'] == response['Tags'][i]['Key'] : 
               print(tags_response[j]['Value'], end=' | ')
         print('')
         print('-------------------------------------------------------------')


#setting the region is specified or using the default config if not
if region is not None :
   client = boto3.client(
      'ec2',
      region_name=region
   )
else : 
   client = boto3.client('ec2')

#making the request
if d_tags :
   print('')
   response = client.describe_tags()
   print_tags(response['Tags'])
else :
   if default_run : 
      print('')
   response = client.describe_instances(
      Filters = tag_filters
   )
   reservations = response['Reservations']
   for i in range(len(reservations)) :
      instances = reservations[i]['Instances']
      for j in range(len(instances)) :
         instances_to_print.insert(len(instances_to_print), instances[j])
   print_instances(instances_to_print)





