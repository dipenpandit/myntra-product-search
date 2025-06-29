from openai import OpenAI
import re
import os
import json
import pandas as pd
import joblib


DATA_PATH = "src/data/myntra_products_with_embeddings.joblib"
df = joblib.load(DATA_PATH)


def get_response(messages):
    client = OpenAI(
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key =  os.getenv("GEMINI_API_KEY")
    )
    response = client.chat.completions.create(
      model = "gemini-2.0-flash",
      temperature = 0.7,
      messages = messages,
      max_completion_tokens=150,
    )
    content = response.choices[0].message.content
    # remove ```json and ``` markers
    json_str = re.sub(r'```json|```', '', content).strip()
    return json_str



def get_filters(user_query, df=df, get_response=get_response):
    brand_list = df["ProductBrand"].drop_duplicates().tolist()
    color_list = df["PrimaryColor"].drop_duplicates().tolist()
    gender_list = df["Gender"].drop_duplicates().tolist()
    
    system_message = {
      "role": "system",
      "content": f"""You are a clothing search assistant designed to extract the filters, product_brand, color, gender, and price
      from the user's query in JSON format. No other text or explaination.
      Available product_brands: {brand_list}
      Available colors: {color_list}
      Available genders: {gender_list}
      price can be anything from 0 to 100k
      based on user's search query. give me json output as follows
      {{
      'color': "if user did not explicitly mentioned the color in query or if the color mentioned by user is not present in above color list, give Not-Mentioned.",
      'brand': "brand should be explicitly from the above list. if not specified or not present in the above list, give Not-Mentioned."
      'gender': "gender should be from above list only. if not specified give Not-Mentioned."
      'max_price': "float32 if mentioned else null."
      'min_price': "float32 if mentioned else null."
      }}
      """
    }

    user_message = {
      "role": "user",
      "content": user_query
    }

    # Call the get_response function
    llm_response = get_response(
    messages=[system_message, user_message]
    )
    return json.loads(llm_response)
