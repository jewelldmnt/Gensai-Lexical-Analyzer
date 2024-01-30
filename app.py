from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
from Syntax_Analyzer.syntax_analyzer import Syntax_Analyzer


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

SPECIAL_CHAR = set("!@#$%^&*()+=<>?/;:'\"[]{}|`~")
OPERATORS = set("+-*/")


def relative_to_assets(path: str) -> Path:
    """
    Returns a Path object representing the path relative to the ASSETS_PATH.

    Parameters:
    - path (str): The path to be appended to the ASSETS_PATH.

    Returns:
    Path: The resulting Path object.
    """
    return ASSETS_PATH / Path(path)


def update_line_number(*args):
    """
    Updates the line numbers displayed in the UI based on the current content in the text widget.
    """
    lines = ide_text.get("1.0", "end-1c").split("\n")
    line_numbers = " ".join(f'{i}' for i in range(1, len(lines) + 1))
    line_number_label.config(text=line_numbers)
    
    
def is_valid_filename(file_path):
    """
    Checks if the given file path has a valid filename and extension.

    Parameters:
    - file_path: The path of the file to be checked.

    Returns:
    tuple: A tuple containing a boolean indicating validity and an error message if invalid.
    """
    try:
        file_name = Path(file_path).name
        number_dot = 0
        for char in file_name:
            if (char in SPECIAL_CHAR or char in OPERATORS) and char != '.':
                return False, "Error: Invalid file extension. Don't include special characters."
            if char == '.':
                number_dot += 1
            if number_dot >= 2:
                return False, "Error: Invalid file extension. You must have only one file extension."

        if not file_path.endswith(".gsai"):
            return False, "Error: Invalid file extension. Only '.gsai' files are allowed."
    except:
        return False, f"Error: File '{file_path}' not found."
    
    return True, None


def upload_code_clicked():
    """
    Opens a file dialog to upload GSAI code from a file and displays it in the IDE text widget.
    """
    file_path = filedialog.askopenfilename(filetypes=[("GSAI files", "*.gsai")])
    if file_path:
        valid, error_message = is_valid_filename(file_path)
        if valid:
            with open(file_path, 'r') as file:
                clear_syntax_errors()
                code_content = file.read()
                ide_text.delete("1.0", END)
                ide_text.insert(END, code_content)
                update_line_number()
                label_filename.config(state=NORMAL) 
                label_filename.config(text=Path(file_path).name)
                label_filename.config(state=DISABLED) 
        else:
            messagebox.showerror("Error", error_message)


def save_code_clicked():
    """
    Saves the current code in the IDE text widget to a file selected by the user.

    Displays success message if the file is successfully saved, otherwise shows an error message.

    """
    file_path = filedialog.asksaveasfilename(defaultextension=".gsai", filetypes=[("GSAI files", "*.gsai")])
    if file_path:
        valid, error_message = is_valid_filename(file_path)
        if valid:
            save_file(file_path)
            label_filename.config(text=Path(file_path).name)
            messagebox.showinfo("Success", f"Code saved to '{file_path}'.")
        else:
            messagebox.showerror("Error", error_message)
            
            
def save_file(file_path):
    """
    Saves the content of the IDE text widget to the specified file.

    Parameters:
    - file_path (str): The path of the file to save the code.

    """
    with open(file_path, 'w') as file:
        file.write(ide_text.get("1.0", END))
 
        
def clear_code_clicked():
    """
    Clears the content of the IDE text widget and updates line numbers.

    """
    ide_text.delete("1.0", END)
    update_line_number()


def clear_syntax_errors():
    """
    Clears the content of the syntax error table.

    """
    # Clear the content of the output table
    for item in output_table.get_children():
        output_table.delete(item)


def run_code_clicked():
    """
    Runs the syntax analyzer on the current code, displays syntax errors in the syntax error table.

    """
    current_filename = label_filename.cget("text")
    if current_filename:
        file_path = "tester/syntax_analyzer.gsai"
        save_file(file_path)
        syntax_analyzer = Syntax_Analyzer()
        syntax_errors = syntax_analyzer.parse(file_path)
        clear_syntax_errors()
        syntax_error_table(syntax_errors)
    else:
        messagebox.showwarning("Warning", "Please save the code or upload a file before running the syntax analyzer.")


def syntax_error_table(all_syntax_error):
    """
    Populates the syntax error table with data.

    Parameters:
    - all_syntax_error (dict): A dictionary containing line numbers and corresponding syntax errors.

    """
    # Insert data into the Treeview
    for line_num, syntax_errors in all_syntax_error.items():
        output_table.insert("", "end", values=[line_num, *syntax_errors[0]])

    # Adjust the height of rows for multiline text
    for i in range(len(all_syntax_error)):
        output_table.rowconfigure(i, minsize=20)  # Adjust the height as needed


def on_cell_click(event):
    """
    Event handler for clicking on a cell in the syntax error table.

    Parameters:
    - event: The event object.

    """
    # Get the item that was clicked
    item_id = output_table.identify_row(event.y)
    # Get the content of the clicked cell
    cell_content = output_table.item(item_id, 'values')
    # Display a popup window with the enlarged content
    show_enlarged_content(cell_content)


def show_enlarged_content(content):
    """
    Displays enlarged content in a popup window.

    Parameters:
    - content (list): The content to be displayed.

    """
    # Create a popup window to display the enlarged content
    popup_window = Toplevel(window)
    popup_window.title("Enlarged Content")
    
    # Create a Text widget to display the content
    enlarged_text = Text(popup_window, wrap=WORD, height=10, width=40)

    # Insert all values from the clicked cell into the Text widget
    for value in content:
        enlarged_text.insert(END, str(value) + '\n')

    enlarged_text.pack()


def on_closing():
    """
    Event handler for closing the application.

    Deletes the syntax_analyzer.gsai file when the app is closed.

    """
    # Delete the syntax_analyzer.gsai file when the app is closed
    file_to_delete = OUTPUT_PATH / Path("tester/syntax_analyzer.gsai")
    if file_to_delete.exists():
        try:
            file_to_delete.unlink()
        except Exception as e:
            window.destroy()
    
    window.destroy()



##########################################################################################################
# Main Program
##########################################################################################################

window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#161A1D")

canvas = Canvas(bg="#161A1D", height=1024, width=1440, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

##########################################################################################################
# Canvas Background Image
##########################################################################################################
image_bg = PhotoImage(file=relative_to_assets("bg.png"))
canvas.create_image(720.0, 457.0, image=image_bg)

##########################################################################################################
# Run Code Button
##########################################################################################################
run_code = PhotoImage(file=relative_to_assets("btn_runcode.png"))
btn_runcode = Button(image=run_code, borderwidth=0, command=run_code_clicked, highlightthickness=0, relief="flat")
btn_runcode.place(x=    105.0, y=904.0, width=110.0, height=37.0)

##########################################################################################################
# Upload Code Button
##########################################################################################################
upload_code = PhotoImage(file=relative_to_assets("btn_uploadcode.png"))
btn_uploadcode = Button(image=upload_code, borderwidth=0, command=upload_code_clicked, highlightthickness=0, relief="flat")
btn_uploadcode.place(x=485.0, y=904.0, width=129.0, height=33.0)

##########################################################################################################
# Clear Code Button
##########################################################################################################
clear_code = PhotoImage(file=relative_to_assets("btn_clearcode.png"))
btn_clearcode = Button(image=clear_code, borderwidth=0, command=clear_code_clicked, highlightthickness=0, relief="flat")
btn_clearcode.place(x=230.0, y=906.0, width=114.0, height=30.0)

##########################################################################################################
# Download PDF Button
##########################################################################################################
download_PDF = PhotoImage(file=relative_to_assets("btn_downloadPDF.png"))
btn_downloadcode = Button(image=download_PDF, borderwidth=0, command=None, highlightthickness=0, relief="flat")
btn_downloadcode.place(x=1171.0, y=904.0, width=163.0, height=34.0)

##########################################################################################################
# Save Code Button
##########################################################################################################
save_code = PhotoImage(file=relative_to_assets("btn_savecode.png"))
btn_savecode = Button(image=save_code, borderwidth=0, command=save_code_clicked, highlightthickness=0, relief="flat")
btn_savecode.place(x=633.0, y=906.0, width=120.0, height=30.0)

###########################################################################################################
# Filename Label
##########################################################################################################
label_filename = Label(canvas, bd=0, bg="#1D2125", fg="#DCDCDC", font=("Arial", 10), text="", state=DISABLED)
label_filename.place(x=117.0, y=111.0, width=105.0, height=24.0)

##########################################################################################################
# Syntax Error Table
##########################################################################################################
# Creating a Treeview widget for the output table
output_table = ttk.Treeview(canvas, columns=("Line Number", "Code", "Syntax Error", "Description"), show="headings")
output_table.place(x=822.0, y=103.0, width=512.0, height=778.0)

# Adding a vertical scrollbar for the output table
scrollbar_y = Scrollbar(canvas, command=output_table.yview, orient=VERTICAL)
scrollbar_y.place(x=1313.0, y=168.0, height=689.0)
output_table.config(yscrollcommand=scrollbar_y.set)

# Configure column headings
output_table.heading("Line Number", text="Line Number")
output_table.heading("Code", text="Code")
output_table.heading("Syntax Error", text="Syntax Error")
output_table.heading("Description", text="Description")

# Configure column widths
output_table.column("Line Number", width=50)  # Adjust the width as needed
output_table.column("Code", width=150)  # Adjust the width as needed
output_table.column("Syntax Error", width=150)  # Adjust the width as needed
output_table.column("Description", width=200)  # Adjust the width as needed

# Configure tag for cell enlargement
output_table.tag_configure('enlarge', font=('Arial', 10, 'bold'))

# Apply tag to each cell in the "Description" column for content enlargement
for item in output_table.get_children():
    output_table.item(item, tags=('enlarge',))

# Bind the click event to the on_cell_click function
output_table.bind("<ButtonRelease-1>", on_cell_click)

##########################################################################################################
# IDE Text Entry
##########################################################################################################
ide_text = Text(canvas, bd=0, bg="#1D2125", fg="#DCDCDC", insertbackground="white", wrap=WORD)
ide_text.place(x=185.0, y=170.0, width=538.0, height=683.0)

# Adding a vertical scrollbar for the IDE
scrollbar_ide = Scrollbar(canvas, command=ide_text.yview, orient=VERTICAL)
scrollbar_ide.place(x=733.0, y=170.0, height=683.0)  # Adjusted x-coordinate for scrollbar
ide_text.config(yscrollcommand=scrollbar_ide.set)

# Creating a Text widget for displaying current line number in IDE
line_number_label = Label(canvas, bd=0, bg="#1D2125", fg="#DCDCDC", font=("Courier", 10), text="", wraplength=30, anchor=N)
line_number_label.place(x=135.0, y=170.0, width=50.0, height=683)
# Binding the update_line_number function to cursor movement
ide_text.bind("<KeyRelease>", update_line_number)


##########################################################################################################
# Main Loop
##########################################################################################################
window.protocol("WM_DELETE_WINDOW", on_closing)
window.resizable(False, False)
window.mainloop()

