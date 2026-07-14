import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Dr. AIT Lab Report Compiler", page_icon="🎓", layout="centered")

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
    
    # --- PAGE 1: COVER ---
    can.setFillColorRGB(1, 1, 1)
    can.rect(100, 380, 420, 50, fill=True, stroke=False) 
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Bold", 14)
    can.drawString(100, 405, name.upper())
    can.drawString(420, 405, usn.upper())
    can.showPage()
    
    # --- PAGE 2: CERTIFICATE (FINAL FIX) ---
    # Wider mask to ensure no ghost text remains
    can.setFillColorRGB(1, 1, 1)
    can.rect(80, 400, 480, 30, fill=True, stroke=False)
    
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Bold", 14)
    # Name on left (x=90), USN pushed far right (x=460)
    can.drawString(90, 410, name.upper())
    can.drawString(460, 410, usn.upper())
    
    can.showPage()
    can.save()
    packet.seek(0)
    return packet

if st.button("⚡ Generate & Download PDF"):
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
            
            st.success("✨ Report Compiled Successfully!")
            st.download_button("📥 Download Final Report", final_io, f"{student_usn.upper()}_Report.pdf", "application/pdf")
    else:
        st.error(f"Error: Missing {manual_path} or fields empty.")
