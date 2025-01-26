import streamlit as st
import markdown2
import pdfkit
import tempfile
import os

# Set the path to wkhtmltopdf
wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

st.title("Markdown to PDF Editor")
markdown_text = st.text_area("Write your Markdown here:", height=300)
if markdown_text:
    st.subheader("Preview")
    html_content = markdown2.markdown(markdown_text)
    st.markdown(html_content, unsafe_allow_html=True)
if st.button("Export as PDF"):
    if markdown_text:
        try:
            html_content = markdown2.markdown(markdown_text)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
                tmp_html.write(html_content.encode("utf-8"))
                tmp_html_path = tmp_html.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf_path = tmp_pdf.name

            pdfkit.from_file(tmp_html_path, tmp_pdf_path, configuration=config)

            with open(tmp_pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="document.pdf",
                mime="application/pdf",
            )

            os.unlink(tmp_html_path)
            os.unlink(tmp_pdf_path)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some Markdown text to export.")