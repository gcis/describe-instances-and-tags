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

default_run = not(i_ip or i_name or i_id or i_pip)

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
   if default_run : 
      print('')
   response = client.describe_instances(
      Filters = tag_filters
   )
   reservations = response['Reservations']
   for i in range(len(reservations)) :
      instances = reservations[i]['Instances']
      for j in range(len(instances)) :
         instance = instances[j]
         if raw_json :
            pprint.pprint(instance)
            print('')
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
               print(instance_name, end='')
               if default_run : 
                  print(' | ', end='')
            if default_run or i_ip :
               instance_ip = instance['PrivateIpAddress']
               print(instance_ip, end='')
               if default_run : 
                  print(' | ', end='')
            if default_run or i_id :
               instance_id = instance['InstanceId']
               print(instance_id, end='')
               if default_run : 
                  print(' | ', end='')
            if default_run or i_pip :
               instance_pip = instance['PublicIpAddress']
               print(instance_pip, end='')
               if default_run : 
                  print(' | ', end='')
            if default_run:
               print('')
               print('-----------------------------------------------------------------')           
            if not default_run:
               print('')





