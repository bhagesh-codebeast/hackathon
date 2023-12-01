import os
import azure.ai.vision as sdk

class do_classification:
	def __init__(self,url,service_options,VISION_ENDPOINT,VISION_KEY,language='en'):
		self.url = url
		self.language = language
		self.service_options = sdk.VisionServiceOptions(VISION_ENDPOINT,VISION_KEY)
	def do_analysis(self):
		vision_source = sdk.VisionSource(url=self.url)
		analysis_options = sdk.ImageAnalysisOptions()
		analysis_options.features = (sdk.ImageAnalysisFeature.CAPTION |sdk.ImageAnalysisFeature.TEXT)
		analysis_options.language = self.language
		analysis_options.gender_neutral_caption = True
		image_analyzer = sdk.ImageAnalyzer(self.service_options, vision_source, analysis_options)
		result = image_analyzer.analyze()
		return result
	def do_preprocessing(self):
		result = self.do_analysis()
		data_dict = {}
		line_dict = {}
		if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
			if result.caption is not None:
				data_dict['Caption'] = {result.caption.content:result.caption.confidence}
			if result.text is not None:
				for line in result.text.lines:
					for word in line.words:
						line_dict[line.content] = {word.content:word.confidence}
			complete_sentence = ' '.join(key for key, _ in line_dict.items())
			return data_dict, line_dict, complete_sentence
		else:
			error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
			print(" Analysis failed.")
			print("   Error reason: {}".format(error_details.reason))
			print("   Error code: {}".format(error_details.error_code))
			print("   Error message: {}".format(error_details.message))
			return error_details, _, _