PDF Field Filler for Immigration Forms
This project is a Python application designed to automate the process of filling out multiple USCIS immigration forms. It provides a simple graphical user interface (GUI) to enter client and attorney information once and then populates that data across all selected PDF documents, saving significant time and reducing data entry errors.

Current Status
Largely Functional for G-28 and N-400.

The application is in a stable, usable state for filling out the G-28 and N-400 forms. The data mapping for these two documents is extensive. While templates for other forms (i-129, i-485, i-589, i-765) are included, their fields are not yet fully mapped into the application.

The primary tool is app.py, which launches the GUI. Helper scripts from the initial development phase (get_fields.py, fill_forms.py) are retained for utility and reference.

Features
The main application (app.py) includes a robust set of features to streamline the form-filling process:

Graphical User Interface: Built with Tkinter for a simple, cross-platform user experience.

Dynamic Form Selection: Choose any combination of available forms to fill for a specific case.

Intelligent Field Display: The UI automatically shows only the input fields required for the forms you've selected.

Two-Column Layout: Client and Attorney information are neatly organized into separate, scrollable columns.

Autofill Profiles: Load pre-saved "Attorney" or "Client" profiles from a dropdown to instantly populate all relevant fields, perfect for testing or frequent use.

Clear Buttons: Quickly clear all client or attorney fields with a single click.

Real-Time Input Validation:

Enforces length and character type rules (e.g., 9-digit A-Numbers, 12-digit USCIS Numbers).

Restricts state fields to 2 characters and automatically converts to uppercase.

Conditional UI: The "Marital Information" section dynamically appears or disappears based on the client's marital status.

Checkbox & Radio Button Support: Correctly handles complex form fields beyond simple text boxes.

Dual Output Modes:

Editable (Default): Generates filled PDFs that remain fully editable in Adobe Acrobat for last-minute changes.

Finalized (Read-Only): Creates locked, flattened PDFs where the data is permanently visible in all viewers (including Mac Preview), ideal for final submission.

How to Use
Prerequisites

Python 3: Ensure you have Python 3 installed on your system.

Dependencies: Open your terminal in the project folder and install the required libraries using pip:

Bash
pip3 install PyMuPDF
Running the Main Application

The primary way to use this tool is through the GUI.

Navigate to the project directory in your terminal.

Run the app.py script:

Bash
python3 app.py
Follow the on-screen instructions:

Select the forms you need to file.

Click "Next."

Fill in the data manually or use the "Load Profile" dropdowns.

Choose whether to create an "Editable" or "Finalized" PDF.

Click "Generate PDFs."

The new, filled files will be saved in the same folder (e.g., g-28_filled.pdf).

Using the Helper Scripts

get_fields.py: This script is a utility for developers to extract all available field names from a PDF. To use it, modify the filenames at the bottom of the script and run python3 get_fields.py. This is essential for mapping new forms.

File Structure
app.py: The main, feature-complete GUI application. This is the file you should run.

fill_forms.py: The original command-line version of the application. Kept for reference.

get_fields.py: A utility script to inspect PDF field names for development.

*.pdf: Template PDF files that the application reads from and writes to.

Future Development
The core logic and UI are complete. The primary path for future development is to expand the application's capabilities by mapping the remaining forms:

I-129

I-485

I-589

I-765

This can be done by using get_fields.py to extract the field names and adding them to the field_map, checkbox_map, and radio_button_map dictionaries in app.py.
