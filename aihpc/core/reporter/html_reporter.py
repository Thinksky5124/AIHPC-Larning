'''
Author       : Thinksky5124
Date         : 2024-04-06 16:24:05
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 18:34:35
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/reporter/html_reporter.py
'''
import os
from typing import Any

from .base_reporter import BaseReporter
from ..utils import ObjectRegister

@ObjectRegister.register('reporter')
class HtmlReporter(BaseReporter):
    def __init__(self, save_path: str) -> None:
        super().__init__(save_path)
        self.html_body = ''

    def __call__(self, x_name: str, x_val: Any, y_name: str, message: str) -> None:
        self.html_body += f"<image src=\"{message}.png\"/>\n"

    def save(self, save_path: str = None) -> None:
        if save_path is None:
            save_path = self.save_path
        if save_path:
            html = open(os.path.join(save_path, "results.html"), "w")
            html.write("<html><body>\n")
            html.write(self.html_body)
        if save_path:
            html.write("</body></html>\n")
    
    def clear(self) -> None:
        self.html_body = ''