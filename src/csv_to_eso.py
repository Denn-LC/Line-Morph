import pandas as pd

def csv_to_eso(input_name, output_name, ra_col_name, dec_col_name):

    catalogue = pd.read_csv(input_name)
    # keep only RA and DEC as it is all ESO portal accepts
    eso_catalogue = catalogue[[ra_col_name, dec_col_name]]

    # ESO portal does not require column names nor pandas row numbers
    eso_catalogue.to_csv(
        output_name,
        index = False,
        header = False
    )