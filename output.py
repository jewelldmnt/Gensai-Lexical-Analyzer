import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def file_handling(extension):
    """
    handles the file starting from its current directory to a directory in the current file and validates the directory.

    Parameters:
        extension (string): the file extension (i.e. pdf, csv).

    Returns:
        file_path (string): file path of the data.
    """
    # Get the current script's directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    directory_name = input("Input filepath in current directory (leave blank if you want to download in current file path): ")
    
    if directory_name:
        directory_path = os.path.join(current_directory, directory_name)
    else:
        directory_path = current_directory
        
    file_name = 'data.{}'.format(extension)
    file_path = os.path.join(directory_path, file_name)
    
    return file_path

def generate_pdf(df, pdf_path):
    """
    generates a pdf file 

    Parameters:
        df:         the dataframe containing the tokens, token type, and code line.
        pdf_path:   the file path to download the pdf file.

    Returns:
        pdf file containing the tokens, type of token, and what line it is found on.
    """
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    
    # Convert DataFrame to a list of lists
    data_matrix = [df.columns.tolist()] + df.values.tolist()
    
    # Create a Table
    table = Table(data_matrix)
    
    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    
    table.setStyle(style)
    
    # Build the PDF document
    doc.build([table])

def output(df):
    '''
    outputs a raw file either a csv or pdf file or simply just print the tokens.

    Parameters:
        df: the dataframe containing the tokens, token type, and code line.

    Returns:
        pdf file or csv file: data containing the tokens, type of token, and what line it is found on.
    '''
    pdf_or_csv = input("Enter 1 for a csv file output.\nEnter 2 for a pdf file output.\nEnter anything for no file output: ")
    
    # Handles the input of the user and outputs the respective file
    if pdf_or_csv == '1':
        df.to_csv(file_handling('csv')) # downloads the csv file to the directory
        print(df.to_string(index=False))
        
    elif pdf_or_csv == '2':
        pdf_path = file_handling('pdf')
        generate_pdf(df, pdf_path)
        print(f"PDF generated and saved at: {pdf_path}")
    else:
        print(df.to_string(index=False))
