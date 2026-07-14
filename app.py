import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Page configuration
st.set_page_config(page_title="Dr. AIT Lab Report Compiler", page_icon="🎓", layout="centered")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    div.stButton > button:first-child { 
        background-color: #1e3a8a !important; 
        color: white !important; 
        border-radius: 6px; 
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Dr. AIT Lab Report Compiler")
st.markdown("Select your course, enter student credentials, and generate a professional, print-ready PDF.")

# 1. Lab Selection
lab_choice = st.selectbox("Select the Laboratory Course:", ["BDA (Big Data Analytics)", "ADBMS (Advanced DBMS)"])

# 2. File Path Mapping
template_path = "BDA FRONT PAGE1_merged.pdf"
if lab_choice == "BDA (Big Data Analytics)":
    manual_path = "BAD_Manual.pdf"
    lab_full_title = "BIG DATA ANALYTICS LABREPORT(MCSL207)"
else:
    manual_path = "ADBMS_Manual.pdf"
    lab_full_title = "ADVANCES IN DATABASE MANAGEMENT SYSTEM LABREPORT"

st.markdown("---")

# 3. Input Matrix
col1, col2 = st.columns(2)
student_name = col1.text_input("Full Student Name:")
student_usn = col2.text_input("University Seat Number (USN):")

def create_overlay(name, usn, title):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # --- PAGE 1: COVER ---
    # Erase old info
    can.setFillColorRGB(1, 1, 1)
    can.rect(80, 380, 450, 60, fill=True, stroke=False)
    
    # Stamp new info (Times-Bold 14)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Bold", 14)
    can.drawCentredString(306, 420, title)
    can.drawCentredString(306, 400, f"{name.upper()}      {usn.upper()}")
    can.showPage()
    
    # --- PAGE 2: CERTIFICATE ---
    # Erase old info
    can.setFillColorRGB(1, 1, 1)
    can.rect(75, 400, 460, 40, fill=True, stroke=False)
    
    # Stamp new info
    can.setFont("Times-Bold", 14)
    can.drawString(98, 412, name.upper())
    can.drawRightString(510, 412, usn.upper())
    
    can.showPage()
    can.save()
    packet.seek(0)
    return packet

# 4. Compilation Engine
if st.button("⚡ Compile & Generate PDF"):
    if student_name and student_usn:
        if os.path.exists(template_path) and os.path.exists(manual_path):
            with st.spinner(f"Compiling {lab_choice} report..."):
                try:
                    overlay_stream = create_overlay(student_name, student_usn, lab_full_title)
                    
                    writer = PdfWriter()
                    template = PdfReader(template_path)
                    overlay = PdfReader(overlay_stream)
                    manual = PdfReader(manual_path)
                    
                    # Merge pages
                    for i in range(2):
                        page = template.pages[i]
                        page.merge_page(overlay.pages[i])
                        writer.add_page(page)
                    
                    # Append body
                    for page in manual.pages:
                        writer.add_page(page)
                        
                    final_io = io.BytesIO()
                    writer.write(final_io)
                    final_io.seek(0)
                    
                    st.success("✨ Report successfully compiled!")
                    st.download_button(
                        label="📥 Download PDF", 
                        data=final_io, 
                        file_name=f"{student_usn.upper()}_{lab_choice[:4]}_Report.pdf", 
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error during compilation: {e}")
        else:
            st.error(f"Missing required file: Ensure {manual_path} is in the repository.")
    else:
        st.warning("Please enter both Name and USN.")
