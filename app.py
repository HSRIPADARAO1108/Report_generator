import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Dr. AIT Report Generator", layout="centered")

# UPDATED CSS: High-contrast, clean, and cool UI
st.markdown("""
    <style>
    /* Clean white background */
    .stApp { background-color: #f8fafc !important; }
    
    /* Elegant typography */
    h1, h2, h3, p, span, label { color: #1e293b !important; font-family: sans-serif; }
    
    /* Professional buttons: Clean dark slate with white text */
    div.stButton > button { 
        width: 100% !important; 
        height: 55px !important; 
        font-weight: 600 !important; 
        background-color: #334155 !important; 
        color: #f8fafc !important;
        border-radius: 12px !important;
        border: none !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease;
    }
    
    /* Button hover effect */
    div.stButton > button:hover { background-color: #0f172a !important; }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border: 2px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Success/Info box coloring */
    .stAlert { border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Dr. AIT Lab Report Compiler")
st.subheader("Select your Laboratory Subject:")

# Subject Selection
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
        can.setFillColorRGB(0, 0, 0)
        can.setFont("Times-Bold", 14)
        
        # Cover Page
        can.drawString(110, 395, name.upper())
        can.drawString(400, 395, usn.upper())
        can.showPage()
        
        # Certificate Page
        can.drawString(90, 400, name.upper())
        can.drawString(400, 400, usn.upper())
        can.showPage()
        
        can.save()
        packet.seek(0)
        return packet

    if st.button("⚡ Generate & Download PDF"):
        if student_name and student_usn and os.path.exists(st.session_state.manual):
            with st.spinner("Compiling your report..."):
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
                
                st.success("✨ Ready to download!")
                st.download_button("📥 Download Final Report", final_io, 
                                   f"{student_usn.upper()}_Report.pdf", "application/pdf")
        else:
            st.error("Please fill in your Name and USN.")
