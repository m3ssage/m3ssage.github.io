---
title: About
weight: 999
icon: material/a
---

## Building a Markdown-Powered Website with MkDocs

As a Markdown enthusiast, I've grown accustomed to creating content using this versatile format. Recently, I set out to build a website that leverages Markdown's ease of use, allowing me to create pages with minimal fuss. My search led me to Static Site HTML generators, which sparked a chain reaction of discoveries: GitHub Pages, Jekyll, and eventually, MkDocs and MkDocs-Material. The latter's impressive capabilities had me hooked, and I wanted to take it to the next level by integrating Continuous Integration/Continuous Deployment (CI/CD) to automate the deployment process.

With this goal in mind, I embarked on a mission to create a seamless workflow, where changes to my Markdown files would trigger a build, followed by automatic deployment to a production environment. The thrill of the challenge was palpable, and I'm excited to share my journey with you.

## Code Annotation Examples

### Codeblocks

Some `code` goes here.

### Plain codeblock

A plain codeblock:

```
Some code here
def myfunction()
// some comment
```

#### Code for a specific language

Some more code with the `py` at the start:

``` py
import tensorflow as tf
def whatever()
```

#### With a title

``` py title="bubble_sort.py"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

#### With line numbers

``` py linenums="1"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

#### Highlighting lines

``` py hl_lines="2 3"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

## Icons and Emojs

:smile: 

:fontawesome-regular-face-laugh-wink:

:fontawesome-brands-twitter:{ .twitter }

:octicons-heart-fill-24:{ .heart }

``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```