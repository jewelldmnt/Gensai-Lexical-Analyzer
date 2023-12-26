import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def file_handling(extension):
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
    pdf_or_csv = input("Enter 1 for a csv file output.\nEnter 2 for a pdf file output.\nEnter anything for no file output: ")
    
    if pdf_or_csv == '1':
        df.to_csv(file_handling('csv'))
        print(df.to_string(index=False))
        
    elif pdf_or_csv == '2':
        pdf_path = file_handling('pdf')
        generate_pdf(df, pdf_path)
        print(f"PDF generated and saved at: {pdf_path}")
    else:
        print(df.to_string(index=False))
