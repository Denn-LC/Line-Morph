import pandas as pd

def tsv_to_csv(input_name, output_name):

    catalogue = pd.read_csv(input_name, sep="\t")

    catalogue.to_csv(output_name, index = False)
