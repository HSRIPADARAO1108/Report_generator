import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Dr. AIT Report Generator", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    div.stButton > button:first-child { background-color: #1e3a8a !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Dr. AIT Lab Report Compiler")

lab_choice = st.selectbox("Select the Laboratory Course:", ["BDA (Big Data Analytics)", "ADBMS (Advanced DBMS)"])
manual_path = "BDA_Manual.pdf" if "BDA" in lab_choice else "ADBMS_Manual.pdf"

st.markdown("---")
col1, col2 = st.columns(2)
student_name = col1.text_input("Full Student Name:")
student_usn = col2.text_input("University Seat Number (USN):")

def create_overlay(name, usn):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Page 1 Mask & Stamp
    can.setFillColorRGB(1, 1, 1)
    can.rect(100, 380, 420, 50, fill=True, stroke=False) 
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Bold", 14)
    can.drawCentredString(306, 405, name.upper())
    can.drawCentredString(306, 385, usn.upper())
    can.showPage()
    
    # Page 2 Mask & Stamp
    can.setFillColorRGB(1, 1, 1)
    can.rect(80, 400, 450, 30, fill=True, stroke=False)
    can.setFont("Times-Bold", 14)
    can.drawString(98, 408, name.upper())
    can.drawRightString(510, 408, usn.upper())
    
    can.showPage()
    can.save()
    packet.seek(0)
    return packet

# 2. Compilation Engine
if 'compiled_pdf_io' not in st.session_state:
    st.session_state.compiled_pdf_io = None

if st.button("⚡ Compile Report"):
    if student_name and student_usn and os.path.exists(manual_path):
        with st.spinner("Processing..."):
            overlay_stream = create_overlay(student_name, student_usn)
            
            reader = PdfReader(manual_path)
            writer = PdfWriter()
            overlay = PdfReader(overlay_stream)
            
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                if i < 2:
                    page.merge_page(overlay.pages[i])
                writer.add_page(page)
            
            # Store the BytesIO object directly in session state
            final_io = io.BytesIO()
            writer.write(final_io)
            final_io.seek(0)
            st.session_state.compiled_pdf_io = final_io
            st.success("✨ Report Compiled! Scroll down to preview.")
    else:
        st.error(f"Error: Ensure {manual_path} exists and fields are filled.")

# 3. Preview & Download
if st.session_state.compiled_pdf_io:
    st.markdown("---")
    st.subheader("👁️ Preview Report")
    # Now passing the BytesIO object which st.pdf() supports
    st.pdf(st.session_state.compiled_pdf_io)
    
    # Reset pointer for download
    st.session_state.compiled_pdf_io.seek(0)
    st.download_button(
        label="📥 Download Final Report",
        data=st.session_state.compiled_pdf_io,
        file_name=f"{student_usn.upper()}_Report.pdf",
        mime="application/pdf"
    )
