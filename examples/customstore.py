import pandas as pd
import sss

my_store = sss.FrameStore(
    format=sss.FrameFormat.csv, path="./tempfiles", no_cleanup=True
)


@sss.keeps("four", store=sss.SSS_FRAME)
def four() -> pd.DataFrame:
    return pd.DataFrame({"a": [4, 6, 10]})


@sss.uses("four", argname="input_df", store=sss.SSS_FRAME)
@sss.keeps("five", store=my_store)
def five(input_df: pd.DataFrame = None) -> pd.DataFrame:
    df = input_df.copy()
    df["b"] = df["a"] * 3
    return df


_ = sss.process(
    (
        four,
        five,
    )
)

# value will persist in ./tempfiles/.sss/<uuid>/five
