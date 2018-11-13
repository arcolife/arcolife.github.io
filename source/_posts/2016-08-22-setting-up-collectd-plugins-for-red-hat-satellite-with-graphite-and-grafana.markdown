---
layout: post
title: "Setting up collectd plugins with Graphite and Grafana"
date: 2016-08-22 15:48:43 +0530
comments: true
categories: [RHEL, Satellite, Linux, Performance, Monitoring, OS]
---

### Intro

Installing collectd could be trivial, although setting up monitoring for continuous time-series metric collection should be simpler. This post is aimed at helping sysadmins setup collectd and connect it to a graphite instance, so that all those metrics could later be viewed from Grafana instance.

<!--more-->

Note:

This post is a spin off from the main satperf project. To take a look at how [satperf](https://www.github.com/redhat-performance/satperf) works, [refer to this post](http://arcolife.github.io/blog/2016/08/22/satperf-a-satellite-performance-benchmarking-and-automation-tool/)

### The process

#### Step 1

Install collectd for your system, Install Graphite server elsewhere (recommended: separate machine). 

---

#### Step 2

When that's installed, take a look at your `/etc/collectd.conf` and add plugins from the list below, as suitable

```
# Allow collectd to log
LoadPlugin syslog

# Loaded Plugins:
LoadPlugin write_graphite
LoadPlugin cpu
LoadPlugin df
LoadPlugin disk
LoadPlugin interface
LoadPlugin irq
LoadPlugin load
LoadPlugin memory
LoadPlugin numa
LoadPlugin processes
LoadPlugin postgresql
LoadPlugin swap
LoadPlugin turbostat
LoadPlugin unixsock
LoadPlugin uptime
```

Note:

- If you're installing this on Red Hat Satellite, you might wanna make additional changes as per [this template in satperf](https://github.com/redhat-performance/satperf/blob/master/playbooks/monitoring/roles/collectd-generic/templates/satellite6.collectd.conf.j2)

- For others, you might wanna take a look at the above mentioned link anyway, for it serves as a generic reference for `/etc/collectd.conf`

- Replace variable names in above referenced satperf's `collectd.conf` as per following defaults / or change them as suitable:

![Figure 1](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/collectd/table.png)

##### Gotchas (for both Satellite setup as well as normal setup):

1) 10 refers to 10 seconds

2) end results on graphite-web UI show under Metrics:
{% codeblock lang:jinja %}
{% raw %}{{graphite_prefix}}.{{inventory_hostname}}.<metrics as per output from plugins>{% endraw %}
{% endcodeblock %}

3) For candlepin password:
{% codeblock lang:bash %}
$ grep "jpa.config.hibernate.connection.password" /etc/candlepin/candlepin.conf | awk -F'=' '{print $2}'`
{% endcodeblock %}
  
4) For Satellite Foreman password: 
{% codeblock lang:bash %}
$ grep "password" /etc/foreman/database.yml | awk '{print $2}' | tr -d '"'
{% endcodeblock %}

---

#### Step 3

Once this is done, reload collectd server and check logs on graphite server to make sure you're able to receive data

#### Other Gotchas:

- Use `iptables -F` if unable to send collectd metrics
- To graph the other parameters in Grafana, [this satellite generic dashboard file](https://github.com/redhat-performance/satperf/blob/master/playbooks/monitoring/roles/dashboard-generic/templates/satellite6_general_system_performance.json.j2)
  - To simply look at which metrics are touched in above dashboard template, refer to [this satperf vars file](https://github.com/redhat-performance/satperf/blob/master/playbooks/monitoring/roles/dashboard-generic/vars/main.yml)
- FYI, I've got an [open PR to add collectd info to sos report, as a plugin](https://github.com/sosreport/sos/pull/866)
- I'll add some screenshots to this post ASAP.
