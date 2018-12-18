# EndOfDecember

<p align="center">
<img  src=./image/game.png width="50%">
</p>
</br>

## How to play

1. requirements

~~~
pip3 install numpy==1.15.4
pip3 install opencv-python==3.4.4.19
~~~

2. clone repo

~~~
git clone git@github.com:yanghoJI/EndOfDecember.git
~~~

3. play the game

~~~
cd 2048
python3 game2048V1.py
~~~

## Description of algorithm

1. flow diagram

<p align="center">
<img  src=./image/flow.png width="55%">
</p>
</br>
</br>
</br>
2. calculNextArray Function

~~~
if Pi == Vi:
    result_Array[Pi] = Pi + Pi
    NextPi = 0

elif Pi == 0 or Vi == 0:
    result_Array[Pi] = 0
    NextPi = Pi + Vi

else:
    result_Array[Pi] = Pi
    NextPi = Vi
~~~

</br>
<p align="center">
<img  src=./image/calcul.png width="55%">
</p>
</br>
</br>

* * *

## 2048 with Reinforcement Learning

#### Comming soon
