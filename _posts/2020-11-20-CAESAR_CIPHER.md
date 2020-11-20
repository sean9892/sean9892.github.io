---
title: "Caesar Cipher(시저 암호)"
date: 2020-11-20
categories:
- cryptography
tags:
- cryptography
---

Caesar Cipher은 고대 로마 황제였던 카이사르(시저)가 사용했던 간단한 암호로써, 알파벳을 특정한 개수만큼 shift하는 것으로 decode할 수 있다.

shift된 문자열이 encode되기 전의 원본인지 판별하는 것을 자동화하는 것은 쉽지 않으며, decode 결과로 가능한 문자열의 수는 많지 않으므로(26개) 다음은 가능한 모든 결과를 출력하는 함수의 구현이다.

```python
def decode_caesar(t):
    def nxtAlpha(x):
        if x=='z':
            return 'a'
        elif x=='Z':
            return 'A'
        else:
            return chr(ord(x)+1)
    import copy
    s=copy.deepcopy(t)
    res=[]
    for x in range(26):
        res.append(copy.deepcopy(s))
        for y in range(len(s)):
            if s[y].isalpha():
                s=s[:y]+nxtAlpha(s[y])+s[y+1:]
    return tuple(res)

if __name__=='__main__':
    print(decode_caesar(input()))
```





