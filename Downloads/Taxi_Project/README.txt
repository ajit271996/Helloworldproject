1. The CloudFormtion Templates CF3.json and CF4.json can be run from command to Generated the EC2 VPC 
   with Load Balancer , Target Groups , VPC and EC2 instances for High Avaialability 
2. The source code provided can be copied to each EC2  instances (in example 2 are used for demo)
3. The required instructions to set up the Python libraries are given in file Steps_to_run_on AWS.txt
   Note that we have used both local mongo db for test purpose and Free Mongo DB Atals Cluster (URL hardcoded for EC2 run)
4. Once the Applications are run on port 8080 of each EC2 instnace , access the Load Balancer  URL  from a web browser
5. The Users and Taxis can be inserted at one go using 2 csv files given , as ssson as we hit the links and 
   click Refresh code will inser records and show  both registered users and taxis  on UI
6. The regular option to to Register a User and Taxi from a Web based Form is also available
7. To get the Users and Taxis Locations Simulated hardcoded for 5 mins , click on "Run Simulation for Taxi Locations"
8. After this A user searches for a Nearest taxi from his location , and code will return the Nearest Taxi within 1 Km of Selected Type (Or Alll)
   and also book the nearest matched taxi for the user
9. The Taxi simulated locations and user random locations are stored in mongo db atlas cluster and can be viewed on map vai charts
10. The User will get the notification for Booked taxi on his email via AWS SNS service
( Both video demo and screenshots word file are attached  for details)
11. The high level architecture diagram (Powerpoint) for AWS high availablity implementation is also attached.

   