import re
import json
import zipfile

from html2text import HTML2Text
from typing import Final


class HTML2TextTransformer(HTML2Text):
    """
    Ignore links, images, formatting and line breaks
    """
    def __init__(self):
        super().__init__()
        self.ignore_links = True  # Ignore links
        self.ignore_images = True  # Ignore images
        self.ignore_emphasis = False  # Ignore formatting
        self.body_width = 0  # Ignore <br>


class FileService:
    """
    Service for working with files
    """
    @staticmethod
    def unzip_file(
            archive_path: str,
            file_to_extract: str
    ) -> str:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            if file_to_extract in zip_ref.namelist():
                with zip_ref.open(file_to_extract) as file:
                    return file.read().decode('utf-8')
            else:
                print(f"Файл {file_to_extract} не найден в архиве.")



QUESTION_ANSWER_HEADING: Final = (
    ("A", "A) "),
    ("B", "B) "),
    ("C", "C) "),
    ("D", "D) "),
    ("E", "E) "),
)


content = FileService.unzip_file('Екзамен 4л хірургія 2022.zip',  'test.js')
converter = HTML2TextTransformer()
test_content = re.search(r'var\s+test\s*=\s*(\{.*\});', content, re.DOTALL)

if test_content:
    test_dict = json.loads(test_content.group(1))
    questions = test_dict['Questions']
    for question in questions:
        question_text = converter.handle(question['Text'])
        print(question_text)
        answers = question['AnswerTemplates']
        index_of_correct_answer = 0
        for index, answer in enumerate(answers):
            print(f"{QUESTION_ANSWER_HEADING[index][1]}{answer["TextWOHtml"]}")
            if answer.get('Score') == 1.0:
                index_of_correct_answer = index
        print(f"ANSWER: {QUESTION_ANSWER_HEADING[index_of_correct_answer][0]}")
else:
    print("Переменная test не найдена в файле.")
