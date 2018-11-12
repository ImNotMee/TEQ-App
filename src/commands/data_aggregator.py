import pandas as pd
import numpy as np
import re
import sys
from uploading_command import UploadingCommand
sys.path.append("../temhelp")
from template_handler import TemplateHandler
sys.path.append("../tests")

class DataAggregator(UploadingCommand):

    def __init__(self, template_name):
        '''
        (DataAggregator, str) -> None

        Initializes a data aggregator, and injects a specific template
        name to the uploading command
        '''
        UploadingCommand.__init__(self, template_name)
        self._postal_code = 'Postal Code'
        self._processing_detail = 'Processing Detail'
        

    def execute(self, df, th):
        '''
        (DataAggregator, DataFrame, TemplateHandler) -> DataFrame

        Executes the command, assuming a dataframe object gets passed in.
        Currently only checks for if the data matches the type the column is
        suppose to be.
        '''
        #template = th.get_template(self._template_name)
        self._exec_status = False
    
        # get a list of fields that are not formatted correctly
        wrong_format_fields = parse_all_columns(df, 'template')
        
        self._exec_status = True        
        return df
    
    def _postal_code_checker(self, df):
            '''
            (DataFrame) ->  DataFrame
            The DataFrame of 'Postal_Code' is given, then return a new
            'Postal_Code' DataFrame to fix any mismatch types of Canadian
            Postal Code. The only form that is right is'X1X1X1'. If there is
            data that is not the correct format, it will be replaced by an
            empty string.
            '''
            p_codes = list()
            # Initalize the regex
            p = re.compile('^([a-zA-z]?[0-9]){3}$')
            for value in df.get_values():
                # Get the value (string)
                postal_code = value
                postal_code = postal_code.replace('-', '')
                postal_code = postal_code.replace(' ', '')
                # Check if the given data matches the type
                if (len(postal_code) == 6 and p.match(postal_code)):
                    p_codes.append(postal_code)
                else:
                    # An empty string replaces the false data
                    p_codes.append("")

            new_df = {'Postal_Code': p_codes}
            return pd.DataFrame(new_df)

    def executed_properly(self):
        '''
        (Command) -> boolean

        Returns a boolean to determine if this command was executed properly
        '''
        return self._exec_status

def parse_all_columns(df, template):
    '''
        (DataFrame, TemplateHandler) -> List of
        [Tuple of (String, int)]
        
        Given a DataFrame and TemplateHandler, returns a tuple of all the
        fields that are not matching the regex/format.
    '''
    # List to store the tuples
    misformated = list()
    # Gets the column names to a list
    header_name = template.get_header()
    # Gets the list of regex
    regex = template.get_regex()
    # for looping through regex list
    count = 0
    
    for col_i in range(len(header_name)):
        column = df.get(header_name[col_i])
        if (column is not None):
            # Loop through all the fields
            for row in range(len(df.index)):
                # getting the regex from the list
                p = re.compile(regex[count])
                # Checks each field to the matching regex
                if (p.match(str(df.iat[row, col_i])) is None):
                    # Get a list of drop down values
                    #dropdown = template.get_dropdown_values(column)
                    dropdown = drop_down[col_i]
                    if (len(dropdown) != 0):
                        # If its not in the drop down list
                        if (column[row] not in dropdown):
                            misformated.append((header_name[col_i], row))
                    else:
                        # Append to the misformated list
                        misformated.append((header_name[col_i], row))    
        # Shift the regex list down by 1 each column is done
        count = count + 1
            
    return misformated