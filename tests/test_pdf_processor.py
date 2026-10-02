from backend.pdf_processor import extract_text_from_pdf


def test_extract_text_from_pdf():

    pdf_path = "tests/test.pdf"

    text = extract_text_from_pdf(pdf_path)

    assert isinstance(text, str)
    assert len(text) > 0