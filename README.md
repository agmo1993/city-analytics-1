## City-Analytics - Cloud based Geospatial Analysis of Tweets in Victoria

## Abstract

We designed and implement a cloud-based solution to collect, process, analyze, and visualize integrated multi-source data. The solution architecture successfully implements several leading heterogeneous technologies and is purposefully designed to be automated and scalable. The resultant system is leveraged to explore several scenarios regarding Australian society and lifestyle through the integration and geospatial analytics of publicly-available social-media data and official statistics.  

Sentiment analysis  is conducted on harvested  tweets originating in Victorian Local Government Areas to identify  whether there exists a meaningful correlation between: 
1) socio-economic well-being of an area and the number of favourable tweets regarding welfare, 
2) relative affluence of a region and user preference regarding mobile device brands, and 
3) overall negativity of tweets and the mental health of a region.  

## System deployment

The system was deployed using Ansible, a software provisioning tool which allows for ad-hoc task execution and configuration management. A long sequence of instructions was developed in an Ansible ‘playbook’, which is written in YAML. 

+ Deployment of virtual machines on the Melbourne Research Cloud (MRC) 
+ Installation of key environment dependencies 
+ Install and deployment of the CouchDB database cluster and twitter harvester 
+ Installation and deployment of the Docker Swarm and the website 
