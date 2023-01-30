# EnBee
EnBee: Energy Bug Extractor from Ethereum Client Software

The EnBee focus to identify energy bugs from Ethereum Client Software [(ECS)](https://ethereum.org/en/developers/docs/nodes-and-clients/)
---
## Running Environment
### Docker (Require)
### golang1.19+
### No processes which not related current software
### [Intel RAPL](https://web.eece.maine.edu/~vweaver/projects/rapl/) support device
---
## Detail Installation
### 1-step (cloning project)
#### git clone https://github.com/pinguskku/EnBee.git
### 2-step (setup docker image)
#### docker pull golang:1.19
### 3-step (setup docker container)
#### docker run -itd --volume="<your_enbee_path>:/go" --name enbee_1 golang:1.19
### 4-step (setup container environment)
#### (In docker container)
#### ● apt update
#### ● apt install python3-pip -y
#### ● pip3 install -r requirements.txt
### 5-step (setup your GitHub API Tokens)
#### ● go to the modules/util.py
<line 7>
```
tokens = [your_token1, your_token2, your_token3, ...]
```
### 6-step (execute EnBee)
#### python3 start.py --datas <your_ecs_projects_links.csv path>



