# Introduction
The thingscope 23-Spring project turned the previous versions of the code into a dockerized container which could be easily distributed to students at Columbia and other universities such that dependency management would not be required to spin up the systems. 

# Known Issues
- Nginx server times out after 60 seconds. For processing large files, access the python agent directly using localhost:5000/agent
- Schema changes that were made to support different endpoints per run were only made to the python agent, they still need to be made to the web client controller. Additional FE changes will likely be required to the web client in parallel

# Infrastructure Changes
- Introduction of docker-compose and docker files to manage the automated building and deploying of each individual image
- Combine the agent, database, and web client into a single stack. Instead of local processing by an agent and a cloud based database and web client, one stack deployed in the cloud allows for the upload, processing, and display of a pcap file and its analysis
- Creation of 2 AWS templates: A lambda template for a pcap processor, and a full EC2 template to deploy the processing agent, web client, and database

## Python Agent Changes
- New Flask module to allow the serving of the python functions to a web client
- Refactoring out the dependency on pycurl to reduce the need for openssl installations, which had blocked the building of the agent for most of the students in the 23-Spring course
- Refactoring direct references to packet arrays into scapy library calls
- Moving print statements to python's native logging
- Modifying sink schema to support composite keys made up of the device and the individual pcap run, allowing a programmatic comparison of two different semester's analysis in the same system

## Web Client Changes
- The Spring 2021 web client is built as part of this docker image. It does not currently have the ability to read the database's new schema, this is needed work

# Schema Updates
In this version of thingscope, multiple pcap files for the same device are stored separately, this allows for independent runs from different times to be compared. While no formal schema exists, the python agent and web server that interface with the database do so under the following structure:

## Devices
Primary key: name of a specific device run.
```json
  {
    "_id": "S23_EmporiaPlug",
    "mac_addr": "10:52:1c:42:15:b2"
  },
  {
    "_id": "S23_EufyCamera",
    "mac_addr": "8c:85:80:3a:4e:4f"
  }
```
## Endpoints
Primary Composite Key: device run ID and IP address
```json
 {
    "_id": {
      "ip": "18.223.118.122",
      "name": "S23_EmporiaPlug"
    },
    "device_mac": "10:52:1c:42:15:b2",
    "domain_name": "fwsrv.emporiaenergy.com.",
    "ip": "18.223.118.122",
    "location": {
      "city": "Columbus",
	//...
```
## Domains
Primary Composite Key: device run ID and domain url
```json
  {
    "_id": "{'name': 'S23_EmporiaPlug', 'domain': 'prod-mqtt.emporiaenergy.com.'}",
    "cnames": [
      "a2poo8btpqc3gs-ats.iot.us-east-2.amazonaws.com."
    ]
  },
  {
    "_id": "{'name': 'S23_EufyCamera', 'domain': 'time.nist.gov.'}",
    "cnames": [
      "ntp1.glb.nist.gov."
    ]
  },
```
# Docker Stack
This version of thingscope operates on a stack of 5 images, found in the docker-compose.yml file
## Agent
The same python agent as in previous semesters. The agent now includes a flask handler which passes URLs to existing functions. The docker image for the python agent passes requests to the flask handler, and the flask handler calls methods from device_security_scanner

Only the device security scanner and sink, which can convert a pcap file into a list of domains and endpoints and save them to a database, were used in this semester. The remaining python files from previous semesters were moved into the legacy folder.

## MongoDB
The mongodb image, which operates entirely from the docker-compose file (there are no other mongo specific files in the repository) is used by the python agent to populate the database and the web server to read from it.

## Web Client
This react application uses the controllers in the Web Server application to pull data from mongodb and display it neatly to end users. See https://thingscope.cs.columbia.edu for a live version of the web client. 

## Web Server
This react application provides the controllers between the Web Client and Mongo DB. It was copied from the Spring 2021 folder and only modified slightly to work with Docker

## Nginx
All applications are provided behind a single URL. Nginx allows for multiple images to all be served at the same domain and have URL patterns determine which image gets the request.

# Installation & Usage
This version of thingscope is designed to operate without installing anything other than docker and docker compose 

- Step 1. Install Docker & Docker Compose - See https://docs.docker.com/compose/install/linux/
- Step 2. run docker-compose up in the Spring-23 directory
- Step 3. Access the web client at localhost:80. To access the api methods directly, access localhost:80/agent and use the file at agent/flask_handler.py to see what methods are available

# Deploying to AWS
While not part of the original deliverables, multiple templates were built to deploy these images to AWS. There are two ways to deploy (scripts for deployment also exist in the agent/scripts folder)
## Agent only in Lambda
Using AWS Serverless Application Model (SAM), the agent can be deployed to AWS Lambda. 
This can be helpful when trying to process extremely large files
```console
sam build --skip-pull-image -t lambda_template.yaml
sam deploy --no-progressbar
```

## Full Stack as Elastic Container Services
Deploy using cloudformation to have a running EC2 instance
```console
aws cloudformation deploy --template docker_template.yml --capabilities CAPABILITY_NAMED_IAM --stack-name thingscope
```
