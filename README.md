# [TOC Project-台中市公車到達時間查詢](https://github.com/st9540808/ChatBot)


## Setup

### Prerequisite
* Python3
* Chrome

#### Install Dependency
```sh
pip install -r requirements.txt
```


### Run Locally
Using`ngrok` as a proxy.

**`ngrok` will be used in the following instruction**

```sh
ngrok http 5000
```

After that, `ngrok` would generate a https URL.

You should set `WEBHOOK_URL` (in setup.py) to `your-https-URL/hook`.

#### Run the sever

```shell
python3 setup.py
```

## Finite State Machine
![fsm](https://raw.githubusercontent.com/st9540808/ChatBot/master/my_state_diagram.png)

## Usage
The initial state is set to `idle`.

The machine only accept following string or template. If the state goes to `waiting`, it will start countdown for 30 minutes and call deactivate(), and then set current state to `idle`.

### accept string
> 1. "Activate" (Case doesn't matter)

Activate webdriver and waiting for user input.
<br>

> 2. "Update" (Case doesn't matter)

Reply the information of previously input bus request string. If it is first called, it will reply the information of `14從民俗到中友`
<br>

> 3. "<路線>**從**<起站>**到**<下車站>"

This string template will request bus information including number of between `起站` and `下車站` if both stops and route exists

### Example
#### 1.
> 	* Input: "Activate"
> 		* Reply: "activated"
> 	* Input: "12從火車站到民俗"
> 	    * Reply: "12 經14站到崇德國中(民俗公園) <br>--------- 台中火車站預計到站: 20:21"
> 	* Input: "Update"
> 	    * Reply: "12 經14站到崇德國中(民俗公園) <br>--------- 台中火車站預計到站: 43分"

<br>

#### 2.
> 	* Input: "Update"
> 	    * Reply: "14 經14站到中友百貨 <br>--------- 民俗公園(昌平路)預計到站: 9分"




## Author
[TaiYou Kuo](https://github.com/st9540808)