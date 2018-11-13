---
layout: post
title: "resizing an xfs partition on a thin provisoned disk in a RHVM env"
date: 2017-02-22 02:53:28 +0530
comments: true
categories: [file systems, XFS, thin provisioning, RHVM]
---

My postgres parition was full and I desperately needed to increase its size, in order to report some performance numbers.

I couldn't afford to loose the data (and my shit). So I followed these steps to safely increase the size of that partition based on xfs, which existed on a logical volume already.

Self help commands and assumptions:

- disk is /dev/vdb/
- xfs is mounted on /dev/vg_pg/lv_pg
- we grew the disk by 20 Gigs

```
xfs_info /dev/vg_pg/lv_pg -d 64G
```

<!--more-->

Delete and resize partition. Let's say we're working with Partition 1 here:

```
fdisk /dev/vdb

# p
(list paritions)

# d
(confirm delete)

# n
(make new parition with default values, after you've extended disk size from RHEVM env)

# w
(save changes)
```

Now, reboot system.

Run `partprobe` to be sure all went well.

Then, run these set of commands:

```
pvresize /dev/vdb1
pvs
lvextend -L +20G /dev/mapper/vg_pg-lv_pg
lvs
xfs_growfs /dev/vg_pg/lv_pg
```

Refs:

1. https://help.1and1.com/servers-c37684/dynamic-cloud-server-linux-c73266/increase-the-physical-volume-size-of-a-linux-1and1-dynamic-cloud-server-a771780.html
2. https://access.redhat.com/solutions/697303
3. https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Storage_Administration_Guide/xfsgrow.html

