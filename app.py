import streamlit as st
import os
import io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="Dr. AIT Lab Report Compiler",
    page_icon="🎓",
    layout="centered"
)

# -------------------- Enhanced CSS --------------------
st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(180deg,#0f172a,#1e293b);
}

/* Main Container */
.block-container{
    max-width:700px;
    padding-top:2rem;
    padding-bottom:2rem;
    padding-left:5%;
    padding-right:5%;
}

/* Headings */
h1{
    color:#ffffff !important;
    text-align:center;
    font-size:2.2rem !important;
    font-weight:700;
}

h2,h3{
    color:#ffffff !important;
}

p,label,span{
    color:#e2e8f0 !important;
}

/* Info Box */
div[data-testid="stAlert"]{
    border-radius:12px;
}

/* Text Inputs */
.stTextInput input{
    background:#ffffff !important;
    color:#000000 !important;
    border:2px solid #38bdf8 !important;
    border-radius:10px !important;
    padding:12px !important;
    font-size:16px !important;
}

/* Input Labels */
label{
    font-weight:600 !important;
    font-size:15px !important;
}

/* Buttons */
div.stButton > button{
    width:100%;
    height:55px;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:12px;
    font-size:16px;
    font-weight:bold;
    transition:0.3s;
}

div.stButton > button:hover{
    background:#1d4ed8;
    transform:translateY(-2px);
}

div.stButton > button:focus{
    border:none;
    box-shadow:0 0 10px rgba(59,130,246,.5);
}

/* Download Button */
div.stDownloadButton > button{
    width:100%;
    height:55px;
    background:#16a34a;
    color:white;
    border:none;
    border-radius:12px;
    font-size:16px;
    font-weight:bold;
}

div.stDownloadButton > button:hover{
    background:#15803d;
}

/* Horizontal Line */
hr{
    border:1px solid #334155;
}

/* Mobile Responsive */
@media screen and (max-width:768px){

    .block-container{
        padding-left:15px;
        padding-right:15px;
        padding-top:20px;
    }

    h1{
        font-size:1.7rem !important;
        line-height:1.3;
    }

    h2{
        font-size:1.3rem !important;
    }

    h3{
        font-size:1.1rem !important;
    }

    .stTextInput input{
        font-size:18px !important;
        height:52px;
    }

    div.stButton > button{
        height:52px;
        font-size:17px;
    }

    div.stDownloadButton > button{
        height:52px;
        font-size:17px;
    }
}

/* Extra Small Phones */
@media screen and (max-width:480px){

    h1{
        font-size:1.45rem !important;
    }

    .stTextInput input{
        font-size:17px !important;
    }

    div.stButton > button{
        font-size:16px;
    }
}

</style>
""", unsafe_allow_html=True)

st.title("🎓 Dr. AIT Lab Report Compiler")

# 1. Subject Selection via Buttons
st.subheader("Select your Laboratory Subject:")
col_a, col_b = st.columns(2)
if col_a.button("BDA (Big Data Analytics)"):
    st.session_state.manual = "BDA_Manual.pdf"
if col_b.button("ADBMS (Advanced DBMS)"):
    st.session_state.manual = "ADBMS_Manual.pdf"

# Initialize manual path in session state
if 'manual' not in st.session_state:
    st.session_state.manual = None

if st.session_state.manual:
    st.info(f"Selected: {st.session_state.manual.replace('_Manual.pdf', '')}")

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

                st.success("✨ Report Compiled Successfully!")
                st.download_button(
                    "📥 Download Final Report",
                    final_io,
                    f"{student_usn.upper()}_Report.pdf",
                    "application/pdf"
                )
        else:
            st.error(f"Error: Make sure {st.session_state.manual} is uploaded and fields are filled.")
