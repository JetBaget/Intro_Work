import requests
from subprocess import Popen, PIPE
import logging

call_param = {'aim':'python_developer_job'} #set parameter for GET-inquiry
response = requests.get('http://gptl.ru/interview_task/api/commands',
                                                 params = call_param) #calling GET-inquiry
input_data = response.json()['data'] #extract useful data from response

new_proc = Popen( input_data, shell = True, stdout = PIPE, stderr = PIPE ) #create subprocess
new_proc.wait() #waiting for subprocess execution
res = new_proc.communicate() #get tuple with stdout and stderr

if input_data != '' and res[0] == '': #case of incorrect command processing
    output_data = res[1]
else:
    output_data = res[0]

logging.basicConfig (format='%(message)s', filename='logfile.log',
                                              level = logging.INFO) #set logging config
logging.getLogger ("urllib3").setLevel (logging.WARNING) #except 'urllib3' from log
logging.info (output_data) #add results in log-file

payload = {'command' : input_data, 'result' : output_data } #data for sending to the server
push = requests.post ('http://gptl.ru/interview_task/api/commands',
                                                      data = payload) #call POST-inquiry

