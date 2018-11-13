---
layout: post
title: "performance engineering TILs - part 1"
date: 2017-03-02 17:00:16 +0530
comments: true
categories: [Cloud, Performance]
---

## On Scale tests

#### ..on distributed systems, in companies with a global, collaborative and distributed workplace setup  

Before running a scale test, make sure to have the following items checked off your list:

1. Is churn on product integrations, enough to simulate production environment?
2. During the tests, is the product going to run with defaults? Is this about baselining with defaults or are we going to let the system bleed while increasing throughputs? 
3. Do you have exact expectations noted down prior to automating? (per se, monitoring enough parameters in the right way. This includes Telemetry, Logs and Configurations per iteration.)

<!--more-->

   An example of this, from a distributed systems application framework could be:
   
   - Time spent collecting the data as well as size of data v/s Time it took to be committed to the db -- per se, fetch time/volume and db time.
   - Size of data transferred over network for a single workload (and for all workloads/functionalities associated with that application)

4. List of parameters not to be changed? CPU/RAM/Memory/Disk/partitions/Network bandwidth/OS/Installed Packages/Tuning parameters/....
5. Do you have tuning recommendations for the product, prior to testing?
6. Do you have enough debugging skills on the product, to begin with? (extension: Have you solved enough bugs yet?). If not, it's good to have some consultation on this as it helps with forming theories on conclusions.
7. Do you have the lab environment's hardware availability dates in a flexible time range? (keeping potential bottlenecks in mind)

I have been reading Brendon Gregg's ["Systems Performance: Enterprise and the Cloud"](http://www.brendangregg.com/sysperfbook.html) and am inclined to finish this soon. All of the points above, have probably been already covered in detail, in that book.
