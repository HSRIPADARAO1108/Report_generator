import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Page configurations
st.set_page_config(
    page_title="Dr. AIT BDA Report Generator", 
    page_icon="🎓", 
    layout="centered"
)

# Professional Institutional Slate Theme Styling
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
st.markdown("Enter student details below to update credentials seamlessly using **Times New Roman (Size 14)** matching your template formatting.")

st.markdown("---")

front_template_path = "BDA FRONT PAGE1_merged.pdf"
manual_pdf_path = "BAD_Manual_merged.pdf"

# Verify repository readiness state inside the sidebar interface
st.sidebar.header("📦 System Resource Status")
resources_ready = True

if os.path.exists(front_template_path):
    st.sidebar.success("✅ Master Template PDF Loaded")
else:
    st.sidebar.error("❌ Missing: BDA FRONT PAGE1_merged.pdf")
    resources_ready = False

if os.path.exists(manual_pdf_path):
    st.sidebar.success("✅ Master Lab Manual Loaded")
else:
    st.sidebar.error("❌ Missing: BAD_Manual_merged.pdf")
    resources_ready = False

# --- STUDENT INPUT MATRIX ---
st.subheader("👤 Enter Student Credentials")
col1, col2 = st.columns(2)
student_name = col1.text_input("Full Student Name:", placeholder="e.g. CHETHAN PRASAD L")
student_usn = col2.text_input("University Seat Number (USN):", placeholder="e.g. 1DA25SCS04")

# Helper function to generate a transparent overlay containing text blocks matching Times layout
def create_overlay_pdf(name, usn):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # ------------------ PAGE 1 OVERLAY (Cover Page) ------------------
    # Completely mask the old student text line on the cover page
    can.setFillColorRGB(1, 1, 1)
    can.rect(80, 385, 450, 45, fill=True, stroke=False)
    
    # Write the newly entered credentials in Times-Bold 14
    can.setFillColorRGB(0.0, 0.0, 0.0) 
    can.setFont("Times-Bold", 14)
    display_text_p1 = f"{name.upper()}      {usn.upper()}"
    can.drawCentredString(306, 404, display_text_p1)
    
    can.showPage() # Target the certificate page next
    
    # ------------------ PAGE 2 OVERLAY (Certificate Page) ------------------
    # Expanded white mask block to fully erase "SRIPADA RAO H       1DA25SCS18"
    # Adjusted coordinates (lower down and taller) to cover all traces of the old text completely
    can.setFillColorRGB(1, 1, 1)
    can.rect(75, 400, 460, 40, fill=True, stroke=False)
    
    # Stamp only the newly entered data beautifully aligned across the line
    can.setFillColorRGB(0.0, 0.0, 0.0)
    can.setFont("Times-Bold", 14)
    
    # Places the new Name on the left, and the new USN perfectly on the right
    can.drawString(98, 412, name.upper())
    can.drawRightString(510, 412, usn.upper())
    
    can.showPage()
    can.save()
    packet.seek(0)
    return packet

# --- GENERATION PIPELINE ENGINE ---
if resources_ready:
    if student_name.strip() and student_usn.strip():
        st.markdown("---")
        
        if st.button("⚡ Compile & Generate Full Printable Report"):
            with st.spinner("Completely removing old credentials and applying new text fields..."):
                try:
                    # 1. Generate the customized Times text layers stream
                    overlay_stream = create_overlay_pdf(student_name, student_usn)
                    
                    # 2. Load structural PDF resources
                    template_reader = PdfReader(front_template_path)
                    overlay_reader = PdfReader(overlay_stream)
                    manual_reader = PdfReader(manual_pdf_path)
                    
                    pdf_writer = PdfWriter()
                    
                    # 3. Apply custom clean mask & text changes over Page 1 (Cover)
                    page1 = template_reader.pages[0]
                    page1.merge_page(overlay_reader.pages[0])
                    pdf_writer.add_page(page1)
                    
                    # 4. Apply custom clean mask & text changes over Page 2 (Certificate)
                    page2 = template_reader.pages[1]
                    page2.merge_page(overlay_reader.pages[1])
                    pdf_writer.add_page(page2)
                    
                    # 5. Append all master experiments manual pages behind them
                    for page in manual_reader.pages:
                        pdf_writer.add_page(page)
                    
                    # 6. Save the final structurally combined binary stream
                    final_pdf_io = io.BytesIO()
                    pdf_writer.write(final_pdf_io)
                    final_pdf_io.seek(0)
                    
                    st.success("✨ Report successfully compiled! Old credentials completely wiped and updated perfectly.")
                    
                    # Download trigger
                    st.download_button(
                        label="📥 Download Finished Lab Report (PDF)",
                        data=final_pdf_io,
                        file_name=f"{student_usn.upper()}_BDA_Complete_Report.pdf",
                        mime="application/pdf"
                    )
                    
                except Exception as engine_err:
                    st.error("🚨 An issue occurred during report compilation processing loops.")
                    st.exception(engine_err)
    else:
        st.info("💡 Please type in the Student Name and USN above to activate the automated compiler.")
else:
    st.error("🚨 Configuration Error: Please ensure 'BDA FRONT PAGE1_merged.pdf' and 'BAD_Manual_merged.pdf' are present in your root GitHub folder path.")
