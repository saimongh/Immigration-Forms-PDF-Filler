# Immigration Form Automation Tool

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Library](https://img.shields.io/badge/PDF-PyMuPDF-red)
![Status](https://img.shields.io/badge/Status-Active-success)

A specialized Python application designed to automate the population of complex USCIS immigration forms (G-28, N-400, etc.). 

Developed during my tenure as a **Legal Intern**, this tool addresses the significant inefficiency of manual data entry in legal workflows. It utilizes a custom GUI to map client data to multiple PDF headers simultaneously, ensuring data consistency and reducing administrative time by eliminating redundant keystrokes.

---

## ⚡ Key Objectives
* **Efficiency:** Enter client and attorney data once; populate it across multiple distinct forms instantly.
* **Accuracy:** Implements real-time input validation (Regex) to prevent common clerical errors in sensitive fields (e.g., A-Numbers, USCIS Account Numbers).
* **Compatibility:** Generates both "Editable" PDFs for attorney review and "Finalized" (Flattened) PDFs for submission, resolving compatibility issues with macOS Preview and other PDF viewers.

---

## 🛠 Technical Architecture

This application is built on a modular architecture separating the GUI presentation layer from the PDF manipulation logic.

### Core Stack
* **Language:** Python 3.10+
* **GUI Framework:** **Tkinter** (chosen for native cross-platform compatibility and lightweight footprint).
* **PDF Engine:** **PyMuPDF (fitz)** (utilized for its high-performance handling of PDF field annotations, widget flattening, and coordinate mapping).

### Key Features
| Feature | Technical Implementation |
| :--- | :--- |
| **Dynamic Form Mapping** | The application reads from a dictionary of field maps, allowing the UI to render only the input fields required for the specific forms selected by the user. |
| **Input Validation** | Uses event listeners to enforce data types (e.g., 9-digit integers for Alien Registration Numbers) and formatting (e.g., auto-capitalizing state codes). |
| **Conditional Logic** | The GUI updates in real-time; for example, the "Marital Information" frame is programmatically hidden or revealed based on the client's selected marital status. |
| **PDF Flattening** | Includes a custom "Finalize" pipeline that bakes widget data into the PDF stream, ensuring the document is immutable and visible in non-Adobe viewers. |

---

## 🚀 Installation & Usage

### Prerequisites
* Python 3.x installed.

### 1. Installation
Clone the repository and install the required dependencies (primarily PyMuPDF).

```bash
git clone [https://github.com/saimongh/Immigration-Forms-PDF-Filler.git](https://github.com/saimongh/Immigration-Forms-PDF-Filler.git)
cd Immigration-Forms-PDF-Filler
pip install pymupdf
