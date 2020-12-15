#!/usr/bin/env python3

# update index.html
with open("public/index.html", 'r') as home:
    home_contents = home.readlines()

# add posts opening div 
target = home_contents.index('<div id="content">\n') + 1
home_contents.insert(target, "<!-- posts -->\n")
home_contents.insert(target + 1, '<div class="posts">\n')

# delete content div because it causes issues with filter
home_contents.remove('<div id="content">\n')

# no need to add closing posts div
# we use closing div from content
#target = home_contents.index('<div id="postamble" class="status">\n') - 1
#home_contents.insert(target, "</div>\n")

# remove link to theindex
home_contents.remove('<li><a href="theindex.html">Hello</a></li>\n')

post_list = []
replace_list = []
# look for posts
for l, line in enumerate(home_contents):
    if line.startswith("<li>2"):
        replace_list.append(l)
        # need to process the whole post before checking further
        # because this post contains another <li> tag within it
        post_file = f"posts/{line[4:-1]}/index.org"
        with open(post_file, 'r') as post:
            categories = ""
            for line in post:
                if line.startswith("#+TITLE: "):
                    title = line[9:]
                elif line.startswith("#+DATE: "):
                    date = line[9:19]
                elif line.startswith("#+INDEX: "):
                    categories += line[9:-1] + ' '
            # then remove extra space from end of categories
            categories = categories[:-1]
        # delete old elements
        #for i in range(4):
        #    home_contents.pop(l)
        # add in new contents
        post_list.append(f'<a class="post" data-category="{categories}" href="{post_file[:-3]}html">\n<div class="post-title">\n{title}</div>\n<div class="post-date">\n{date}\n</div>\n</a>\n')
        #home_contents.insert(l, "</a>\n")
        #home_contents.insert(l, "</div>\n")
        #home_contents.insert(l, date + '\n')
        #home_contents.insert(l, '<div class="post-date">\n')
        #home_contents.insert(l, "</div>\n")
        #home_contents.insert(l, title)
        #home_contents.insert(l, '<div class="post-title">\n')
        #home_contents.insert(l, f'<a class="post" data-category="{categories}" href="{post_file[:-3]}html">\n')

# add posts in reverse order
post_list.reverse()
for p, post in enumerate(post_list):
    home_contents[replace_list[0] + p] = post # change first line
    # delete next three
    for i in range(3):
        home_contents.pop(replace_list[0]+p+1)
    #home_contents.insert(target+2, p)
        
# delete last list elements
home_contents.remove('<ul class="org-ul">\n')
home_contents.remove('</ul>\n')

# now save the file again
with open("public/index.html", 'w') as home:
    home.write(home_contents[0])

with open("public/index.html", 'a') as home:
    for line in home_contents[1:]:
        home.write(line)


# update theindex.html
with open("public/posts/theindex.html", 'r') as index:
    index_contents = index.readlines()

# replace index header
#index_contents.remove('<header>\n')
#target = index_contents.index('<h1 class="title">Index</h1>\n')
#index_contents[target] = '<h2>Index</h2>\n'
#index_contents.remove('</header>\n')

# need to change links in header
index_contents[13] = '<div class="flex-nav">  <div class="name">    X. Capaldi |     <a href="../index.html">      home    </a>  </div>  <a href="https://github.com/xcapaldi" target="_blank">    <img src="../../assets/icons/github.svg" alt="github">    <img src="../../assets/icons/github_white.svg" alt="github">  </a>  <a href="https://www.linkedin.com/in/xavier-capaldi-452a9292" target="_blank">    <img src="../../assets/icons/linkedin.svg" alt="linkedin">    <img src="../../assets/icons/linkedin_white.svg" alt="linkedin">  </a>  <a href="mailto:capaldix@physics.mcgill.ca" target="_blank">    <img src="../../assets/icons/mail.svg" alt="email">    <img src="../../assets/icons/mail_white.svg" alt="email">  </a>  <a href="http://keys.gnupg.net/pks/lookup?op=get&search=0x091B17759759416E" target="_blank">    <img src="../../assets/icons/lock.svg" alt="gpg key">    <img src="../../assets/icons/lock_white.svg" alt="gpg key">  </a>  <a href="rss.xml" target="_blank">    <img src="../../assets/icons/rss.svg" alt="rss">    <img src="../../assets/icons/rss_white.svg" alt="rss">  </a>  <a href="theindex.html">    <img src="../../assets/icons/help-circle.svg" alt="information">    <img src="../../assets/icons/help-circle_white.svg" alt="information">  </a>  </div></div><hr>'

# for each article link add title to listing
for l, line in enumerate(index_contents):
    if line.startswith("<li>"):
        path_end = 13 + line[13:].index('>')
        post_file = f"posts/{line[13:path_end - 6]}.org"
        category = line[path_end + 1:-10]
        # grab title from file 
        with open(post_file, 'r') as post:
            title = post.readline()[9:]

        # recreate the entry
        index_contents[l] = f'{line[:path_end]}>{category} -- {title}</a></li>\n'

# now save the file again
with open("public/posts/theindex.html", 'w') as index:
    index.write(index_contents[0])

with open("public/posts/theindex.html", 'a') as index:
    for line in index_contents[1:]:
        index.write(line)

        


# update rss.xml
with open("public/posts/rss.xml", 'w') as rss:
    # write header info
    rss.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    rss.write('<rss version="2.0">\n')
    rss.write('<channel>\n')
    rss.write('<title>X. Capaldi - Personal Blog</title>\n')
    rss.write('<link>http://www.xcapaldi.com</link>\n')
    rss.write('<description>Posts from Xavier Capaldi. Use an RSS reader to receive notifications on new posts.</description>\n')
    rss.write('<copyright>2021 Xavier Capaldi</copyright>\n')
    rss.write('<language>en-us</language>\n') 
    #rss.write('<atom:link href="http://www.xcapaldi.com/posts/rss.xml" rel="self" type="application/rss+xml"/>')

    # add posts
    posts = []
    with open("public/index.html", 'r') as home:
        home_contents = home.readlines()
        for l, line in enumerate(home_contents):
            # check if a post and extract info
            if line.startswith('<a class="post"'):
                title = home_contents[l + 2][:-1]
                link = 'http://www.xcapaldi.com/' + line[line.index('href') + 6:-3]
                description = ""
                # open file to extract description
                with open(f'public/{line[line.index("href") + 6:-3]}', 'r') as post:
                    need_description = True
                    post_contents = post.readlines()
                    l = 0
                    while need_description:
                        if post_contents[l].find('<p>') != -1:
                            description += post_contents[l]
                            while need_description:
                                l += 1
                                if post_contents[l].find('</p>') == -1:
                                    description += post_contents[l]
                                else:
                                    description += post_contents[l]
                                    need_description = False
                        l += 1
                    # now we need to format the description
                    # remove carriage returns
                    description = description.replace('\n', ' ')
                    # remove html tags
                    # </header><p> at start and </p> at end
                    description = description[12:-5]
                rss.write('<item>\n')
                rss.write(f'<title>{title}</title>\n')
                rss.write(f'<link>{link}</link>\n')
                rss.write(f'<description>{description}</description>\n')
                rss.write('</item>\n')
    # closing info
    rss.write('</channel>\n')
    rss.write('</rss>')
