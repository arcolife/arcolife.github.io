---
layout: post
title: "satperf: A Satellite Performance benchmarking and automation tool"
date: 2016-08-22 18:18:16 +0530
comments: true
categories: [RHEL, Satellite, Linux, Performance, Monitoring, Red Hat Satellte, OS]
---

### 1. Intro

Satperf ([link](github.com/redhat-performance/satperf)) is a [Red Hat Satellite](https://access.redhat.com/products/red-hat-satellite) Performance Benchmarking & Automation tool that makes it super easy to quickly setup your own environment with satellite components and start running workloads. It uses ansible playbooks to manage remote execution and has built-in modules for various roles that Satellite Web UI has to offer. These are carried out with the use of hammer commands ([read more on Hammer](https://access.redhat.com/documentation/en/red-hat-satellite/6.2/paged/hammer-cli-guide/chapter-1-introduction-to-hammer)) as an equivalent of Satellite API.

<!--more-->

Briefly, it does the following activities:

- Satellite installation and monitoring
- uploads manifest, updates repo
- concurrently syncs multiple Repositories from Repo Server
- creates lifecycle environments
- creates capsules
- concurrently syncronizes multiple capsules
- ..etc

Satperf runs modules through ansible playbooks, briefly described below under 'Ansible Playbooks in Satperf` section.

### 2. Satperf setup

This is to get the satellite installation + monitoring tools up and running.

Although there's a README included with the project, let's briefly go through steps needed and get an install up and running.

It isn't packaged right now, so first, clone [this satperf repo](https://www.github.com/redhat-performance/satperf).


#### 2.a. PREREQUISITES

From project root, run: `$ source ./setup`, follow the output and act accordingly (install packages / activate virtualenv).

Ensure that satperf help command succeeds: `$ ./satperf.py -h`

![Figure 1](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/satperf/help_menu.png)

#### 2.b CONFIGURATION

The above step should get the setup ready for configurations. Now, configure following files in the manner illustrated:

1. Add configurations specific to Ansible

{% codeblock lang:cfg conf/ansible.cfg %}
log_path = ~/ansible.log
private_key_file = ~/.ssh/id_rsa_perf
{% endcodeblock %}

2. Add [FQDN / hostnames / IP Addresses] for your installation.
   Follow the ansible inventory file pattern, as shown by sample contents of this file.

{% codeblock lang:ini conf/hosts.ini %}
[capsules]
x.x.x.x 
[satellite6]
x.x.x.x
[graphite]
x.x.x.x
[grafana]
x.x.x.x
{% endcodeblock %}

3. `conf/satperf.conf`: Add configurations specific to satperf. 

{% codeblock lang:cfg conf/satperf.conf %}
[Settings]
hosts = conf/hosts.ini
# satperf log file
log_file = log/satperf.log
# Logfile size in Bytes
log_file_size = 10000

[Monitoring]
# for collectd multi/single-host installations one/all of satellite6:capsules
# hosts = satellite6
hosts = satellite6:capsules
{% endcodeblock %}

   For now, leave the sections `[RHN], [Satellite], [Pbench]` untouched.
   In this post, we're only configuring satellite monitering module of satperf.

#### 2.c SATELLITE INSTALLATION

If you already have the satellite setup running, skip below to 'MONITORING INSTALLATION'.

Run `$ ./satperf.py -s`

You'd be asked the following, press [Enter] or type 'n' to skip, if the component's already installed, or you don't want it.

{% codeblock lang:bash %}
 =======> Installing Satellite..
Continue (y/n)?: 

 =======> Installing Capsules..
Continue (y/n)?: 
{% endcodeblock %}

Ignore any other components shown in menu, if so.

Although we've tested this internally and it works, but since this is currently WIP, take a look at logs if something fails, or feel free to [open an issue upstream](https://github.com/redhat-performance/satperf/issues).

#### 2.c MONITORING INSTALLATION

Run `$ ./satperf.py -m`

You'd be asked the following, press [Enter] or type 'n' to skip, if the component's already installed, or you don't want it.

{% codeblock lang:bash %}
 =======> Installing Collectd..
Continue (y/n)?: 

 =======> Installing Graphite..
Continue (y/n)?: 

 =======> Installing Grafana..
Continue (y/n)?: 
{% endcodeblock %}

Although we've tested this internally and it works, but since this is currently WIP, take a look at logs if something fails, or feel free to [open an issue upstream](https://github.com/redhat-performance/satperf/issues).


#### 2.d FINAL STEPS (WIP)

Build the dashboards viewable, through Grafana, by running `$ ./satperf.py -i` 

WIP status: facing an error in this step, similar to [this one](https://github.com/bayandin/webpagetest-private/issues/1)

---

### Ansible Playbooks in Satperf

2 major categories:

1. Satellite
   - Setup (either AWS or normal environements)
     - Satellite
     - Capsules
     - Docker hosts (N content hosts per docker host)
   - Satutils
   - healthcheck

2. Monitoring
   - Collectd
   - Graphite
   - Grafana

---

### Playbook: Monitoring

For a description of metrics we collect about Satellite installation, [refer to this post](http://arcolife.github.io/blog/2016/08/22/setting-up-collectd-plugins-for-red-hat-satellite-with-graphite-and-grafana/)

#### Collectd: role description

Installs collectd on either/all of: satellite / capsule / docker-hosts

#### Graphite: role description

Installs Graphite time-series database for metric storage of collected metrics on the configured graphite host

#### Grafana: role description

Installs Grafana time-series metric visualization framework, on the configured grafana host

---

### Playbook: Satellite

#### Setup: role description

  - common
  - rhsm
  - setup
  - pbench_client (WIP)
  - satellite-populate

#### Satutils: role description (WIP)

  - backup
  - upload-manifest
  - restore
  - add-product
  - create-lifecycle
  - enable-content
  - content-view-create
  - content-view-publish
  - content-view-promote
  - sync-content
  - sync-capsule
  - register
  - status_check

#### Health check: role description (WIP)

We plan to integrate [this github project - sat6_healthCheck](https://github.com/boogiespook/sat6_healthCheck/)

---

### Blog roll: More on Satellite itself

From [Satellite's latest release](https://access.redhat.com/announcements/2470701):

Red Hat Satellite 6.2 is now generally available, and includes the following major enhancements:

- Enhanced container management with RHEL Atomic
- New remote configuration management for managed hosts
- bootstrap.sh support for configuration management and host migration
- The ability to change disconnected environments to connected
- Inter-Satellite synchronization for content
- PXE-less discovery for existing systems

- [Release Notes](https://access.redhat.com/documentation/en/red-hat-satellite/6.2/single/release-notes)

- [Satellite Installation Guide](https://access.redhat.com/documentation/en/red-hat-satellite/6.2/single/installation-guide#upgrading_satellite_server_and_capsule_server) 
