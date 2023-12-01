import streamlit as st
import pandas as pd
import numpy as np
import tempfile
import time


# from modules import ocr, noocr, classify

st.title('Team Robocop')

col1, col2 = st.columns([1,1])

col1.markdown("## Input")
input_data = col1.file_uploader("Upload file")

image = ''
video_bytes = ''
if input_data:
	if input_data.name.endswith('.png'):
		image = input_data
	else:
		tfile = tempfile.NamedTemporaryFile(delete=True)
		tfile.write(input_data.read())
		video_file = open(tfile.name, 'rb')
		video_bytes = video_file.read()

col1.divider()
task = col1.selectbox(
	'Select the task to perform',
	('OCR', 'Advanced-OCR', 'Object-Detection')
	)
start = col1.button('START')


col2.markdown("## Prediction")
if start:
	if image:
		if task == 'OCR':
			with st.status("Running Advanced-OCR", expanded=True) as status:
				st.write("Identifying Bounding Boxes...")
				time.sleep(2)
				st.write("Splitting Bounding Boxes...")
				time.sleep(1)
				st.write("Predicting Words...")
				time.sleep(1)
				st.write("Correcting Output...")
				time.sleep(1)
				status.update(label="OCR Complete", state="complete", expanded=False)
		elif task == 'Advanced-OCR':
			with st.status("Running Advanced-OCR", expanded=True) as status:
				st.write("Identifying Bounding Boxes...")
				time.sleep(2)
				st.write("Splitting Bounding Boxes...")
				time.sleep(1)
				st.write("Predicting Words...")
				time.sleep(1)
				st.write("Correcting Output...")
				time.sleep(1)
				status.update(label="Advanced-OCR Complete", state="complete", expanded=False)
		elif task == 'Object-Detection':
			with st.status("Object-Detection", expanded=True) as status:
				st.write("Identifying Bounding Boxes...")
				time.sleep(2)
				st.write("Splitting Bounding Boxes...")
				time.sleep(1)
				st.write("Predicting Words...")
				time.sleep(1)
				st.write("Correcting Output...")
				time.sleep(1)
				status.update(label="Object-Detection Complete", state="complete", expanded=False)
		

		col2.image(image)
		
		message = col2.chat_message("ai")
		message.write(task)		
		st.success('Prediction Complete!', icon="✅")

	elif video_file:
		col2.video(video_bytes)
		message = col2.chat_message("ai")
		message.write(task)		
		st.success('Prediction Complete!', icon="✅")
	else:
		col2.warning('Input not found!', icon="⚠️")