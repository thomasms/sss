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

# or get from the store
print(sss.SSS_FRAME.get("five"))
