import fitz  # this is the name for the pymupdf library
import pprint

def get_pdf_fields_pymupdf(pdf_path):
    """prints the fillable form fields from a given pdf using pymupdf."""
    print(f"--- fields for: {pdf_path} ---\n")
    try:
        # open the pdf file
        doc = fitz.open(pdf_path)
        fields = {}

        # iterate through each page and find the fields (called "widgets")
        for page_num, page in enumerate(doc):
            for field in page.widgets():
                fields[field.field_name] = field.field_value or '' # store name and current value

        if fields:
            pprint.pprint(fields)
        else:
            print("no fillable fields found.")

    except Exception as e:
        print(f"an error occurred: {e}")

    finally:
        if 'doc' in locals():
            doc.close() # always make sure to close the file

    print("\n" + "-"*50 + "\n")


# run the function for the new files
# (make sure the filenames here match what's in your folder exactly)
get_pdf_fields_pymupdf('i-129 Template.pdf')
get_pdf_fields_pymupdf('i-589 Template.pdf')
get_pdf_fields_pymupdf('i-765 Template.pdf')
get_pdf_fields_pymupdf('n-400 Template.pdf')