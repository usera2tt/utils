import os
from PyPDF2 import PdfFileMerger

def merge(files_dir: str, output_name='merge.pdf'):
    def _get_path(file):
        return os.path.join('.', files_dir, file)
        
    if not os.path.exists(files_dir):
        raise Exception('Directory not exists')

    files = list(filter(lambda s: s.endswith('.pdf') and s != output_name, 
        os.listdir(files_dir)))
    files.sort()
    print(files)
    merger = PdfFileMerger(strict=False)

    for file in files:
        merger.append(_get_path(file))
    merger.write(_get_path(output_name))
    merger.close()


if __name__ == '__main__':
    merge('merge')
