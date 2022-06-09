# Extract data from influxDB and get the url
# With the url extracted, automate the comment using bitbucket API

import argparse
from datetime import datetime
import pytz
import requests
import pandas as pd
import json
import time

influx_database_name = "autostatus_prod"
influx_query_url = f'http://xxxxxx.xxxxxx.co.kr:8086/query?db={influx_database_name}'
table_name = "job"

def str2bool(v):
    if v.lower() in ('True', 'TRUE', 'yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('False' , 'FALSE' 'no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def convert_utc(date_string):
    dt_strptime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

    tz_kst = pytz.timezone('Asia/Seoul')
    dt_kst = tz_kst.localize(dt_strptime)

    dt_utc_from_kst = dt_kst.astimezone(pytz.utc)
    return dt_utc_from_kst.strftime('%Y-%m-%d %H:%M:%S')

def time_parse(time_):
    date = time_.split(' ')[0]
    time = time_.split(' ')[1]
    return date, time

def query_compose(table_name,job_name,start_date,start_time,end_date,end_time):
    query_string = f'''
    SELECT * FROM {table_name}
    WHERE jobname =~ /.*{job_name}.*/
    AND ( result =~ /Error/)
    AND time >= '{start_date}T{start_time}Z' AND time <= '{end_date}T{end_time}Z'
    '''
    payload = {'q': query_string}
    return payload

def request_influx_Data(influx_query_url, payload):
    influxData = requests.get(url=influx_query_url, params=payload).json()
    return influxData

def get_url(influxData):
    col = influxData['results'][0]['series'][0]['columns']
    data = influxData['results'][0]['series'][0]['values']

    dat = pd.DataFrame.from_dict(data)
    dat.columns = col

    if(job_name == 'xxxxx_PLATFORM'):
        dat = dat[~dat['repo'].str.contains("xxxxxxxx_TEST")]
        dat.reset_index(inplace=True,drop=False)

    # List of '#RUN_CI' needed jobs
    print(dat[['time','owner','repo','result']])
    return dat


def get_package_and_pr(url):
    package_name = url.owner.str.split('/', expand=True)
    pr_no = url.repo.str.split('-', expand=True)
    return package_name, pr_no

def put_comment(job_name, package_name, pr_no, dry_run, username, password):
    headers = {'content-type': 'application/json'}
    comment = '#RUN_BUILD'
    sum = 0
    for ind in range(0,len(package_name)):
        sum += 1
        if(job_name == 'xxxxx_PLATFORM'):
            commentLink = f'https://xxxxxx.com/rest/api/1.0/projects/{job_name}/repos/{package_name[1][ind]}/pull-requests/{pr_no[1][ind]}/comments'
        else:
            commentLink = f'https://xxxxxxxx.xxxxx.co.kr/rest/api/1.0/projects/{name[1][ind]}/repos/{package_name[2][ind]}/pull-requests/{pr_no[1][ind]}/comments'

        if dry_run is False:
            res = requests.post(commentLink, auth=(username,password), headers=headers, data=json.dumps({"text": comment }))

        time.sleep(api_call_sleep)

    if dry_run:
        print(f'{sum} of jobs were done with dry_run')
    else:
        print(f'{sum} of jobs were done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do #RUN_CI for the all jobs in specific time frame')
    parser.add_argument('--base_url', type=str, help='Bitbucket base URL : https://xxxxxxx.xxxxx.co.kr/projects or https://xxxxxx.com/projects', required=True)
    parser.add_argument('--job_name', type=str, help='job name : xxxxxx_PLATFORM or ABC or DEF', required=True)
    parser.add_argument('--username', type=str, help='Bitbucket username with repo admin permissions', required=True)
    parser.add_argument('--password', type=str, help='Bitbucket Password', required=True)
    parser.add_argument('--start_datetime', type=str, help='start_datetime (yyyy-mm-dd hh:mm:ss)', required=True)
    parser.add_argument('--end_datetime', type=str, help='end_datetime (yyyy-mm-dd hh:mm:ss)', required=True)
    parser.add_argument('--dry_run', default=True, type=str2bool, help='to disable dry run option, input False' required=True)
    parser.add_argument('--sleep', type=float, help='Sleep between API calls, default is 0.01 (s)', required=False, default=0.01)

    # input parameter to variables
    args = parser.parse_args()
    job_name = args.job_name
    username = args.username
    password = args.password
    start_datetime = args.start_datetime
    end_datetime = args.end_datetime
    dry_run = args.dry_run
    api_call_sleep = args.sleep

    # date time parsing
    start_date, start_time = time_parse(convert_utc(start_datetime))
    end_date, end_time = time_parse(convert_utc(end_datetime))

    # compose influx query string
    query_string = query_compose(table_name,job_name,start_date,start_time,end_date,end_time)

    # request influx data
    influxData = request_influx_Data(influx_query_url, query_string)

    # get url data from influx data
    url = get_url(influxData)

    # parse package_name and PR number
    package_name, pr_no = get_package_and_pr(url)

    # put comment on extracted package_name and PR number
    put_comment(job_name, package_name, pr_no, dry_run, username, password)
