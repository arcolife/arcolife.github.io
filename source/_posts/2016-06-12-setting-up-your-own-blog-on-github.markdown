---
layout: post
title: "Setting up your own blog hosted on Github"
date: 2016-06-12 04:37:14 +0530
comments: true
categories: [blogging, github]
---

I recently shifted from having a static page as my [github.io link](http://arcolife.github.io/blog/2016/06/06/first-post/) to making a blog out of the default .io page for my Github account. I found it pretty cool to be able to push stuff through markdown (although even that formatting is configurable under `Rakefile` of octopress source code).

So here's a really short post on how to set it up.

<!--more-->

### Step 0: Make sure you have a github account and a suitable repo

Make an account on [this github website](https://www.github.com/)

..and then, make a new repository on github, called `<username>.github.io`

Reference: I have a repo called: `http://github.com/arcolife/arcolife.github.io`

### Step 1: Get your gear!

Make sure you have git and ruby installed in your command line environment.

I had the following versions:

- ruby 2.2.5p319 (2016-04-26 revision 54774) [x86_64-linux]

  Although lower versions (such as 1.9) might work too.
  
- git version 2.5.5

### Step 2: Get octopress

- Download the repository under a suitable location on your disk:

```
git clone git://github.com/imathis/octopress.git octopress
cd octopress/
```

- Next, if you run `bundle install && rake install`, then IIRC, you'd get a failure.
  If not, then the almighty Gods are with you on this lad ..else,
  make a change to `group:development` in `Gemfile` by adding the following:

```
  gem 'json_pure', '~> 1.8.3'
```

  This is because when I tried to install the requirements,
  I got an error and a recommendation to add the above.
  Refer to [this file under my repo](https://github.com/arcolife/arcolife.github.io/blob/source/Gemfile#L16),
  if in doubt.

  Be advised that this micro-step may not be necessary in future releases or in your environment.
  

- Now install requirements along with octopress itself:
  ```
  bundle install && rake install
  ```

### Step 3: Connect your username.github.io with octopress

Run this:
```
rake setup_github_pages
```

Follow the instructions and supply input as asked.

This would clone and download your repo to a folder called `source` and change your
branch from `master` to `source`. You should check this with `git remove -v`.
I got something like this:

```
octopress	git://github.com/imathis/octopress.git (fetch)
octopress	git://github.com/imathis/octopress.git (push)
origin		https://github.com/arcolife/arcolife.github.io (fetch)
origin		https://github.com/arcolife/arcolife.github.io (push)
```

and on running `git branch` it should display `* source`.

If you then do a `git status` you'd get something like this:

```
your branch is based on 'origin/master', but the upstream is gone.
(use "git branch --unset-upstream" to fixup)
```

..which is fine. Let's move on to next step.

----
Side note:
However, if in case, this fails to change your branch to `source`,
i.e, you don't have your username under urls of `origin` in your output of
`git remote -v` ..then you'd have to do this step manually like this:

```
git remote add origin git@github.com:arcolife/arcolife.github.com.git
git branch -m master source
git branch
```

This should now display `* source`.

### Step 4: Try running in preview mode

```
rake preview
```

This should start a server on `http://localhost:4000` and you should be able to
view a default colorful octopress page.

### Step 5 (optional): Deciding where to keep the default blog

[Check this out](http://octopress.org/docs/deploying/subdir/)

Mine is with default settings so I haven't tried this out.

### Step 6: Push your changes to github and deploy the blog


```
rake generate

git add .
git commit -am "init github based octopress"
git push origin source

rake deploy
```

This might take upto 5 mins sometimes or may be a matter of
few seconds depending on how the update job runs and the load
on github servers. Refresh and check in intervals.

### Step 7: A new post

```
rake new_post["My first post"]
```

This would generate a new post and display a message like this:

```
mkdir -p source/_posts
Creating new post: source/_posts/2016-06-12-my-first-post.markdown
```

Edit that file and write up a post using markdown format.
Repeast steps in `Step 6` to deploy.

### Step 8: Tweaks quickstart

Some of these tips are well covered under [Octopress' blogging basics](http://octopress.org/docs/blogging/)
and under [octopress' github README config section](https://github.com/octopress/octopress#configuration)
but just pointing them out for quickstart references:

#### Configure blog name and other basics

Open `_config.yml` and edit the following:

```
title:
subtitle:
author:
```

repeat steps from `Step 6` to see changes live on your username.github.io

#### Linking your octopress blog with social networks

Edit `_config.yml` and edit the following (change your usernames accordingly):

- Github:

```
github_user: arcolife
github_repo_count: 5
```

- Google Plus:

```
googleplus_user: +ArchitSharma1337
```

- Twitter: (read more below under `Adding asides` section on adding twitter feed)

```
twitter_user: arcolife
+twitter_show_replies: false
+twitter_follow_button: true
+twitter_show_follower_count: false
```

- For facebook like on posts:

```
facebook_like: true
```

#### Images in post

If you wanna insert images, add them under `source/images` and you could either:

- Refer to their path either like this:

  ```
  ![Sample image caption](https://raw.githubusercontent.com/username/username.github.io/master/images/sample.png)
  ```

  Replace username with your github username, and `images/sample.png` with whatever path your images are in,
  under `source/`

- Or give a relative path like this:

  ```
  ![Image caption](../images/sample.png)
  ```

The second option is hackish & works based on your directory structure.
[There are other ways of doing this as well](http://stackoverflow.com/a/17089293/1332401)

#### Adding `asides` (panel contents)

Edit `_config.yml` as follows:

```
blog_index_asides:  [custom/asides/about.html, asides/recent_posts.html, asides/github.html, asides/googleplus.html]
post_asides:        [custom/asides/about.html, asides/recent_posts.html, asides/github.html,  asides/googleplus.html]
```

You could add your custom asides / make changes to layout from files under `source/_includes` folder.
For example, to add your twitter feed, you'd wanna take a look [at this blog post](http://blog.jmac.org/2013-03-30-putting-twitter-back-into-octopress.html) which tells you how to add that and why it was removed as a default.

#### Google analytics

This is to track location/count of visitors to your website. Open `_config.yml` and edit the following:

```
google_analytics_tracking_id: <add your ID here>
```

You'd need to have an account on [this google analytics website](https://analytics.google.com/)
to get an ID. There's a limit on number of free IDs allotted to your google account. Check out
the T&Cs on their website.

#### Comments in blog posts

If you wanna enable `Disqus` based comments, you need to have an account on [this disqus admin website](https://www.disqus.com/admin/) and add the url `<username>.github.io` under trusted domains on `https://<disqus admin username>.disqus.com/admin/settings/advanced/` and you need to configure your `community` name (which is nothing but a setting for your site) under `https://<disqus admin username>.disqus.com/admin/settings/general/`

#### Adding a static website under your github website

If you'd like to link up a static content (fully supporting it's own html/css layout),
just add them under `source/<new_dir>/` and you should be able to access that
under `username.github.io/<new_dir>`

Then, go ahead and edit `_config.yml` and edit the following:

```
disqus_short_name: arcolife
disqus_show_comment_count: true
```

#### Working on drafts, disabling comments and adding categories

When you're writing a blog post, change true/false or add categories
to your _posts/<post>.md as shown below:

```
comments: true
published: true
categories: [RHEL, Linux, Microservices]
```

A push to github with `published: false` means the markdown has been safely
committed to source branch on your repo, but the post is not publicly visible.
This way you could keep working on the file and change to true when it's ready.

----

All that said, I still haven't added an 'about' section to my post,
or moved it under a custom `blog/` folder successfully. Or changed the
default page to something else or made changes to default theme.
If you've done that, please add a comment here on how you did it
or a link to it if you've blogged about it. Would save me some time eh! :)

Thats it for now folks!

Share it across, post a comment if you'd like to add something
to this post, or want any edits made or found a flaw in the flow
or would simply like to let me know if this helped.

Cheers!
