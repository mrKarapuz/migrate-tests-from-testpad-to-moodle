import json
import logging
import os
import re

from config import settings
from sdk.html_transformer import HTML2TextTransformer
from services import FileService


class Converter:

    def __init__(self, archive_path: str):
        self.archive_path = archive_path

    def _get_content(self):
        content = FileService.unzip_file(
            archive_path=self.archive_path,
            file_to_extract=settings.FILE_WITH_TEST,
        )
        return re.search(r"var\s+test\s*=\s*(\{.*});", content, re.DOTALL)

    def _create_aiken_file(self, content: str):
        output_file = os.path.splitext(os.path.basename(self.archive_path))[0] + ".txt"
        FileService.write_file(
            file_path=os.path.join(settings.BASE_DIR, output_file),
            text=content,
        )

    def convert(self) -> int:
        """
        Convert tests and return tests count
        :return:
        """
        transformer = HTML2TextTransformer()
        content = self._get_content()
        if content:
            test_dict = json.loads(content.group(1))
            questions = test_dict["Questions"]
            for question in questions:
                question_content = transformer.handle(question["Text"]).strip() + "\n"
                answers = question["AnswerTemplates"]
                index_of_correct_answer = 0
                for index, answer in enumerate(answers):
                    answer_option = transformer.handle(
                        f"{settings.QUESTION_ANSWER_HEADING[index][1]} {answer["TextWOHtml"]}",
                    ).strip()
                    question_content += answer_option + "\n"
                    if answer.get("Score") == 1.0:
                        index_of_correct_answer = index
                correct_answer = f"ANSWER: {settings.QUESTION_ANSWER_HEADING[index_of_correct_answer][0]}"
                question_content += correct_answer + "\n"
                self._create_aiken_file(question_content)
            return len(questions)
        else:
            logging.warning("No content to convert.")
