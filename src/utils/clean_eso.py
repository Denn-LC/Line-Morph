import pandas as pd
from io import StringIO


def clean_eso(input_name):
    # read eso export as text as it is broken
    with open(input_name, "r", encoding = "utf-8") as file:
        data = file.read()

    # repiar broken rows
    data = data.replace("truehttp://archive.eso.org/", "true\nhttp://archive.eso.org/")

    return pd.read_csv(StringIO(data))

