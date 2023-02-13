# sss - Stupidly Simple Storage


Provides two decorates: `keeps` and `uses`, pretty straightforward what they do.

## install

The package is calles `esses` (because there are 3 s's and `sss` was taken).

```bash
pip install esses
```


## Examples

### Default
Example for default (in-memory store).

```python
import sss

@sss.keeps("one")
def one() -> int:
    return 123

@sss.uses("one", argname="first")
@sss.keeps("two")
def two(first=0) -> int:
    return first + 10


@sss.uses("one", argname="first")
@sss.uses("two", argname="second")
@sss.keeps("three")
def three(first=0, second=0) -> int:
    return first + second

result = sss.process((one, two, three))
print(result)

```

### Pandas DataFrame storage
Example for frame (to disk store).

```python
import sss
import pandas as pd


@sss.keeps("four", store=sss.SSS_FRAME)
def four() -> pd.DataFrame:
    return pd.DataFrame({"a": [4, 6, 10]})


@sss.uses("four", argname="input_df", store=sss.SSS_FRAME)
@sss.keeps("five", store=sss.SSS_FRAME)
def five(input_df: pd.DataFrame = None) -> pd.DataFrame:
    df = input_df.copy()
    df["b"] = df["a"] * 3
    return df


last = sss.process((four, five))
print(last)

```