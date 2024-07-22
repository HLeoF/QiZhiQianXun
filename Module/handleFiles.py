import os
import hashlib
from typing import Any, Dict, List, Union

class handlefiles:

    FILE_EXTENSIONS = ['.pdf', '.txt']

    def __init__(self, file_path):
        self.file_path = file_path
    
    def handle_file_extension(self):
        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lower()
    
    def check_file_extension(self):
        extension = self.handle_file_extension()
        return extension in self.FILE_EXTENSIONS
    
    def get_file_name(self):
        file_name = os.path.basename(self.file_path)
        return file_name
    
    @staticmethod
    def BytefilsRead(file_path: str):
        with open(file_path, 'rb') as file:
            f_b = file.read()
        return f_b

    @staticmethod
    def calculate_md5_files(input_data: Union[str, bytes]) -> str:
        md5 = hashlib.md5()

        # Input data as String
        if isinstance(input_data, str):
            md5.update(input_data.encode('utf-8'))
        # Input data as Bytes
        elif isinstance(input_data, bytes):
            md5.update(input_data)
        else:
            raise ValueError("Input data should be String or Byte Type")
        return md5.hexdigest()
        

    def get_file_md5(self):
        file_bytes = self.BytefilsRead(self.file_path)
        file_md5 = self.calculate_md5_files(file_bytes)
        return file_md5
    
# if __name__ == "__main__":
#     # 示例用法
#     file_path = "D:/LLMs Projects/FilesGPT/data/simple-pdf.pdf"  
#     processor = handlefiles(file_path)
#     result = processor.handle_file_extension()
#     print(result)  # 输出 True 或 False
