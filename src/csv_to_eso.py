import pandas as pd

def csv_to_eso(input_name, output_name, ra_col_name, dec_col_name):

    catalogue = pd.read_csv(input_name)

    # keep only RA and DEC for the ESO upload
    eso_catalogue = catalogue[[ra_col_name, dec_col_name]]

    # remove column headers and pandas row indices
    eso_catalogue.to_csv(output_name, index = False, header = False)
