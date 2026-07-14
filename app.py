import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter

# Page UI properties layout configuration
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
st.markdown("Enter your student details below to instantly generate a fully compiled, personalized, print-ready laboratory manual featuring your official front coversheets.")

st.markdown("---")

front_pdf_path = "BDA_FRONT_TEMP.pdf"
manual_pdf_path = "BAD_Manual_merged.pdf"

# Verify repository readiness state inside the sidebar interface
st.sidebar.header("📦 System Resource Status")
resources_ready = True

if os.path.exists(front_pdf_path):
    st.sidebar.success("✅ Front Page PDF Loaded")
else:
    st.sidebar.error("❌ Missing: BDA_FRONT_TEMP.pdf")
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

# Core function to swap text directly inside the PDF content streams
def modify_pdf_text(input_pdf_path, old_name_1, old_name_2, old_usn, new_name, new_usn):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        # Check text contents using page streams natively
        content = page.get_contents()
        if content:
            # Safely extract binary data to replace string encodings
            data = page.get_contents().get_data()
            
            # Perform text structural switches inside the PDF code block
            if old_usn.encode('utf-8') in data:
                data = data.replace(old_usn.encode('utf-8'), new_usn.upper().encode('utf-8'))
            if old_name_1.encode('utf-8') in data:
                data = data.replace(old_name_1.encode('utf-8'), new_name.upper().encode('utf-8'))
            if old_name_2.encode('utf-8') in data:
                data = data.replace(old_name_2.encode('utf-8'), new_name.upper().encode('utf-8'))
                
            page.get_contents().set_data(data)
        writer.add_page(page)
        
    return writer

# --- GENERATION PIPELINE ENGINE ---
if resources_ready:
    if student_name.strip() and student_usn.strip():
        st.markdown("---")
        
        if st.button("⚡ Compile & Generate Full Printable Report"):
            with st.spinner("Modifying coversheets and binding master manual document streams..."):
                try:
                    # Placeholders inside original files mapping
                    target_usn = "1DA25SCS18"
                    target_name_1 = "SRIPADA RAO H"
                    target_name_2 = "H SRIPADA RAO"
                    
                    # 1. Update text metadata directly within the front PDF stream
                    pdf_writer = modify_pdf_text(
                        front_pdf_path, target_name_1, target_name_2, target_usn, student_name, student_usn
                    )
                    
                    # 2. Append the main experimental lab manual payload
                    main_manual_reader = PdfReader(manual_pdf_path)
                    for page in main_manual_reader.pages:
                        pdf_writer.add_page(page)
                    
                    # 3. Export data configurations out as a binary asset
                    final_pdf_io = io.BytesIO()
                    pdf_writer.write(final_pdf_io)
                    final_pdf_io.seek(0)
                    
                    st.success("✨ Laboratory report compiled successfully with original coversheets!")
                    
                    # 4. Instant system download utility trigger
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
    st.error("🚨 Configuration Error: Ensure both 'BDA_FRONT_TEMP.pdf' and 'BAD_Manual_merged.pdf' are pushed to your GitHub repository.")
