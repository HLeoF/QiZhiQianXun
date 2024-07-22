import pdfplumber

def parse_pdf(file_path):

    # declare a empty list to store the data of each parse pdf page
    chunks = [] 

    # Open PDF file By pdfminer
    with pdfplumber.open(file_path) as pdf:
        #Visit all pages for the pdf file
        for page in pdf.pages:
            #Extract current page content
            page_content = page.extract_text()
        
            #If current page exist content, processing and store data
            if page_content:
                chunk = {
                    "page_content":page_content, # page content
                    "metadata":{
                        "source":file_path, # pdf source file path
                        "page_number":page.page_number, # current page number
                        "total_pages":len(pdf.pages), # the total number of the pdf file
                        "width":page.width, # page width
                        "height":page.height, # page height
                        "rotation":page.rotation, #page rotation
                        **pdf.metadata # extract other data from the pdf file
                    }
                }

                #construct content append into the chuncks list
                chunks.append(chunk)
    
    return chunks

    
    