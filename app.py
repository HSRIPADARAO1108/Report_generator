import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_config(page_title="Dr. AIT Lab Report Compiler", layout="centered")

# UPDATED CSS: High-contrast Clean Theme
st.markdown("""
    <style>
    /* Global Background: Clean White */
    .stApp { background-color: #ffffff !important; }
    
    /* Text: Dark Grey for maximum readability */
    h1, h2, h3, p, span, label { color: #1e293b !important; }
    
    /* Buttons: Professional Dark Navy, White Text */
    div.stButton > button { 
        width: 100% !important; 
        height: 55px !important; 
        font-weight: 600 !important; 
        background-color: #0f172a !important; 
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        margin: 5px 0 !important;
    }
    
    /* Inputs: Clean professional borders */
    .stTextInput > div > div > input {
        border: 2px solid #cbd5e1 !important;
        border-radius: 6px !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Dr. AIT Lab Report Compiler")
st.subheader("Select your Laboratory Subject:")

# Vertical stack of buttons for easy mobile access
if st.button("BDA (Big Data Analytics)"):
    st.session_state.manual = "BDA_Manual.pdf"
if st.button("ADBMS (Advanced DBMS)"):
    st.session_state.manual = "ADBMS_Manual.pdf"

if 'manual' not in st.session_state:
    st.session_state.manual = None

if st.session_state.manual:
    st.info(f"Selected: {st.session_state.manual.replace('_Manual.pdf', '')}")
    st.markdown("---")
    
    student_name = st.text_input("Full Student Name:")
    student_usn = st.text_input("University Seat Number (USN):")

    def create_overlay(name, usn):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # --- PAGE 1: COVER ---
        can.setFillColorRGB(1, 1, 1)
        can.rect(100, 380, 420, 50, fill=True, stroke=False) 
        can.setFillColorRGB(0, 0, 0)
        can.setFont("Times-Bold", 14)
        can.drawString(110, 395, name.upper())
        can.drawString(400, 395, usn.upper())
        can.showPage()
        
        # --- PAGE 2: CERTIFICATE ---
        can.setFillColorRGB(1, 1, 1)
        can.rect(80, 395, 480, 30, fill=True, stroke=False)
        can.setFillColorRGB(0, 0, 0)
        can.setFont("Times-Bold", 14)
        can.drawString(90, 400, name.upper())
        can.drawString(400, 400, usn.upper())
        
        can.showPage()
        can.save()
        packet.seek(0)
        return packet

    if st.button("⚡ Generate & Download PDF"):
        if student_name and student_usn and os.path.exists(st.session_state.manual):
            with st.spinner("Processing..."):
                overlay_stream = create_overlay(student_name, student_usn)
                reader = PdfReader(st.session_state.manual)
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
                
                st.success("✨ Success! Click below to download.")
                st.download_button("📥 Download Final Report", final_io, 
                                   f"{student_usn.upper()}_Report.pdf", "application/pdf")
        else:
            st.error("Please ensure you entered your Name, USN, and selected a subject.")
