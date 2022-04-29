# Requirements
* jamotools == 0.1.10 (https://github.com/HaebinShin/jamotools)
<br></br>

# Type Of Typo
* Typing a key located nearby. (ex. 룬의 아이들 -> 훈의 아이들, The Hobbit -> The Hibbit)
* Typing a key with or without the shift key. (ex. 100% 실전대비 -> 1005 실전대비, The Hobbit -> The hobbit)
<br></br>

# How To Use
## Code
```python
from typo import Typo

typo = Typo()

print(typo.convert("누가 내 치즈를 옮겼을까? - Spencer Johnson", k=1))  # convert 1 character
print(typo.convert("누가 내 치즈를 옮겼을까? - Spencer Johnson", k=3))  # convert 3 character
print(typo.convert("누가 내 치즈를 옮겼을까? - Spencer Johnson", k=5))  # convert 5 character
```
## Result
> 누가 내 치즈를 옮겼을까 <span style="color:red">/</span> - Spencer Johnson  
> 누가 내 <span style="color:red">티</span>즈를 옮겼을까? - <span style="color:red">s</span>pencer Johnso<span style="color:red">m</span>  
> 누<span style="color:red">기</span> 내 <span style="color:red">차</span>즈를 옮겼을까? <span style="color:red">_</span> Spenc<span style="color:red">E</span>r Johh<span style="color:red">d</span>on  
