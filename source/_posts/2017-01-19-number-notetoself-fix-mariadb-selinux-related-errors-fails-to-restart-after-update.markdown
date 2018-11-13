---
layout: post
title: "#noteToSelf - fix MariaDB-selinux related errors (fails to restart after update)"
date: 2017-01-19 21:37:53 +0530
comments: true
categories: [Linux, MariaDB, RHEL]
published: true
---

https://jira.mariadb.org/browse/MDEV-11789

```
yum -y install MariaDB-devel  gcc gcc-c++ autoconf automake make libtool   zlib zlib-devel openssl-devel
yum install -y MySQL-server
 
# tried this, didn't work (where /home/native is the directory with mysql database is stored; configurable in my.cnf)
semanage fcontext -a -t mysqld_db_t "/home/native(/.*)?"
restorecon -Rv /home/native/
yum install selinux-policy
audit2allow -a
yum install yum-utils
yum-complete-transaction
 
# then tried this
yum provides sealert
yum install setroubleshoot-server
sealert -a /var/log/audit/audit.log
# this produces alerts from audit.log and provides hints as to what should be executed next..
 
# so i followed directions..
ausearch -c 'mysqld_safe_hel' --raw | audit2allow -M my-mysqldsafehel
semodule -i my-mysqldsafehel.pp
```

<!--more-->
