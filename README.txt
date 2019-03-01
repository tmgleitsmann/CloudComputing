DUNDER MIFFLIN FILES FOR SUFS

client.py: 
- Client command line program. 

manageEC2.py: 
- Holds functions for creating, deleting and getting info for EC2 instances.

main.py: 
- Calls on functions from "manageEC2.py" 

testSend.py: 
- An attempt to get basic communication going using SQS

testReceive.py: 
- An attempt to get basic communication going using SQS

sufs
-sufs
--settings.py: 
  -changing settings and configurations
--urls.py: 
  -mapping for different urls where we will send users. incharge of routing within APPS
--wsgi.py: 
  -how our python web app and web server communicate. Django sets up a default.
  
-sufs_app
--views.py:
  -generate http responses that we will route to urls.py
--urls.py:
  -incharge of linking backend processes to browsers using paths
--models.py
--tests.py
--apps.py
--admin.py

Other: 
- boto3test.py
- SampleText.txt
