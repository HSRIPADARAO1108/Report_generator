import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Dr. AIT Report Generator", page_icon="🎓", layout="centered")

st.title("🎓 Dr. AIT Lab Report Compiler")

# 1. Select Lab
lab_choice = st.selectbox("Select the Laboratory Course:", ["BDA (Big Data Analytics)", "ADBMS (Advanced DBMS)"])
manual_path = "BDA_Manual.pdf" if "BDA" in lab_choice else "ADBMS_Manual.pdf"

st.markdown("---")
col1, col2 = st.columns(2)
student_name = col1.text_input("Full Student Name:")
student_usn = col2.text_input("University Seat Number (USN):")

def create_overlay(name, usn):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # --- PAGE 1: COVER ---
    # Mask area: (x, y, width, height) - Covers where "SRIPADA RAO H" is
    can.setFillColorRGB(1, 1, 1)
    can.rect(150, 380, 400, 50, fill=True, stroke=False) 
    
    # Stamp new info
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Bold", 14)
    can.drawCentredString(306, 400, f"{name.upper()}      {usn.upper()}")
    can.showPage()
    
    # --- PAGE 2: CERTIFICATE ---
    # Mask area: Covers the name/USN in the certificate text
    can.setFillColorRGB(1, 1, 1)
    can.rect(80, 400, 450, 40, fill=True, stroke=False)
    
    # Stamp new info
    can.setFont("Times-Bold", 14)
    can.drawString(98, 415, name.upper())
    can.drawRightString(510, 415, usn.upper())
    
    can.showPage()
    can.save()
    packet.seek(0)
    return packet

if st.button("⚡ Generate Final PDF"):
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
            
            final_io = io.BytesIO()
            writer.write(final_io)
            final_io.seek(0)
            
            st.success("✨ Report Ready!")
            st.download_button("📥 Download Report", final_io, f"{student_usn.upper()}_Report.pdf", "application/pdf")
    else:
        st.error(f"Error: Ensure {manual_path} exists and fields are filled.")
