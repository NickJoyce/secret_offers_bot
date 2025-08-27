from openai import OpenAI
from settings import GPT_API_KEY
from openai import AsyncOpenAI

client = OpenAI(api_key=GPT_API_KEY)

async_client = AsyncOpenAI(api_key=GPT_API_KEY)

































# response = client.responses.create(
#     model="gpt-4.1-nano",
#     instructions=None,
#     input="Сгенерируй рандомный пример json",
#     temperature=0.2,
#     max_output_tokens=None,
#     top_p=None
# )

# print(response.output_text)


# response = await client.responses.create(
#     model="gpt-4o", input="Explain disestablishmentarianism to a smart five year old."
# )
# print(response.output_text)



