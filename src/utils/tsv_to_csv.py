import pandas as pd

def tsv_to_csv(input_name, output_name):

    catalogue = pd.read_csv(
      input_name,
      sep = "\t",
      comment = "#",
      skiprows = [61, 62] # vioque specific 
    )

    catalogue.to_csv(output_name, index = False)
