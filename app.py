import tkinter as tk
from tkinter import ttk, messagebox
import fitz # the pymupdf library

# --- Predefined Profiles (Updated with radio button choices) ---
ATTORNEY_PROFILES = {
    "Gabriel": {
        "attorney first name": "Gabriel", "attorney last name": "DeLa Merced", "attorney middle name": "S",
        "attorney law firm": "GABRIEL S DELA MERCED", "attorney bar number": "2441319",
        "attorney phone number": "2123919090", "attorney mobile number": "9173797441",
        "attorney email address": "gdmlaw43w46@gmail.com", "attorney address street": "1 Liberty Plz 165 Broadway",
        "attorney address apt": "2362", "attorney address city": "New York", "attorney address state": "NY",
        "attorney address zip": "10006", "attorney address country": "USA",
        "checkboxes": ["g28_is_attorney"],
        "g28_address_unit": "Ste.",
        "g28_restriction_status": "am not"
    }, "None": {}
}
CLIENT_PROFILES = {
    "Test Client": {
        "applicant a number": "123456789", "applicant address apt": "4C", "applicant address city": "Elmhurst",
        "applicant address country": "United States of America", "applicant address state": "NY",
        "applicant address street": "81-43 Dongan Ave", "applicant address zip": "11373",
        "applicant date of birth": "09/04/2003", "applicant email address": "saimonghseng03@gmail.com",
        "applicant first name": "Saimong", "applicant last name": "Hseng", "applicant middle name": "",
        "applicant phone number": "6469208253", "applicant ssn": "120928959",
        "applicant uscis number": "123456789012", "other names used": "N/A",
        "country of birth": "USA", "country of citizenship": "USA", "date of last arrival": "01/01/2024",
        "i-94 number": "123456789", "passport number": "P12345", "sex": "Male", "marital status": "Single",
        "spouse last name": "", "spouse first name": "", "spouse date of birth": ""
    }, "None": {}
}

# --- Maps for Checkboxes and Radio Buttons ---
checkbox_map = { "g28_is_attorney": {"g-28": 'form1[0].#subform[0].CheckBox1[0]'} }
radio_button_map = {
    "g28_address_unit": { "label": "G-28 Addr. Unit:", "options": { "Apt.": {"g-28": 'form1[0].#subform[0].Line3b_Unit[0]'}, "Ste.": {"g-28": 'form1[0].#subform[0].Line3b_Unit[1]'}, "Flr.": {"g-28": 'form1[0].#subform[0].Line3b_Unit[2]'} } },
    "g28_restriction_status": { "label": "G-28 Restriction:", "options": { "am not": {"g-28": 'form1[0].#subform[0].Checkbox1dAmNot[0]'}, "am": {"g-28": 'form1[0].#subform[0].Checkbox1dAm[0]'} } },
    "sex": { "label": "Sex:", "options": { "Male": {"i-485": 'form1[0].#subform[1].Pt1Line6_CB_Sex[0]', "n-400": 'form1[0].#subform[1].P2_Line7_Gender[0]', "i-589": 'form1[0].#subform[0].PartALine9Sex[0]', "i-129": 'form1[0].#subform[2].Line1_Gender_P3[0]', "i-765": 'form1[0].Page2[0].Line10_Checkbox[0]'}, "Female": {"i-485": 'form1[0].#subform[1].Pt1Line6_CB_Sex[1]', "n-400": 'form1[0].#subform[1].P2_Line7_Gender[1]', "i-589": 'form1[0].#subform[0].PartALine9Sex[1]', "i-129": 'form1[0].#subform[2].Line1_Gender_P3[1]', "i-765": 'form1[0].Page2[0].Line10_Checkbox[1]'} } },
    "marital status": { "label": "Marital Status:", "options": { "Single": {"i-485": 'form1[0].#subform[9].Pt6Line1_MaritalStatus[0]', "n-400": 'form1[0].#subform[3].P10_Line1_MaritalStatus[0]', "i-589": 'form1[0].#subform[0].Marital[0]', "i-765": 'form1[0].Page2[0].Line11_MaritalStatus[0]'}, "Married": {"i-485": 'form1[0].#subform[9].Pt6Line1_MaritalStatus[1]', "n-400": 'form1[0].#subform[3].P10_Line1_MaritalStatus[1]', "i-589": 'form1[0].#subform[0].Marital[1]', "i-765": 'form1[0].Page2[0].Line11_MaritalStatus[1]'}, "Divorced": {"i-485": 'form1[0].#subform[9].Pt6Line1_MaritalStatus[2]', "n-400": 'form1[0].#subform[3].P10_Line1_MaritalStatus[2]', "i-589": 'form1[0].#subform[0].Marital[2]', "i-765": 'form1[0].Page2[0].Line11_MaritalStatus[2]'}, "Widowed": {"i-485": 'form1[0].#subform[9].Pt6Line1_MaritalStatus[3]', "n-400": 'form1[0].#subform[3].P10_Line1_MaritalStatus[3]', "i-589": 'form1[0].#subform[0].Marital[3]'} } }
}

# The complete field map
field_map = {
    "other names used": {"i-485": 'form1[0].#subform[0].Pt1Line2_FamilyName[0]', "n-400": 'form1[0].#subform[0].Line2_FamilyName1[0]', "i-589": 'form1[0].#subform[0].TextField1[0]', "i-129": 'form1[0].#subform[2].Line3_FamilyName1[0]', "i-765": 'form1[0].Page1[0].Line2a_FamilyName[0]'},
    "country of birth": {"i-485": 'form1[0].#subform[1].Pt1Line7_CountryOfBirth[0]', "n-400": 'form1[0].#subform[1].P2_Line10_CountryOfBirth[0]', "i-589": 'form1[0].#subform[0].TextField5[0]', "i-129": 'form1[0].#subform[2].Part3Line4_CountryOfBirth[0]', "i-765": 'form1[0].Page3[0].Line18c_CountryOfBirth[0]'},
    "country of citizenship": {"i-485": 'form1[0].#subform[1].Pt1Line8_CountryofCitizenshipNationality[0]', "n-400": 'form1[0].#subform[1].P2_Line11_CountryOfNationality[0]', "i-589": 'form1[0].#subform[0].TextField5[2]', "i-129": 'form1[0].#subform[2].Part3Line4_CountryOfCitizenship[0]', "i-765": 'form1[0].Page2[0].Line17a_CountryOfBirth[0]'},
    "date of last arrival": {"i-129": 'form1[0].#subform[2].Part3Line5_DateofArrival[0]', "i-485": 'form1[0].#subform[1].Pt1Line10_DateofArrival[0]', "i-589": 'form1[0].#subform[1].NotMarried[0].PtAIILine17_DateofLastEntry[0]', "i-765": 'form1[0].Page3[0].Line21_DateOfLastEntry[0]'},
    "i-94 number": {"i-129": 'form1[0].#subform[2].Part3Line5_ArrivalDeparture[0]', "i-485": 'form1[0].#subform[2].P1Line12_I94[0]', "i-589": 'form1[0].#subform[1].NotMarried[0].PtAIILine18_I94Number[0]', "i-765": 'form1[0].Page3[0].Line20a_I94Number[0]'},
    "passport number": {"i-129": 'form1[0].#subform[2].Part3Line5_PassportorTravDoc[0]', "i-485": 'form1[0].#subform[1].Pt1Line10_PassportNum[0]', "i-589": 'form1[0].#subform[0].TextField7[0]', "i-765": 'form1[0].Page3[0].Line20b_Passport[0]'},
    "spouse last name": {"i-485": 'form1[0].#subform[9].Pt6Line4_FamilyName[0]', "n-400": 'form1[0].#subform[3].P10_Line4a_FamilyName[0]'},
    "spouse first name": {"i-485": 'form1[0].#subform[9].Pt6Line4_GivenName[0]', "n-400": 'form1[0].#subform[3].P10_Line4a_GivenName[0]'},
    "spouse date of birth": {"n-400": 'form1[0].#subform[3].P10_Line4d_DateofBirth[0]'},
    "attorney middle name": {"g-28": 'form1[0].#subform[0].Pt1Line2c_MiddleName[0]'}, "attorney law firm": {"g-28": 'form1[0].#subform[0].Pt2Line1d_NameofFirmOrOrganization[0]'}, "attorney phone number": {"g-28": 'form1[0].#subform[0].Line4_DaytimeTelephoneNumber[0]'}, "attorney mobile number": {"g-28": 'form1[0].#subform[0].Line7_MobileTelephoneNumber[0]'}, "attorney email address": {"g-28": 'form1[0].#subform[0].Line6_EMail[0]'}, "attorney address street": {"g-28": 'form1[0].#subform[0].Line3a_StreetNumber[0]'}, "attorney address apt": {"g-28": 'form1[0].#subform[0].Line3b_AptSteFlrNumber[0]'}, "attorney address city": {"g-28": 'form1[0].#subform[0].Line3c_CityOrTown[0]'}, "attorney address state": {"g-28": 'form1[0].#subform[0].Line3d_State[0]'}, "attorney address zip": {"g-28": 'form1[0].#subform[0].Line3e_ZipCode[0]'}, "attorney address country": {"g-28": 'form1[0].#subform[0].Line3h_Country[0]'},
    "applicant phone number": { "g-28": 'form1[0].#subform[1].Line9_DaytimeTelephoneNumber[0]', "i-129": 'form1[0].#subform[0].Line2_DaytimePhoneNumber1_Part8[0]', "i-485": 'form1[0].#subform[22].P3_Line4_DaytimeTelePhoneNumber[0]', "i-589": 'form1[0].#subform[0].PtAILine8_TelephoneNumber[0]', "i-765": 'form1[0].Page4[0].Pt3Line3_DaytimePhoneNumber1[0]', "n-400": 'form1[0].#subform[10].P12_Line3_Telephone[0]', }, "applicant email address": { "g-28": 'form1[0].#subform[1].Line11_EMail[0]', "i-129": 'form1[0].#subform[0].Line9_EmailAddress[0]', "i-485": 'form1[0].#subform[22].P3_Line6_Email[0]', "i-765": 'form1[0].Page4[0].Pt3Line5_Email[0]', "n-400": 'form1[0].#subform[10].P12_Line5_Email[0]', },
    "applicant address street": { "g-28": 'form1[0].#subform[1].Line12a_StreetNumberName[0]', "i-129": 'form1[0].#subform[2].Line8a_StreetNumberName[0]', "i-485": 'form1[0].#subform[2].Pt1Line18_StreetNumberName[0]', "i-589": 'form1[0].#subform[0].PtAILine8_StreetNumandName[0]', "i-765": 'form1[0].Page2[0].Pt2Line7_StreetNumberName[0]', "n-400": 'form1[0].#subform[2].P4_Line1_StreetName[0]', }, "applicant address apt": { "g-28": 'form1[0].#subform[1].Line12b_AptSteFlrNumber[0]', "i-129": 'form1[0].#subform[2].Line6_AptSteFlrNumber[0]', "i-485": 'form1[0].#subform[2].Pt1Line18US_AptSteFlrNumber[0]', "i-589": 'form1[0].#subform[0].PtAILine8_AptNumber[0]', "i-765": 'form1[0].Page2[0].Pt2Line7_AptSteFlrNumber[0]', "n-400": 'form1[0].#subform[2].P4_Line1_Number[0]', }, "applicant address city": { "g-28": 'form1[0].#subform[1].Line12c_CityOrTown[0]', "i-129": 'form1[0].#subform[2].Line8d_CityTown[0]', "i-485": 'form1[0].#subform[2].Pt1Line18_CityOrTown[0]', "i-589": 'TextField1[4]', "i-765": 'form1[0].Page2[0].Pt2Line7_CityOrTown[0]', "n-400": 'form1[0].#subform[2].P4_Line1_City[0]', }, "applicant address state": { "g-28": 'form1[0].#subform[1].Line12d_State[0]', "i-129": 'form1[0].#subform[2].Line8e_State[0]', "i-485": 'form1[0].#subform[2].Pt1Line18_State[0]', "i-589": 'form1[0].#subform[0].PtAILine8_State[0]', "i-765": 'form1[0].Page2[0].Pt2Line7_State[0]', "n-400": 'form1[0].#subform[2].P4_Line1_State[0]', }, "applicant address zip": { "g-28": 'form1[0].#subform[1].Line12e_ZipCode[0]', "i-129": 'form1[0].#subform[2].Line8f_ZipCode[0]', "i-485": 'form1[0].#subform[2].Pt1Line18_ZipCode[0]', "i-589": 'form1[0].#subform[0].PtAILine8_Zipcode[0]', "i-765": 'form1[0].Page2[0].Pt2Line7_ZipCode[0]', "n-400": 'form1[0].#subform[2].P4_Line1_ZipCode[0]', }, "applicant address country": { "g-28": 'form1[0].#subform[1].Line12h_Country[0]', "n-400": 'form1[0].#subform[2].P4_Line1_Country[0]', },
    "applicant a number": { "g-28": 'form1[0].#subform[1].Pt3Line9_ANumber[0]', "i-485": 'form1[0].#subform[0].AlienNumber[0]', "i-129": 'form1[0].#subform[2].Line1_AlienNumber[0]', "i-589": 'form1[0].#subform[0].PtAILine1_ANumber[0]', "i-765": 'form1[0].Page2[0].Line7_AlienNumber[0]', "n-400": [ 'form1[0].#subform[0].#area[0].Line1_AlienNumber[0]', 'form1[0].#subform[1].#area[1].Line1_AlienNumber[1]', 'form1[0].#subform[2].#area[2].Line1_AlienNumber[2]', 'form1[0].#subform[3].#area[3].Line1_AlienNumber[3]', 'form1[0].#subform[4].#area[4].Line1_AlienNumber[4]', 'form1[0].#subform[5].#area[6].Line1_AlienNumber[5]', 'form1[0].#subform[6].#area[7].Line1_AlienNumber[6]', 'form1[0].#subform[7].#area[8].Line1_AlienNumber[7]', 'form1[0].#subform[8].#area[9].Line1_AlienNumber[8]', 'form1[0].#subform[9].#area[10].Line1_AlienNumber[9]', 'form1[0].#subform[10].#area[11].Line1_AlienNumber[10]', 'form1[0].#subform[11].#area[12].Line1_AlienNumber[11]', 'form1[0].#subform[12].#area[13].Line1_AlienNumber[12]', 'form1[0].#subform[13].#area[14].Line1_AlienNumber[13]' ] },
    "applicant last name": { "g-28": 'form1[0].#subform[1].Pt3Line5a_FamilyName[0]', "i-485": 'form1[0].#subform[0].Pt1Line1_FamilyName[0]', "i-129": 'form1[0].#subform[1].Part3_Line2_FamilyName[0]', "i-589": 'form1[0].#subform[0].PtAILine4_LastName[0]', "i-765": 'form1[0].Page1[0].Line1a_FamilyName[0]', "n-400": 'form1[0].#subform[0].P2_Line1_FamilyName[0]', }, "applicant first name": { "g-28": 'form1[0].#subform[1].Pt3Line5b_GivenName[0]', "i-485": 'form1[0].#subform[0].Pt1Line1_GivenName[0]', "i-129": 'form1[0].#subform[1].Part3_Line2_GivenName[0]', "i-589": 'form1[0].#subform[0].PtAILine5_FirstName[0]', "i-765": 'form1[0].Page1[0].Line1b_GivenName[0]', "n-400": 'form1[0].#subform[0].P2_Line1_GivenName[0]', }, "applicant middle name": { "g-28": 'form1[0].#subform[1].Pt3Line5c_MiddleName[0]', "i-485": 'form1[0].#subform[0].Pt1Line1_MiddleName[0]', "i-129": 'form1[0].#subform[1].Part3_Line2_MiddleName[0]', "i-589": 'form1[0].#subform[0].PtAILine6_MiddleName[0]', "i-765": 'form1[0].Page1[0].Line1c_MiddleName[0]', "n-400": 'form1[0].#subform[0].P2_Line1_MiddleName[0]', },
    "applicant date of birth": { "i-485": 'form1[0].#subform[0].Pt1Line3_DOB[0]', "i-129": 'form1[0].#subform[2].Line6_DateOfBirth[0]', "i-589": 'DateTimeField1[0]', "i-765": 'form1[0].Page3[0].Line19_DOB[0]', "n-400": 'form1[0].#subform[1].P2_Line8_DateOfBirth[0]', }, "applicant uscis number": { "g-28": 'form1[0].#subform[1].#area[1].Pt3Line8_USCISOnlineAcctNumber[0]', "i-485": 'form1[0].#subform[1].Pt1Line9_USCISAccountNumber[0]', "i-589": 'TextField1[2]', "i-765": 'form1[0].Page2[0].Line8_ElisAccountNumber[0]', "n-400": 'form1[0].#subform[1].P2_Line6_USCISELISAcctNumber[0]', }, "applicant ssn": { "i-129": 'form1[0].#subform[2].Line5_SSN[0]', "i-589": 'TextField1[1]', "i-765": 'form1[0].Page2[0].Line12b_SSN[0]', "n-400": 'form1[0].#subform[1].Line12b_SSN[0]', },
    "attorney bar number": { "g-28": 'form1[0].#subform[0].Pt2Line1b_BarNumber[0]', "i-485": 'form1[0].#subform[0].AttorneyStateBarNumber[0]', "i-589": 'form1[0].#subform[10].AttorneyStateBarNumber[0]', }, "attorney last name": { "g-28": 'form1[0].#subform[0].Pt1Line2a_FamilyName[0]', }, "attorney first name": { "g-28": 'form1[0].#subform[0].Pt1Line2b_GivenName[0]', },
}
available_forms = { "g-28": "g-28 Template.pdf", "i-129": "i-129 Template.pdf", "i-485": "i-485 Template.pdf", "i-589": "i-589 Template.pdf", "i-765": "i-765 Template.pdf", "n-400": "n-400 Template.pdf" }

# --- Application Functions ---

def on_generate_click(selected_forms, all_widgets, finalize_var):
    client_data = {key: widget.get() for key, widget in all_widgets.items()}
    is_finalized = finalize_var.get()
    
    if "applicant address state" in client_data: client_data["applicant address state"] = client_data["applicant address state"].upper()
    a_num = client_data.get("applicant a number", ""); uscis_num = client_data.get("applicant uscis number", "")
    if a_num and len(a_num) != 9: messagebox.showerror("Validation Error", "A-Number must be exactly 9 digits or blank."); return
    if uscis_num and len(uscis_num) != 12: messagebox.showerror("Validation Error", "USCIS Number must be exactly 12 digits or blank."); return

    for form_name in selected_forms:
        form_data = {}
        # Handle text fields
        for simple_name, value in client_data.items():
            if isinstance(value, str) and value and form_name in field_map.get(simple_name, {}):
                pdf_field_names = field_map[simple_name][form_name]
                if isinstance(pdf_field_names, list):
                    for field_name in pdf_field_names: form_data[field_name] = value
                else: form_data[pdf_field_names] = value
        
        # Handle checkboxes and radio buttons
        for key, value in client_data.items():
            if isinstance(value, bool) and value is True and form_name in checkbox_map.get(key, {}): # Checkboxes
                form_data[checkbox_map[key][form_name]] = "Yes"
            elif isinstance(value, str) and value and key in radio_button_map: # Radio buttons
                if value in radio_button_map[key]["options"] and form_name in radio_button_map[key]["options"][value]:
                    form_data[radio_button_map[key]["options"][value][form_name]] = "Yes"

        input_filename = available_forms[form_name]; output_filename = f"{form_name}_filled.pdf"
        if is_finalized: fill_and_lock_form(input_filename, output_filename, form_data)
        else: fill_editable_form(input_filename, output_filename, form_data)
        
    messagebox.showinfo("Success", f"PDFs have been generated! (Editable: {not is_finalized})")

def fill_editable_form(input_path, output_path, data_dictionary):
    try:
        doc = fitz.open(input_path); doc.need_appearances = True
        for page in doc:
            for field in page.widgets():
                if field.field_name in data_dictionary: field.field_value = str(data_dictionary[field.field_name]); field.update()
        doc.save(output_path, garbage=4, deflate=True, clean=True); doc.close()
    except Exception as e: messagebox.showerror("Error", f"Could not process {input_path}.\nError: {e}")
def fill_and_lock_form(input_path, output_path, data_dictionary):
    try:
        doc = fitz.open(input_path)
        for page in doc:
            for field in page.widgets():
                if field.field_name in data_dictionary:
                    field.field_value = str(data_dictionary[field.field_name]); field.field_flags = fitz.PDF_FIELD_IS_READ_ONLY; field.update()
        doc.save(output_path)
    except Exception as e: messagebox.showerror("Error", f"Could not process {input_path}.\nError: {e}")

def load_profile_data(profile_data, all_widgets):
    for key, value in profile_data.items():
        if key in all_widgets:
            widget = all_widgets[key]
            if isinstance(widget, tk.BooleanVar): widget.set(key in profile_data.get("checkboxes", []))
            elif isinstance(widget, tk.StringVar): widget.set(value)
            else: widget.delete(0, tk.END); widget.insert(0, value)

def clear_fields(all_widgets, field_type):
    for key, widget in all_widgets.items():
        is_attorney_field = key.startswith("attorney") or key.startswith("g28")
        if (field_type == "attorney" and is_attorney_field) or (field_type == "client" and not is_attorney_field):
            if isinstance(widget, tk.BooleanVar): widget.set(False)
            elif isinstance(widget, tk.StringVar): widget.set("")
            else: widget.delete(0, tk.END)

# --- NEW: show_input_fields with dynamic marital section ---
def show_input_fields(selected_forms):
    selection_frame.pack_forget()
    all_req_text = {k for k, v in field_map.items() if any(f in selected_forms for f in v)}
    all_req_radio = {k for k, d in radio_button_map.items() if any(f in selected_forms for v in d['options'].values() for f in v)}
    all_req_check = {k for k, v in checkbox_map.items() if any(f in selected_forms for f in v)}

    # Separate keys into logical groups for UI layout
    client_text_inputs = sorted([k for k in all_req_text if "applicant" in k and "spouse" not in k])
    client_spouse_inputs = sorted([k for k in all_req_text if "spouse" in k])
    client_radio_inputs = sorted([k for k in all_req_radio if not k.startswith("g28")])
    
    attorney_text_inputs = sorted([k for k in all_req_text if k.startswith("attorney")])
    attorney_radio_inputs = sorted([k for k in all_req_radio if k.startswith("g28")])
    attorney_check_inputs = sorted([k for k in all_req_check if k.startswith("g28")])

    main_frame = ttk.Frame(window); main_frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(main_frame); canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview); scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set); canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    def _on_mousewheel(event):
        if event.num == 5 or event.delta < 0: canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0: canvas.yview_scroll(-1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel); canvas.bind_all("<Button-4>", _on_mousewheel); canvas.bind_all("<Button-5>", _on_mousewheel)
    scrollable_frame = ttk.Frame(canvas); canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.columnconfigure(0, weight=1); scrollable_frame.columnconfigure(1, weight=1)
    
    all_widgets = {}
    
    # --- Client Column ---
    client_frame = ttk.LabelFrame(scrollable_frame, text="Client Information", padding=(10, 5)); client_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5); client_frame.columnconfigure(1, weight=1)
    
    row_counter = 1
    for key in client_radio_inputs:
        details = radio_button_map[key]
        label_text = details['label']
        ttk.Label(client_frame, text=label_text).grid(row=row_counter, column=0, sticky="w", padx=5, pady=(5,0))
        var = tk.StringVar(); all_widgets[key] = var
        radio_frame = ttk.Frame(client_frame); radio_frame.grid(row=row_counter, column=1, sticky='w')
        for i, option in enumerate(details["options"]):
            rb = ttk.Radiobutton(radio_frame, text=option, variable=var, value=option)
            rb.grid(row=0, column=i, padx=2)
        row_counter += 1
    
    for key in client_text_inputs:
        label_text = key.replace(" uscis", " USCIS").replace(" ssn", " SSN").replace(" a number", " A Number").title()
        ttk.Label(client_frame, text=f"{label_text}:").grid(row=row_counter, column=0, sticky="w", padx=5, pady=2)
        entry = ttk.Entry(client_frame); entry.grid(row=row_counter, column=1, sticky="ew", padx=5, pady=2); all_widgets[key] = entry
        row_counter += 1

    marital_frame = ttk.LabelFrame(client_frame, text="Marital Information", padding=(10, 5))
    marital_frame.grid(row=row_counter, column=0, columnspan=2, sticky="nsew", padx=5, pady=10)
    marital_frame.columnconfigure(1, weight=1)
    
    for i, key in enumerate(client_spouse_inputs):
        label_text = key.title()
        ttk.Label(marital_frame, text=f"{label_text}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)
        entry = ttk.Entry(marital_frame); entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2); all_widgets[key] = entry

    def toggle_marital_info(*args):
        marital_status = all_widgets.get("marital status", tk.StringVar(value="Single")).get()
        if marital_status == "Single":
            marital_frame.grid_remove()
        else:
            marital_frame.grid()
    
    if "marital status" in all_widgets:
        all_widgets["marital status"].trace("w", toggle_marital_info)
        toggle_marital_info()

    # --- Attorney Column ---
    attorney_frame = ttk.LabelFrame(scrollable_frame, text="Attorney Information", padding=(10, 5)); attorney_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5); attorney_frame.columnconfigure(1, weight=1)
    
    row_counter = 1
    for key in attorney_text_inputs:
        label_text = key.replace(" uscis", " USCIS").title()
        ttk.Label(attorney_frame, text=f"{label_text}:").grid(row=row_counter, column=0, sticky="w", padx=5, pady=2)
        entry = ttk.Entry(attorney_frame); entry.grid(row=row_counter, column=1, sticky="ew", padx=5, pady=2); all_widgets[key] = entry
        row_counter += 1
    
    ttk.Separator(attorney_frame, orient='horizontal').grid(row=row_counter, column=0, columnspan=2, sticky='ew', pady=5); row_counter += 1
    
    for key in attorney_check_inputs:
        var = tk.BooleanVar(); all_widgets[key] = var
        label_text = key.replace("_", " ").title()
        ttk.Checkbutton(attorney_frame, text=label_text, variable=var).grid(row=row_counter, column=0, columnspan=2, sticky='w', padx=5); row_counter += 1
    
    for key in attorney_radio_inputs:
        details = radio_button_map[key]
        ttk.Label(attorney_frame, text=details['label']).grid(row=row_counter, column=0, sticky='w', padx=5, pady=(5,0))
        var = tk.StringVar(); all_widgets[key] = var
        radio_frame = ttk.Frame(attorney_frame); radio_frame.grid(row=row_counter, column=1, sticky='w')
        for i, option in enumerate(details["options"]):
            ttk.Radiobutton(radio_frame, text=option, variable=var, value=option).grid(row=0, column=i, padx=2)
        row_counter += 1

    # --- Load/Clear Section ---
    load_frame = ttk.LabelFrame(scrollable_frame, text="Load & Clear", padding=(10, 5)); load_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
    
    global client_var, attorney_var
    ttk.Label(load_frame, text="Load Attorney:").pack(side='left', padx=(0,5)); 
    attorney_var = tk.StringVar(value="None"); ttk.OptionMenu(load_frame, attorney_var, "None", *ATTORNEY_PROFILES.keys(), command=lambda s: load_profile_data(ATTORNEY_PROFILES.get(s, {}), all_widgets)).pack(side='left', padx=5)
    ttk.Button(load_frame, text="Clear Attorney", command=lambda: clear_fields(all_widgets, "attorney")).pack(side='left', padx=5)
    
    ttk.Label(load_frame, text="Load Client:").pack(side='left', padx=(20,5)); 
    client_var = tk.StringVar(value="None"); ttk.OptionMenu(load_frame, client_var, "None", *CLIENT_PROFILES.keys(), command=lambda s: load_profile_data(CLIENT_PROFILES.get(s, {}), all_widgets)).pack(side='left', padx=5)
    ttk.Button(load_frame, text="Clear Client", command=lambda: clear_fields(all_widgets, "client")).pack(side='left', padx=5)
    
    # --- Validation Logic ---
    state_vcmd = (window.register(lambda P: (len(P) <= 2 and P.isalpha()) or P == ""), '%P'); anum_vcmd = (window.register(lambda p: (len(p) <= 9 and p.isdigit()) or p == ""), '%P'); uscis_vcmd = (window.register(lambda p: (len(p) <= 12 and p.isdigit()) or p == ""), '%P')
    for key, widget in all_widgets.items():
        if isinstance(widget, ttk.Entry):
            if "state" in key: widget.config(validate="key", validatecommand=state_vcmd)
            elif "a number" in key: widget.config(validate="key", validatecommand=anum_vcmd)
            elif "uscis number" in key: widget.config(validate="key", validatecommand=uscis_vcmd)

    # --- Bottom Controls ---
    finalize_var = tk.BooleanVar()
    ttk.Checkbutton(scrollable_frame, text="Finalize for submission (read-only, visible everywhere)", variable=finalize_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=10, pady=10)
    ttk.Button(scrollable_frame, text="Generate PDFs", command=lambda: on_generate_click(selected_forms, all_widgets, finalize_var)).grid(row=3, column=0, columnspan=2, pady=10)

def on_next_click():
    selected_forms = [form for form, var in checkbox_vars.items() if var.get()]; 
    if not selected_forms: messagebox.showwarning("No Selection", "Please select at least one form."); return
    show_input_fields(selected_forms)

# --- GUI Setup ---
window = tk.Tk(); window.title("PDF Form Filler"); window.geometry("850x700")
selection_frame = ttk.LabelFrame(window, text="1. Select Forms to File", padding=(20, 10)); selection_frame.pack(fill="x", padx=10, pady=10)
checkbox_vars = {}
for form_name in sorted(available_forms.keys()):
    var = tk.BooleanVar(); ttk.Checkbutton(selection_frame, text=form_name, variable=var).pack(anchor="w", padx=5, pady=2); checkbox_vars[form_name] = var
ttk.Button(selection_frame, text="Next", command=on_next_click).pack(pady=10)
window.mainloop()