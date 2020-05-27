# City-Analytics - Cloud based Geospatial Analysis of Tweets in Victoria
===
## Abstract
===
We designed and implement a cloud-based solution to collect, process, analyze, and visualize integrated multi-source data. The solution architecture successfully implements several leading heterogeneous technologies and is purposefully designed to be automated and scalable. The resultant system is leveraged to explore several scenarios regarding Australian society and lifestyle through the integration and geospatial analytics of publicly-available social-media data and official statistics.  

Sentiment analysis  is conducted on harvested  tweets originating in Victorian Local Government Areas to identify  whether there exists a meaningful correlation between: 
1) socio-economic well-being of an area and the number of favourable tweets regarding welfare, 
2) relative affluence of a region and user preference regarding mobile device brands, and 
3) overall negativity of tweets and the mental health of a region.  

## System deployment
===
The system was deployed using Ansible, a software provisioning tool which allows for ad-hoc task execution and configuration management. A long sequence of instructions was developed in an Ansible ‘playbook’, which is written in YAML. 

+ Deployment of virtual machines on the Melbourne Research Cloud (MRC) 
+ Installation of key environment dependencies 
+ Install and deployment of the CouchDB database cluster and twitter harvester 
+ Installation and deployment of the Docker Swarm and the website 

### Deployment of virtual machines 
===

The first stage of the deployment was of the virtual machines (instances) on the MRC, coupled with the creation of the volumes associated with each instance. This can be executed with the following command: 
```
./lanch-nectar.sh 
```
The command launches the playbook called launch-nectar.yaml, which creates the necessary security groups, creates the volumes and creates four instances. The instances are given the appropriate labels which will then be utilized later in the deployment sequence. These labels are whether the instance is a dbMaster or dbSlave (for CouchDB), a leader, manager or worker (for Docker Swarm). 

### Installation of key environment dependencies  
===

The next stage of the deployment is the installation of the environments dependencies required for both the database and webserver applications, which was Docker. The execution of this step is performed with the following script, 
```
./install-environments.sh 
```
This shell script runs the playbook called install_environments.yaml. Moreover, this playbook also performs key tasks to provide networking access to the instances, as well as the Docker containers and Docker Swarm launched on them. This was done by adding a series of proxy addresses to the environment variables.  

### Install and deployment of the CouchDB database cluster  
===

This stage of the deployment creates the CouchDB containers of three of the instances and sets up the CouchDB cluster. The execution is performed by executing the following script, 

```
./couch-setup.sh 
```

Once the containers are set up, the database is created, and the design documents are imported into the CouchDB database – where the views can be accessed. 
Installation and deployment of the Docker Swarm (website and twitter harvester) 
The final step of the deployment is launching of the initialization of the Docker Swarm, and consequently the webserver – where the front end is hosted. The following command is executed to enable this, 

```
./deploy-swarm.sh 
```

This shell script runs the playbook called deploy_swarm.yaml, which runs a series of commands to build to initialize the swarm, build the website image, build the twitter harvester image and create two docker services across all the nodes. After this step, the system infrastructure is set up. 
