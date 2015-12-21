# -*- coding: UTF-8 -*-
# change power plan for windows
import subprocess
import re

pattern = re.compile(r'[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}')
plan = subprocess.check_output(["powercfg","-l"])
columns = plan.split('\r\n')
s = "381b4222-f694-41f0-9685-ff5bb260df2e"

for i in range(len(columns)):
    match = pattern.search(columns[i])
    if match:
        print match.group()
    print columns[i]
subprocess.call(["powercfg","-s",s])
#print plan
