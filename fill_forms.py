import fitz # the pymupdf library

# The master map of fields is correct
field_map = {
    "applicant a number": {
        "g-28": 'form1[0].#subform[1].Pt3Line9_ANumber[0]',
        "i-485": 'form1[0].#subform[0].AlienNumber[0]',
        "i-129": 'form1[0].#subform[2].Line1_AlienNumber[0]',
        "i-589": 'form1[0].#subform[0].PtAILine1_ANumber[0]',
        "i-765": 'form1[0].Page2[0].Line7_AlienNumber[0]',
        "n-400": [
            'form1[0].#subform[0].#area[0].Line1_AlienNumber[0]',
            'form1[0].#subform[1].#area[1].Line1_AlienNumber[1]',
            'form1[0].#subform[2].#area[2].Line1_AlienNumber[2]',
            'form1[0].#subform[3].#area[3].Line1_AlienNumber[3]',
            'form1[0].#subform[4].#area[4].Line1_AlienNumber[4]',
            'form1[0].#subform[5].#area[6].Line1_AlienNumber[5]',
            'form1[0].#subform[6].#area[7].Line1_AlienNumber[6]',
            'form1[0].#subform[7].#area[8].Line1_AlienNumber[7]',
            'form1[0].#subform[8].#area[9].Line1_AlienNumber[8]',
            'form1[0].#subform[9].#area[10].Line1_AlienNumber[9]',
            'form1[0].#subform[10].#area[11].Line1_AlienNumber[10]',
            'form1[0].#subform[11].#area[12].Line1_AlienNumber[11]',
            'form1[0].#subform[12].#area[13].Line1_AlienNumber[12]',
            'form1[0].#subform[13].#area[14].Line1_AlienNumber[13]'
        ]
    },
    "applicant last name": { "g-28": 'form1[0].#subform[1].Pt3Line5a_FamilyName[0]', "i-485": 'form1[0].#subform[0].Pt1Line1_FamilyName[0]', "i-129": 'form1[0].#subform[1].Part3_Line2_FamilyName[0]', "i-589": 'form1[0].#subform[0].PtAILine4_LastName[0]', "i-765": 'form1[0].Page1[0].Line1a_FamilyName[0]', "n-400": 'form1[0].#subform[0].P2_Line1_FamilyName[0]', },
    "applicant first name": { "g-28": 'form1[0].#subform[1].Pt3Line5b_GivenName[0]', "i-485": 'form1[0].#subform[0].Pt1Line1_GivenName[0]', "i-129": 'form1[0].#subform[1].Part3_Line2_GivenName[0]', "i-589": 'form1[0].#subform[0].PtAILine5_FirstName[0]', "i-765": 'form1[0].Page1[0].Line1b_GivenName[0]', "n-400": 'form1[0].#subform[0].P2_Line1_GivenName[0]', },
    "applicant middle name": { "g-28": 'form1[0].#subform[1].Pt3Line5c_MiddleName[0]', "i-485": 'form1[0].#subform[0].Pt1Line1_MiddleName[0]', "i-129": 'form1[0].#subform[1].Part3_Line2_MiddleName[0]', "i-589": 'form1[0].#subform[0].PtAILine6_MiddleName[0]', "i-765": 'form1[0].Page1[0].Line1c_MiddleName[0]', "n-400": 'form1[0].#subform[0].P2_Line1_MiddleName[0]', },
    "applicant date of birth": { "i-485": 'form1[0].#subform[0].Pt1Line3_DOB[0]', "i-129": 'form1[0].#subform[2].Line6_DateOfBirth[0]', "i-589": 'DateTimeField1[0]', "i-765": 'form1[0].Page3[0].Line19_DOB[0]', "n-400": 'form1[0].#subform[1].P2_Line8_DateOfBirth[0]', },
    "applicant uscis number": { "g-28": 'form1[0].#subform[1].#area[1].Pt3Line8_USCISOnlineAcctNumber[0]', "i-485": 'form1[0].#subform[1].Pt1Line9_USCISAccountNumber[0]', "i-589": 'TextField1[2]', "i-765": 'form1[0].Page2[0].Line8_ElisAccountNumber[0]', "n-400": 'form1[0].#subform[1].P2_Line6_USCISELISAcctNumber[0]', },
    "applicant ssn": { "i-129": 'form1[0].#subform[2].Line5_SSN[0]', "i-589": 'TextField1[1]', "i-765": 'form1[0].Page2[0].Line12b_SSN[0]', "n-400": 'form1[0].#subform[1].Line12b_SSN[0]', },
    "attorney bar number": { "g-28": 'form1[0].#subform[0].Pt2Line1b_BarNumber[0]', "i-485": 'form1[0].#subform[0].AttorneyStateBarNumber[0]', "i-589": 'form1[0].#subform[10].AttorneyStateBarNumber[0]', },
    "attorney last name": { "g-28": 'form1[0].#subform[0].Pt1Line2a_FamilyName[0]', },
    "attorney first name": { "g-28": 'form1[0].#subform[0].Pt1Line2b_GivenName[0]', },
}

# --- Main Program ---
available_forms = { "g-28": "g-28 Template.pdf", "i-129": "i-129 Template.pdf", "i-485": "i-485 Template.pdf", "i-589": "i-589 Template.pdf", "i-765": "i-765 Template.pdf", "n-400": "n-400 Template.pdf" }

# Form selection and user input
selected_forms = []
print("which forms do you need to file? (y/n)")
for short_name in sorted(available_forms.keys()):
    while True:
        choice = input(f"  - {short_name}? ").lower()
        if choice in ['y', 'n']:
            if choice == 'y':
                selected_forms.append(short_name)
            break
        else:
            print("invalid input. please enter 'y' or 'n'.")
if not selected_forms:
    print("no forms selected. exiting.")
    exit()
print(f"\nyou selected: {', '.join(selected_forms)}\n")
required_inputs = set()
for simple_name, form_dict in field_map.items():
    if any(form_name in selected_forms for form_name in form_dict.keys()):
        required_inputs.add(simple_name)
client_data = {}
print("please enter the following information:")
for key in sorted(list(required_inputs)):
    prompt = f"{key}: "
    client_data[key] = input(prompt)

# --- Final function with custom font loading ---
def fill_and_lock_form(input_path, output_path, data_dictionary, font_path=None, font_size=10):
    try:
        doc = fitz.open(input_path)
        
        # If a custom font is provided, register it and get its reference name
        font_ref = "Helv" # Default font
        if font_path:
            try:
                # Create a font reference name and insert the font
                font_alias = "CustomFont"
                doc.insert_font(fontfile=font_path, fontname=font_alias)
                font_ref = font_alias
            except Exception as e:
                print(f"  - warning: could not load font {font_path}. falling back to default. error: {e}")

        for page in doc:
            for field in page.widgets():
                if field.field_name in data_dictionary:
                    field.text_font = font_ref
                    field.text_fontsize = font_size
                    field.text_align = fitz.TEXT_ALIGN_CENTER # Center align all fields
                    field.field_value = str(data_dictionary[field.field_name])
                    field.field_flags = fitz.PDF_FIELD_IS_READ_ONLY
                    field.update()
        doc.save(output_path)
        doc.close()
        print(f"successfully created {output_path}")
    except Exception as e:
        print(f"could not process {input_path}. error: {e}")

# --- Main filling loop ---
print("\nstarting to fill pdfs...")
for form_name in selected_forms:
    form_data = {}
    for simple_name, value in client_data.items():
        if value and form_name in field_map.get(simple_name, {}):
            pdf_field_names = field_map[simple_name][form_name]
            
            if isinstance(pdf_field_names, list):
                for field_name in pdf_field_names:
                    form_data[field_name] = value
            else:
                form_data[pdf_field_names] = value
    
    input_filename = available_forms[form_name]
    output_filename = f"{form_name}_filled.pdf"
    
    # Conditional logic for font selection
    if form_name == "i-589":
        fill_and_lock_form(input_filename, output_filename, form_data, font_path=None)
    else:
        # Use our downloaded Courier Prime Bold font for all other forms
        fill_and_lock_form(input_filename, output_filename, form_data, font_path="CourierPrime-Bold.ttf")

print("\nall finished!")