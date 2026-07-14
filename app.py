import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter, PageObject
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# Page setup layout
st.set_page_config(
    page_title="Dr. AIT BDA Report Generator", 
    page_icon="🎓", 
    layout="centered"
)

# Professional Slate Theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
    }
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #f8fafc !important;
    }
    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    div.stButton > button:first-child {
        background-color: #1e3a8a !important;
        color: white !important;
        border-radius: 6px;
        width: 100%;
        border: none;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 Dr. AIT BDA Lab Report Compiler")
st.markdown("Enter student credentials below to generate a fully updated, compiled, print-ready laboratory manual.")

st.markdown("---")

manual_pdf_path = "BAD_Manual_merged.pdf"

# Check system state
st.sidebar.header("📦 System Resource Status")
resources_ready = True

if os.path.exists(manual_pdf_path):
    st.sidebar.success("Base Lab Manual Loaded")
else:
    st.sidebar.error("Missing: BAD_Manual_merged.pdf")
    resources_ready = False

# --- STUDENT INPUT MATRIX ---
st.subheader("👤 Enter Student Credentials")
col1, col2 = st.columns(2)
student_name = col1.text_input("Full Student Name:", placeholder="e.g. CHETHAN PRASAD L")
student_usn = col2.text_input("University Seat Number (USN):", placeholder="e.g. 1DA25SCS04")

# Core function to generate the complete document from scratch dynamically to avoid Linux conversion bugs
def generate_complete_report(name, usn, base_manual_path):
    pdf_buffer = io.BytesIO()
    # Margins matching official report parameters
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                            rightMargin=54, leftMargin=54, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Typographical Styles matching Dr. AIT document parameters
    inst_style = ParagraphStyle('Inst', parent=styles['Heading1'], fontSize=18, leading=22, alignment=TA_CENTER, textColor='#1e3a8a', spaceAfter=4)
    sub_inst_style = ParagraphStyle('SubInst', parent=styles['Normal'], fontSize=10, leading=14, alignment=TA_CENTER, textColor='#475569', spaceAfter=4)
    dept_style = ParagraphStyle('Dept', parent=styles['Heading2'], fontSize=14, leading=18, alignment=TA_CENTER, textColor='#0f172a', spaceAfter=20)
    report_title = ParagraphStyle('RepTitle', parent=styles['Heading1'], fontSize=22, leading=26, alignment=TA_CENTER, textColor='#1e3a8a', spaceAfter=10)
    meta_label = ParagraphStyle('MetaLabel', parent=styles['Normal'], fontSize=12, leading=16, alignment=TA_CENTER, textColor='#334155', spaceAfter=15)
    cert_body = ParagraphStyle('CertBody', parent=styles['Normal'], fontSize=12, leading=22, alignment=TA_JUSTIFY, textColor='#1e293b', spaceAfter=30)
    
    # ==================== PAGE 1: COVER PAGE ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</b>", inst_style))
    story.append(Paragraph("(An Autonomous Institute, Affiliated to Visvesvaraya Technological University, Belagavi, Accredited by NAAC, with \"A\" Grade)", sub_inst_style))
    story.append(Paragraph("Near Jnana Bharathi Campus, Bangalore – 560056", sub_inst_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</b>", dept_style))
    story.append(Paragraph("Master of Technology<br/>in<br/>Computer Science and Engineering", meta_label))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>“ BIG DATA ANALYTICS LAB REPORT ”</b>", report_title))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<i>Submitted by</i>", meta_label))
    story.append(Paragraph(f"<b>{name.upper()} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {usn.upper()}</b>", inst_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<i>Under the Guidance of</i>", meta_label))
    story.append(Paragraph("<b>Dr. Prabha R</b><br/>Professor & HOD, Dept. of ISE, Dr. AIT", sub_inst_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Visvesvaraya Technological University</b><br/>Jnana Sangama, Belagavi, Karnataka 590018", sub_inst_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>For the academic year 2026 - 2027</b>", meta_label))
    
    story.append(PageBreak())
    
    # ==================== PAGE 2: CERTIFICATE ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</b>", inst_style))
    story.append(Paragraph("(An Autonomous Institute, affiliated to VTU, Belagavi, Accredited by NAAC with ‘A’ Grade)", sub_inst_style))
    story.append(Paragraph("Near Jnana Bharathi Campus, Bengaluru – 560056", sub_inst_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>CERTIFICATE</b></u>", report_title))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>“BDA Laboratory”</b>", dept_style))
    
    cert_text = f"This is to certify that the submitted document in the partial fulfillment of the requirement of the M.Tech 2nd semester BDA laboratory curriculum during the year 2025-26 is a result of Bonafide work carried out by <b>{name.upper()}</b> bearing University Seat Number <b>{usn.upper()}</b>."
    story.append(Paragraph(cert_text, cert_body))
    
    story.append(Spacer(1, 80))
    story.append(Paragraph("<b>Signature of the Incharge &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Head of Department, ISE</b>", sub_inst_style))
    story.append(Paragraph("Dr. Prabha R &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Dr. Prabha R", sub_inst_style))
    story.append(Spacer(1, 60))
    story.append(Paragraph("<b>Internal Examiner &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; External Examiner</b>", sub_inst_style))
    
    doc.build(story)
    pdf_buffer.seek(0)
    
    # Now merge with the master manual PDF
    pdf_writer = PdfWriter()
    front_reader = PdfReader(pdf_buffer)
    manual_reader = PdfReader(base_manual_path)
    
    # Append newly customized front page and certificate
    for page in front_reader.pages:
        pdf_writer.add_page(page)
        
    # Append the entire lab report manual text pages
    for page in manual_reader.pages:
        pdf_writer.add_page(page)
        
    final_output_io = io.BytesIO()
    pdf_writer.write(final_output_io)
    final_output_io.seek(0)
    return final_output_io

# --- GENERATION PIPELINE ENGINE ---
if resources_ready:
    if student_name.strip() and student_usn.strip():
        st.markdown("---")
        
        if st.button("⚡ Compile & Generate Full Printable Report"):
            with st.spinner("Compiling custom institutional coversheets and merging manual files..."):
                try:
                    # Run the dynamic compilation pipeline
                    compiled_report = generate_complete_report(
                        student_name, student_usn, manual_pdf_path
                    )
                    
                    st.success("✨ Report compiled successfully! The entered Name and USN have been visually rendered onto the front pages.")
                    
                    # File download utility trigger
                    st.download_button(
                        label="📥 Download Finished Lab Report (PDF)",
                        data=compiled_report,
                        file_name=f"{student_usn.upper()}_BDA_Complete_Report.pdf",
                        mime="application/pdf"
                    )
                    
                except Exception as engine_err:
                    st.error("🚨 An issue occurred during report compilation loops.")
                    st.exception(engine_err)
    else:
        st.info("💡 Please type in the Student Name and USN above to activate the automated compiler.")
else:
    st.error("🚨 Configuration Error: Please ensure 'BAD_Manual_merged.pdf' is present in your GitHub repository.")
