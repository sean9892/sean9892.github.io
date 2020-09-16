"""
---
title: "[BOJ] A+B"
date: 2020-04-22
categories:
- OJ
tags:
- Arithmetic

---

[BOJ1000 A+B](https://www.acmicpc.net/problem/1000)
"""

fname=input("filename >> ")
title=input("title >> ")
date=input("date >> ")
cat=input("category >> ")
cnttag=int(input("the number of tag >> "))
tag=[]
for x in range(cnttag):
    y=input("tag >> ")
    tag.append(y)

f=open(date+"-"+fname+".md","w")
f.write("---\n")
f.write("title:"+'"'+title+'"\n')
f.write("date:"+date+"\n")
f.write("categories:\n- "+cat+"\n")
f.write("tags:\n")
for x in tag:
    f.write("- "+x+"\n")
f.write("---\n")
