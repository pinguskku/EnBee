[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpinguskku%2FEnBee&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

# EnBee
EnBee: Energy Bug Extractor from Ethereum Client Software

# What is the Energy Bug?
A source code that performs unnecessary calculations in software is defined as an energy bug.
Unnecessary actions of software can be divided into two categories.

First, abnormal behavior

=> Indicates a bug in the software.

Second, normal behavior

=> This is not a bug, but indicates a case where unnecessary operations are performed.

First of all, EnBee is the first tool to automatically identify energy bugs in ECS, identifying energy bugs among bugs that are abnormal behavior.


# Description
You can run EnBee to traditional software (web, apps, etc.) using unit testing as well as Ethereum Client Software.
Because each step is modularized, customization is easy.

The EnBee focus to identify energy bugs from Ethereum Client Software [(ECS)](https://ethereum.org/en/developers/docs/nodes-and-clients/)
---
## Running Environment
### Docker (Require)
### golang1.19+
### No processes which not related current software
### [Intel RAPL](https://web.eece.maine.edu/~vweaver/projects/rapl/) support device
---
## Installation Guide
### 1-step (cloning project)
#### ● git clone https://github.com/pinguskku/EnBee.git
### 2-step (setup docker image)
#### ● docker pull golang:1.19
### 3-step (setup docker container)
#### ● docker run -itd --volume="<your_enbee_path>:/go" --name enbee_1 golang:1.19
### 4-stop (enter docker container)
#### ● docker exec -it enbee_1 /bin/bash
### 5-step (setup container environment)
#### (In docker container)
#### ● apt update
#### ● apt install python3-pip -y
#### ● pip3 install -r requirements.txt
### 6-step (setup your GitHub API Tokens)
#### ● go to the modules/util.py
<line 7>
```
tokens = [your_token1, your_token2, your_token3, ...]
```
### 7-step (execute EnBee)
#### python3 start.py --datas <your_ecs_projects_links.csv path>
#### ex) python3 start.py --datas /go/example/project_link.csv
---




