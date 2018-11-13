---
layout: post
title: "Monitoring in Satperf: metrics collection"
date: 2016-10-05 18:21:42 +0530
comments: true
categories: [RHEL, Satellite, Linux, Performance, Monitoring, OS]
---

Satperf utilizes a visualization framework called Grafana, to present graphs.

### Metrics Collected

An explanation of how the following metrics are placed in the satperf monitoring dashboard, is described in the ['Grafana Dashboard'](#overview) section. If you wanna copy these metrics, refer to [this file \[2\] in references](#references)
<!--more-->
- The panels that [satperf](https://www.github.com/redhat-performance/satperf) monitoring module provides:

![Figure 1](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/collectd/process_panels.png)

- The metrics that [satperf](https://www.github.com/redhat-performance/satperf) monitoring module collects for processes:

![Figure 1](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/collectd/process_metrics.png)

#### Overview<h3 id="overview"></a>

The Grafana dashboard is divided into rows and each row has either a single or multiple panels.
Each of those panels query specific metrics. Here's how those metrics in the template [\[1\]](#references) are grouped:

- Grafana variable templating
- Rows > Panels > Queries

The rows are named as following:

![Figure 1](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/grafana/rows.png)

A sample "CPU ALL" row with all panels:

![Figure 2](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/grafana/rows_panels.png)

On clicking edit in one of the panels in that row, we get the metric query frame, like this:

![Figure 3](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/grafana/panel_edit.png)

The templating `$Cloud`, `$Node` etc.. are included at the top of the dashboard, like this:

![Figure 4](https://raw.githubusercontent.com/arcolife/arcolife.github.io/source/source/images/grafana/templating.png)

---
<h3 id="references"></a>

### Grafana Dashboard

1. Satperf Dashboard template [can be obtained here](https://github.com/redhat-performance/satperf/blob/master/playbooks/monitoring/roles/dashboard-generic/templates/satellite6_general_system_performance.json.j2)
2. Variables replaced in that template [are in this file](https://github.com/redhat-performance/satperf/blob/master/playbooks/monitoring/roles/dashboard-generic/vars/main.yml)

### Satperf Dashboard templating explained<h3 id="templating"></a>

So in the jinja template [\[1\]](#references), we have multiple "title"(s) under "rows" section and variables from [\[2\]](#references) are replaced inside the template as illustrated in following piece of that jinja template:

{% raw %}
```
{# Loop over per-process options here #}
    {% for metrics in per_process_metrics %}
      {
        "collapse": true,
        "editable": true,
        "height": "200px",
        "panels": [

      {% for panel in per_process_panels[item.process_list_name] %}
```
{% endraw %}

Additionally, `"title": "CPU All"` in the dashboard template [\[1\]](#references) refers to one row of the dashboard.

---

Note: This post is a spin off from the main satperf project.

- To take a look at how [satperf](https://www.github.com/redhat-performance/satperf) works, [refer to this post](http://arcolife.github.io/blog/2016/08/22/satperf-a-satellite-performance-benchmarking-and-automation-tool/)
- To learn how to setup monitoring for the parameters covered in this post, [refer to this post](http://arcolife.github.io/blog/2016/08/22/setting-up-collectd-plugins-for-red-hat-satellite-with-graphite-and-grafana/)
