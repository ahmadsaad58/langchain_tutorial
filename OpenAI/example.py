from openai import OpenAI

def create_poem():
  # pulls the api key from .envs files
  client = OpenAI()

  # using gpt-3.5, it answers my question to make compose a poem
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
      {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
  )

  # print said poem
  print(completion.choices[0].message)


if __name__ == "__main__":
  create_poem()
