import fitz
from django.conf import settings
import os
import re

def extractOptions(text):
	first_option = ""
	second_option = ""
	third_option = ""
	fourth_option = ""
	result = []
	num_flag = False
	txt = ""
	p = 0

	special_case = False

	if text.find("1.") < 0 and text.find("2.") and text.find("3."):
		if text.find("(a)") >=0 and text.find("(b)") >= 0 and text.find("(c)") >= 0:
			text = text.replace("(a)",'1.')
			text = text.replace("(b)",'2.')
			text = text.replace("(c)",'3.')
			text = text.replace("(d)",'4.')
			special_case = True

	for t in text.split("\n"):
		if p > 0:
			txt = txt + t + "\n"
		p += 1

	text = txt

	if text.find("4.") >= 0:
		pos = text.find("4.")
		till = text.find("(a)")
		fourth_option= text[pos:till]
		num_flag = True
	
	if text.find("3.") >= 0:
		pos = text.find("3.")
		if text.find("4.") >= 0:
			till = text.find("4.")
		else:
			till = text.find("(a)")
		third_option= text[pos:till]
		num_flag = True
	
	if text.find("2.") >= 0:
		pos = text.find("2.")
		if text.find("3.") >= 0:
			till = text.find("3.")
		else:
			till = text.find("(a)")
		second_option= text[pos:till]
		num_flag = True
	
	if text.find("1.") >= 0:
		pos = text.find("1.")
		if text.find("2.") >= 0:
			till = text.find("2.")
		else:
			till = text.find("(a)")
		first_option= text[pos:till]
		num_flag = True
	
	
	pos = 0
	if not special_case:
		till = min(text.find("(a)"),text.find("1."))
	else:
		till = text.find("1.")
	main_option = text[pos:till]
	
	main_option = str(main_option.replace('\n',' ').replace('www.visionias.in','').replace('©Vision IAS','')).strip()
	#main_option = re.sub("\d*\.*        \d*\.",'',main_option)
	if main_option[0].isdigit():
		dot_pos = main_option.find(".")
		if dot_pos >= 0:
			main_option = main_option[dot_pos + 1:]
	result.append(main_option)
	result.append(first_option.replace('\n',' '))
	result.append(second_option.replace('\n',' '))
	result.append(third_option.replace('\n',' '))
	result.append(fourth_option.replace('\n',' '))
	return result

def extractAnswers(text):
	result = []
	a_Text = ""
	b_Text = ""
	c_Text = ""
	d_Text = ""

	a_pos = text.find("(a)")
	b_pos = text.find("(b)")
	c_pos = text.find("(c)")
	d_pos = text.find("(d)")


	a_Text = text[a_pos:b_pos]
	b_Text = text[b_pos:c_pos]
	c_Text = text[c_pos:d_pos]
	d_Text = text[d_pos:]

	result.append(a_Text)
	result.append(b_Text)
	result.append(c_Text)
	result.append(d_Text)

	return result


def extractQandA(textList):
	q_counter = 1
	commn_txt = 'DO NOT OPEN THIS BOOKLET UNTIL YOU ARE ASKED TO DO SO'
	commn_txt2 = "1."
	result = []
	for q in textList:
		if q_counter == 1:
			pos_start = q.find(commn_txt)
			new_text = q[pos_start + len(commn_txt) + 1:]
			sec_pos = new_text.find(commn_txt2)
			if sec_pos >= 0:
				new_text2 = new_text[sec_pos:]
			result.append(new_text2)
		else:
			result.append(q)
		q_counter += 1
	return result

def extractText(text):
	i = 0
	q = []
	ques = ""

	for line in text.split("\n"):
		if line.startswith("(d)"):
			ques = ques + line
			q.append(ques)
			ques = ""
		else:
			ques = ques + line + "\n"
	return q



def handle_uploaded_file(file):
    path_to_file = os.path.join(str(settings.MEDIA_ROOT),'files',str(file).replace(' ','_'))
    doc = fitz.open(path_to_file)
    number_of_pages = doc.page_count
    # ctx['page_count'] = number_of_pages
    
    # ctx['file_name'] = str(file)
    
    page_text_list = []
    image_details = []
    font_details = set()
    tot_images = 0

    page_string = ''
    for pageIndx in range(0,number_of_pages):
        
        # Page Details
        txt = doc.get_page_text(pageIndx)
        # page_text_list.append(txt)
        page_string += txt + '\n\n'
    return page_string


def get_q_and_a(file):
    contents = handle_uploaded_file(file)
    #print(contents)
    q = extractText(contents)
    result = extractQandA(q)
    # print(result[0])

    all_options = []
    all_answers = []
    for QA in result:
        options = extractOptions(QA)
        all_options.append(options)
        answers = extractAnswers(QA)
        all_answers.append(answers)
    
    return all_options, all_answers


def read_answers(text):
	answers = []
	for line in text.split("\n"):
		if line.startswith("Q") and line.find(" ") > 0 and line.find(".") > 0:
			answers.append(line.strip())
		
	return answers

def read_ans_from_file(file):
	page_string = handle_uploaded_file(file)
	
	answers = read_answers(page_string)

	return answers