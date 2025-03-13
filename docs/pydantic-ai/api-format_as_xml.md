# pydantic_ai.format_as_xml

Version

Showing documentation for the latest release v0.0.36 2025-03-07.

# pydantic_ai.format_as_xml

```
pydantic_ai.format_as_xml
```

[](https://ai.pydantic.dev)

### format_as_xml

```
format_as_xml(
    obj: Any,
    root_tag: str = "examples",
    item_tag: str = "example",
    include_root_tag: bool = True,
    none_str: str = "null",
    indent: str | None = "  ",
) -> str
```

```
format_as_xml(
    obj: Any,
    root_tag: str = "examples",
    item_tag: str = "example",
    include_root_tag: bool = True,
    none_str: str = "null",
    indent: str | None = "  ",
) -> str
```

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[bool](https://docs.python.org/3/library/functions.html#bool)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

[str](https://docs.python.org/3/library/stdtypes.html#str)

Format a Python object as XML.

This is useful since LLMs often find it easier to read semi-structured data (e.g. examples) as XML,
rather than JSON etc.

Supports: str, bytes, bytearray, bool, int, float, date, datetime, Mapping,
Iterable, dataclass, and BaseModel.

```
str
```

```
bytes
```

```
bytearray
```

```
bool
```

```
int
```

```
float
```

```
date
```

```
datetime
```

```
Mapping
```

```
Iterable
```

```
dataclass
```

```
BaseModel
```

Parameters:

```
obj
```

```
Any
```

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

Python Object to serialize to XML.

```
root_tag
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Outer tag to wrap the XML in, use None to omit the outer tag.

```
None
```

```
'examples'
```

```
item_tag
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Tag to use for each item in an iterable (e.g. list), this is overridden by the class name
for dataclasses and Pydantic models.

```
'example'
```

```
include_root_tag
```

```
bool
```

[bool](https://docs.python.org/3/library/functions.html#bool)

Whether to include the root tag in the output
(The root tag is always included if it includes a body - e.g. when the input is a simple value).

```
True
```

```
none_str
```

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

String to use for None values.

```
None
```

```
'null'
```

```
indent
```

```
str | None
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

Indentation string to use for pretty printing.

```
'  '
```

Returns:

```
str
```

[str](https://docs.python.org/3/library/stdtypes.html#str)

XML representation of the object.

Example:
format_as_xml_example.pyfrom pydantic_ai.format_as_xml import format_as_xml

print(format_as_xml({'name': 'John', 'height': 6, 'weight': 200}, root_tag='user'))
'''
<user>
  <name>John</name>
  <height>6</height>
  <weight>200</weight>
</user>
'''

```
from pydantic_ai.format_as_xml import format_as_xml

print(format_as_xml({'name': 'John', 'height': 6, 'weight': 200}, root_tag='user'))
'''
<user>
  <name>John</name>
  <height>6</height>
  <weight>200</weight>
</user>
'''
```

```
from pydantic_ai.format_as_xml import format_as_xml

print(format_as_xml({'name': 'John', 'height': 6, 'weight': 200}, root_tag='user'))
'''
<user>
  <name>John</name>
  <height>6</height>
  <weight>200</weight>
</user>
'''
```

```
pydantic_ai_slim/pydantic_ai/format_as_xml.py
```

```
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
```

```
def format_as_xml(
    obj: Any,
    root_tag: str = 'examples',
    item_tag: str = 'example',
    include_root_tag: bool = True,
    none_str: str = 'null',
    indent: str | None = '  ',
) -> str:
    """Format a Python object as XML.

    This is useful since LLMs often find it easier to read semi-structured data (e.g. examples) as XML,
    rather than JSON etc.

    Supports: `str`, `bytes`, `bytearray`, `bool`, `int`, `float`, `date`, `datetime`, `Mapping`,
    `Iterable`, `dataclass`, and `BaseModel`.

    Args:
        obj: Python Object to serialize to XML.
        root_tag: Outer tag to wrap the XML in, use `None` to omit the outer tag.
        item_tag: Tag to use for each item in an iterable (e.g. list), this is overridden by the class name
            for dataclasses and Pydantic models.
        include_root_tag: Whether to include the root tag in the output
            (The root tag is always included if it includes a body - e.g. when the input is a simple value).
        none_str: String to use for `None` values.
        indent: Indentation string to use for pretty printing.

    Returns:
        XML representation of the object.

    Example:
    ```python {title="format_as_xml_example.py" lint="skip"}
    from pydantic_ai.format_as_xml import format_as_xml

    print(format_as_xml({'name': 'John', 'height': 6, 'weight': 200}, root_tag='user'))
    '''
    <user>
      <name>John</name>
      <height>6</height>
      <weight>200</weight>
    </user>
    '''
    ```
    """
    el = _ToXml(item_tag=item_tag, none_str=none_str).to_xml(obj, root_tag)
    if not include_root_tag and el.text is None:
        join = '' if indent is None else '\n'
        return join.join(_rootless_xml_elements(el, indent))
    else:
        if indent is not None:
            ElementTree.indent(el, space=indent)
        return ElementTree.tostring(el, encoding='unicode')
```

```
def format_as_xml(
    obj: Any,
    root_tag: str = 'examples',
    item_tag: str = 'example',
    include_root_tag: bool = True,
    none_str: str = 'null',
    indent: str | None = '  ',
) -> str:
    """Format a Python object as XML.

    This is useful since LLMs often find it easier to read semi-structured data (e.g. examples) as XML,
    rather than JSON etc.

    Supports: `str`, `bytes`, `bytearray`, `bool`, `int`, `float`, `date`, `datetime`, `Mapping`,
    `Iterable`, `dataclass`, and `BaseModel`.

    Args:
        obj: Python Object to serialize to XML.
        root_tag: Outer tag to wrap the XML in, use `None` to omit the outer tag.
        item_tag: Tag to use for each item in an iterable (e.g. list), this is overridden by the class name
            for dataclasses and Pydantic models.
        include_root_tag: Whether to include the root tag in the output
            (The root tag is always included if it includes a body - e.g. when the input is a simple value).
        none_str: String to use for `None` values.
        indent: Indentation string to use for pretty printing.

    Returns:
        XML representation of the object.

    Example:
    ```python {title="format_as_xml_example.py" lint="skip"}
    from pydantic_ai.format_as_xml import format_as_xml

    print(format_as_xml({'name': 'John', 'height': 6, 'weight': 200}, root_tag='user'))
    '''
    <user>
      <name>John</name>
      <height>6</height>
      <weight>200</weight>
    </user>
    '''
    ```
    """
    el = _ToXml(item_tag=item_tag, none_str=none_str).to_xml(obj, root_tag)
    if not include_root_tag and el.text is None:
        join = '' if indent is None else '\n'
        return join.join(_rootless_xml_elements(el, indent))
    else:
        if indent is not None:
            ElementTree.indent(el, space=indent)
        return ElementTree.tostring(el, encoding='unicode')
```

