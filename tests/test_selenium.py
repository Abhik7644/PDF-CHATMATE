import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_pdf_chat_end_to_end():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://localhost:8501")

        wait = WebDriverWait(driver, 30)

        # 1. Wait for application
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1")
            )
        )

        # 2. Find file uploader
        file_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='file']")
            )
        )

        # 3. Upload test PDF
        pdf_path = os.path.abspath("tests/test.pdf")
        file_input.send_keys(pdf_path)

        # 4. Click Upload PDF
        upload_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Upload PDF')]")
            )
        )

        upload_button.click()

        # 5. Wait for successful upload
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(text(), 'PDF uploaded successfully')]"
                )
            )
        )

        # 6. Find chat input
        chat_input = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "textarea"
                )
            )
        )

        # 7. Ask question
        question = "What is the main topic of this document?"

        chat_input.send_keys(question)
        chat_input.send_keys(Keys.ENTER)

        # 8. Wait for assistant response
        wait.until(
            EC.presence_of_element_located(
                (
                  By.XPATH,
                  f"//*[contains(text(), '{question}')]"
                )
            )
        )

        # 9. Verify question was submitted
        wait.until(
            lambda driver: len(
                driver.find_elements(
                    By.CSS_SELECTOR,
                    '[data-testid="stChatMessage"]'
                )
            ) >= 2
        )

        #10 . get chat messages
        messages = driver.find_elements(
            By.CSS_SELECTOR,
            '[data-testid="stChatMessage"]'
        )

        assert len(messages) >=2

        assistant_message=messages[-1].text

        assert assistant_message.strip() != ""

        assert "Internal Server Error" not in assistant_message

    finally:
        driver.quit()