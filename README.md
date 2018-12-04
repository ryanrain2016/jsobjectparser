# jsobjectparser
解析网页中爬下来的javascript对象为python对象

```python
from jsobjectparser import parse
s = """
{
    a: 'b',
    c: {
        d: 4.5,
        e: [
            {
                f: 4,
                g: 5
            },
            {
                $f: "4",
                g: '5'
            }
        ]
    }
}
"""
obj = parse(s)
print(obj)  # {'a': 'b', 'c': {'d': 4.5, 'e': [{'f': 4, 'g': 5}, {'$f': '4', 'g': '5'}]}}
print(type(obj)) # <class 'dict'>
```
