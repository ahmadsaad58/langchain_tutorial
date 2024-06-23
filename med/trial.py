from typing import Tuple
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, BaseOutputParser
from langchain.prompts.chat import ChatPromptTemplate



import base64

def encode_image():

	IMAGE_PATH = "image_path"

	# Open the image file and encode it as a base64 string
	def encode_image(image_path):
		with open(image_path, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode("utf-8")

	base64_image = encode_image(IMAGE_PATH)


def parser():

	class AnswerOutputParser(BaseOutputParser):
		def parse(self, text: str) -> Tuple[str]:
			pass

		
	template = """You are a doctor who needs to analyze this input and summarize the patient's information in technical terms.
            """
	
	human_template = '{problem}'

	chat_prompt = ChatPromptTemplate.from_messages(
			[
				('system', template), 
				('human', human_template)
			]
		)

	messages = chat_prompt.format_messages(
		problem = "2x^2 - 5x + 3 = 0"
	)

	result = chat_model.invoke(messages)
	parsed = AnswerOutputParser().parse(result.content)
	steps, answer = parsed

	return steps, answer

def chain():
	class CommaSeparatedParser(BaseOutputParser):
		def parse(self, text: str) -> Tuple[str]:
			return text.strip().split(', ')
		
	template = """You are a helpful assistant who generates comma separated lists.
			A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
			ONLY return a comma separated list, and nothing more.
			"""

	human_template = "{text}"

	chat_prompt = ChatPromptTemplate.from_messages(
			[
				('system', template), 
				('human', human_template)
			]
		)

	chain = chat_prompt | chat_model | CommaSeparatedParser()
	result = chain.invoke({'text': 'colors'})
	return result
