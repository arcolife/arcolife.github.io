---
layout: post
title: "Recovering encrypted LVM based partitions, after accidentally overwriting 'em with 'fio'!"
date: 2017-04-30 08:09:01 +0530
comments: true
categories: [file systems, ext4, LVM, Fedora, disk recovery, disk partitioning]
---

Disclaimer: Logging my experience of a quasi-success in executing `$subject`. 

#### Specs

- Partitioning scheme: LVM based encrypted partitions
- Hardware - Lenovo T440p
- OS (earlier) - Fedora 24 Gnome
- OS (now) - Fedora 24 KDE

As if there aren't enough cases already, this one found a grand entrance to the club of royally screwed ups, when it comes to messing up with your disk partitions.

<!--more-->

##### Backstory and the foreplay

I supplied [this command](https://github.com/arcolife/kvm_io/blob/master/bench_iter.sh#L113) but with `fio` instead of `pbench-fio`. I thought the options would be similar to what `fio` supports, so I ran it with`--client=<IP of VM>` which it obviously didn't support and reacted to, with a complaint. The command I then ran using ssh, was something this:

```
fio --filename=/dev/sda --direct=1 --rw=randwrite --refill_buffers --ioengine=libaio --bs=128k --rate_iops=1280  --iodepth=16 --numjobs=8 --runtime=20 
```

But I managed to mess it up and this ran on host's `/dev/sda` instead of VM's. Albeit, I didn't realize the blunder in that moment and later rebooted the machine. Well then obviously it wouldn't boot up and so it went into PXE boot mode. With 0 pendrives within my reach, I PXE booted through my office's network and thought I'd use the liveuser to recover. But that went into the `#dracut` mode. I went back home and finally used a live USB to boot into the laptop. On checking for partitions through `fdisk`, I couldn't see any. Whelp!

And in the install menu's disk selection option, it didn't show up the partitions either..

![Manual Partition - Free](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/manual_partition_without.jpeg)

#### The act of repression

So then I downloaded testdisk [1] and followed those step-by-step instructions. Unfortunately, mine was a case of an encrypted ext4 partition, which isn't what that testdisk's version supports (for listing files) out of the box. But on a 'quick search', testdisk did discover 2 partitions (Bootable and Primary) and on a 'deeper search', other parititions with labels P and D (Primary/Deleted [1]). I chose to write the quick search partition table and the exited the tool. 

![quick testdisk](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/testdisk_quick.jpeg)
![deep testdisk](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/testdisk_deeper.jpeg)
![Post testdisk](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/partition_post_testdisk.jpeg)

Later, I ran another tool `PhotoRec` [2] by the same author behind `testdisk` and that helped me recover 4 txt files and 3 LUKS files. I wrote the partitions it found out, to the table. It would only make sense if I could somehow decrypt and mount/scan the .LUKS files. I used an external hard drive and saved them to it while supplying the same as an option to PhotoRec.

![Photo Rec deep](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/photorec_deep.jpeg)

Note that this was a hurdle I *had to* cross since they're encrypted partitions. Generally speaking, if we've got N encrypted partitions, but the initial few sectors containing the header volume info for passphrase are overwritten, it's often impossible to recover data (as of what I understood from conversations in forums). But this might be considered as an advantage in cases where you'd like to mess up the hard drive on purpose, since erasing the first few bytes does the job, as the data in rest of the sectors is encrypted af.

Getting back to point, I followed [3] and mapped those LUKS files to the VG pool (although unsuccessfully). Error that I spotted (under `/var/log/messages`) was somewhere along the lines of `vgchange buffer io error on device sda <snip snip> logical block: LUKS I/O error -5 writing to inode`.

![LUKS dump](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/luks_dump.jpeg)
![LUKS open](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/luks_open.jpeg)
![PVS](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/pvs.jpeg)

Side note: Neither in PhotoRec nor in TestDisk, did I attempt to re-write MBR table.

On the edge of a Post Traumatic Scan Disorder from Testdisk and photoRec, I almost gave up while recalling suggestions from a few forums, which pointed to the fact that it's impossible to recover encrypted partitions if the header volume info wasn't backed up. It all seemed gloomy and dark and I slept thereafter while putting another photoRec scan to work in the background.

![Vgchange error](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/vgchange_error.jpeg)

A couple hours later, I tried to wake up the laptop screen but it wouldn't (Fedora 24 KDE does that sometimes it seems). Trudging back to the idea of starting over, I hard rebooted and decided to install the OS, from scratch. But to my surprise, while booting up with the live USB and inside the install menu's disk partitioning scheme option `I'll configure partition myself`, I saw an "Unknown" partitioning dropdown. Now now, this didn't show up earlier and so then I went ahead and removed all but the biggest one (which I knew was the home partition). I supplied the passphrase for older encryption, specified a mount point `/home`, made other parititions (all except biosboot [5]) and Voila! all I had to do later was to reinstall some rpm packages. 

![Manual Partition - Unknown](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/manual_partition_with.jpeg)

So to speak, I'm not sure what gave or how it worked, but it did! Tag-lining this as a "comedy of errors and a tragedy to remember".

![Happy](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/final.jpeg)

PS: On recovery, I've lost some disk space ( ~ 80 MiB) fragmented and squeezed in between those partitions. Also, my RAM shows up as 15.4 GiB instead of 16 GiB. Or maybe that's just how accurate a System Monitor in KDE is?!

![Fragments count](https://raw.githubusercontent.com/arcolife/arcolife.github.io/master/images/recovery/fragments.jpeg)

#### References

1. http://www.cgsecurity.org/wiki/TestDisk_Step_By_Step
2. http://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step
3. https://alvinabad.wordpress.com/2012/09/22/how-to-recover-a-luks-encrypted-disk/
4. [Recovering files from an encrypted drive](https://forum.cgsecurity.org/phpBB3/viewtopic.php?t=1431)
5. [Re: how to tell when biosboot partition is needed?](https://www.redhat.com/archives/kickstart-list/2012-August/msg00005.html)
6. [USB stick unreadable](https://forum.cgsecurity.org/phpBB3/viewtopic.php?t=462)
7. http://www.pavelkogan.com/2014/05/23/luks-full-disk-encryption/
8. http://manpages.ubuntu.com/manpages/xenial/man1/ecryptfs-recover-private.1.html
