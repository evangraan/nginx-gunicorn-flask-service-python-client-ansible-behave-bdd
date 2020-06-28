from behave import *
import time
import subprocess
import re
import requests
import json

def view_last_record(context):
    headers = {"Content-type": "application/json", "Accept": "text/plain", "Authorization": "Bearer " + context.token}
    r = requests.get(context.url + "/api/test/latest", headers=headers, verify=False)
    return json.loads(r.text)['data']

def find_last_record(context):
    return view_last_record(context)['filename']

def check_records(context):
    headers = {"Content-type": "application/json", "Accept": "text/plain", "Authorization": "Bearer " + context.token}
    r = requests.get(context.url + "/api/test/count", headers=headers, verify=False)
    return json.loads(r.text)['data']['count']

@given(u'a client running')
def step_impl(context):
   context.client_ip = '192.168.1.225'
   context.client_uuid = 'a9201032-1e1f-40a2-8995-8472a76dd7d2'

@given(u'a service API running')
def step_impl(context):
    context.api_ip = '192.168.1.224'
    context.url = 'https://' + context.api_ip

@given(u'client credentials')
def step_impl(context):
    pass

@given(u'service API credentials')
def step_impl(context):
    context.token = 'my3m45hl;kw4hn900bdfnb9fegherjyerlgjHWRTHRThp0qerh!;lfdskfgjsdjgpb9e09-$'

@given(u'enough time for records to have been reported')
def step_impl(context):
    context.existing_records = check_records(context)
    time.sleep(21)

@when(u'I check the service API records repository')
def step_impl(context):
    context.latest_records = check_records(context)

@then(u'I see the correct amount of records')
def step_impl(context):
    assert(int(context.latest_records) >= int(context.existing_records) + 4)

@then(u'the records have the client uuid')
def step_impl(context):
    print(find_last_record(context))
    assert(context.client_uuid in find_last_record(context))

@then(u'the records are timestamped')
def step_impl(context):
    filename = find_last_record(context)
    assert(len(re.findall("\d{10}\.\d{7}", filename)) > 0)


@then(u'the records contain JSON process lists')
def step_impl(context):
    content = str(view_last_record(context))
    assert("memory_info" in content)