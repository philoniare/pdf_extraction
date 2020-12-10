import fitz # PyMuPDF
import io
from PIL import Image
import json
from collections import Counter 

pdf_file = fitz.open("example.pdf")
def most_frequent(lst): 
    occurence_count = Counter(lst) 
    return occurence_count.most_common(1)[0][0] 

def get_line_text(line):
    text = ''
    fonts = []
    for span in line['spans']:
        text += span['text']
        if('font' in span):
            fonts.append(span['font'])
    return text, most_frequent(fonts)

doc = {}
text_ind, image_ind = 0, 0
for page_index in range(len(pdf_file)):
    # get the page itself
    page = pdf_file[page_index]
    page_dict = page.getText("dict")
    page_image_ind = 0
    for ind, block in enumerate(page_dict['blocks']):
        if(block['type'] == 1):
            # image block
            image = Image.open(io.BytesIO(block['image']))
            # save it to local disk
            filename = f"images/image{page_index+1}_{page_image_ind}.{block['ext']}"
            image.save(open(filename, "wb"))
            doc["y" + str(image_ind)] = filename
            image_ind += 1
            page_image_ind += 1
        elif(block['type'] == 0):
            # text block
            output_lines = []
            for line in block['lines']:
                output_lines.append(get_line_text(line))
            doc["x" + str(text_ind)] = output_lines
            text_ind += 1

with open('data.json', 'w') as outfile:
    json.dump(doc, outfile)