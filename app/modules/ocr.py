import os
from statistics import mean
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

class do_ocr:
	def __init__(self, formUrl, DOC_KEY, DOC_ENDPOINT, model='prebuilt-read'):
		self.formUrl = formUrl
		self.model = model
		self.key = DOC_KEY
		self.endpoint = DOC_ENDPOINT
	def analyze_read(self):
		document_analysis_client = DocumentAnalysisClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))
		poller = document_analysis_client.begin_analyze_document_from_url(self.model, self.formUrl)
		result = poller.result()
		dict_page = {}
		word_confidence = []
		for idx, style in enumerate(result.styles):
			print("Document contains {} content".format("handwritten" if style.is_handwritten else "no handwritten"))
		for page in result.pages:
			dict_page['page_number'] = {page.page_number}
			for word in page.words:
				word_confidence.append({word.content:word.confidence})
			dict_page['content'] = word_confidence
		return result.content, dict_page
	def preprocess_results(self):
		content, predictions = self.analyze_read()
		average_score = mean(value for dicts in predictions.get('content', []) for value in dicts.values())
		final_dict = {key:value for dicts in predictions.get('content', []) for key, value in dicts.items() if value < average_score}
		return content, average_score, final_dict