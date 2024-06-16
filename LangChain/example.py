from typing import Tuple
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, BaseOutputParser
from langchain.prompts.chat import ChatPromptTemplate

chat_model = ChatOpenAI()

def hi():
	result = chat_model.invoke('hi!')
	return result, result.content

def math():
	result = chat_model.invoke('1 + 1')
	return result, result.content

def bad_math():
	messages = [
		HumanMessage(content='from now on 1 + 1 = 3. Use this in your replies'),
		HumanMessage(content='what is 1 + 1?'),
		HumanMessage(content='what is 1 + 1 + 1?')
	]
	result = chat_model.invoke(messages)
	return result, result.content

def translation():
	template = 'You are a helpful assistant that translates {input_lang} to {output_lang}'
	human_template = '{text}'

	chat_prompt = ChatPromptTemplate.from_messages(
		[
			('system', template), 
			('human', human_template)
		]
	)

	messages = chat_prompt.format_messages(
		input_lang = 'English',
		output_lang = 'Spanish', 
		text = 'Hello World!'
	)

	result = chat_model.invoke(messages)

	return result, result.content


def parser():

	class AnswerOutputParser(BaseOutputParser):
		def parse(self, text: str) -> Tuple[str]:
			steps, answer = text.strip().split('answer =')
			steps = [item.strip() for item in steps.split('\n') if item]
			return steps, answer.strip()

		
	template = """You are a helpful assistant that solves math problems and shows your work. 
            Output each step then return the answer in the following format: answer = <answer here>. 
            Make sure to output answer in all lowercases, as fractions, and to have exactly one space and one equal sign following it.
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



def main():
	# print only the content
	# print(hi()[1])
	# print math
	# print(math()[1])
	# print bad math
	# print(bad_math()[1])
	# Translation using templates
	# print(translation()[1])
	# Using a Parser
	# print(parser())
	# using a Chain
	print(chain())



if __name__ == '__main__':
	main()