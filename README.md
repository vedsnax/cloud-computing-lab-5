# Cloud Computing Lab 5 – AWS RDS PostgreSQL

## Project Overview

This project demonstrates the deployment of an AWS RDS PostgreSQL database and its connection with an application deployed on an AWS EC2 instance.

The application used is Apache Answer, deployed on an EC2 instance. The PostgreSQL database is hosted using Amazon RDS.

## Architecture

User  
↓  
AWS EC2 Instance  
Apache Answer Application  
↓  
PostgreSQL : 5432  
↓  
AWS RDS PostgreSQL  
`answer_db`

## AWS Services Used

- Amazon EC2
- Amazon RDS
- PostgreSQL
- Amazon VPC
- EC2 Security Groups

## RDS Database Details

- Database Engine: PostgreSQL
- DB Instance: `lab5-apache-answer-postgres`
- Database Name: `answer_db`
- Port: `5432`
- Region: `ap-south-1`
- Instance Class: `db.t3.micro`

## EC2 Application

Apache Answer is deployed and running on an AWS EC2 instance.

The application is connected to the PostgreSQL database hosted on Amazon RDS.

## EC2 Application URL

Application URL: http://15.207.89.183:8080

## Database Connection

The EC2 application connects to Amazon RDS using the RDS endpoint and PostgreSQL port 5432.

The RDS database is private and is accessed from the EC2 instance.

## Security Configuration

The RDS Security Group allows PostgreSQL traffic on port `5432` only from the Security Group attached to the EC2 instance.

Public access from `0.0.0.0/0` is not allowed for PostgreSQL.

## Database Schema

The PostgreSQL database contains multiple tables used by Apache Answer, including:

- `question`
- `answer`
- `user`
- `comment`
- `activity`
- `tag`
- `badge`
- `revision`

## CRUD Operations

All CRUD operations were successfully demonstrated through the running EC2 application.

### Create

A new question was created through Apache Answer.

### Read

The created question was viewed through the application.

### Update

The question content was edited successfully.

### Delete

The question was deleted successfully.

## Evidence

The submission includes screenshots showing:

1. EC2 application running
2. AWS RDS PostgreSQL database deployed
3. RDS database configuration
4. RDS Security Group configuration
5. PostgreSQL database tables
6. Create, Read, Update and Delete operations

## Result

The Apache Answer application running on AWS EC2 was successfully connected to AWS RDS PostgreSQL, and all CRUD operations were successfully demonstrated.
