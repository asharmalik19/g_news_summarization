from google import genai
import os
import sqlite3
import pandas as pd

def generate_summary(article, client):
    prompt = f"""
    You are a professional news summarizer.
    Read the article below and produce a concise, three-bullet summary that captures its key facts, main events, and core takeaways.

    {article}

    Summary:
    • """

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", 
        contents=prompt
    )
    return response.text
    
if __name__ == '__main__':
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

#     article = """
# 'Finding an affordable smartphone with good performance can be tricky. Mobile prices keep going up. However, in 2025, several brands offer impressive phones for less than PKR 40,000. These phones do not sacrifice quality.\n\nBrands like Tecno, Vivo, Infinix, Redmi, and Realme are providing great options. They offer a balance of features and price. This means you can get a fantastic mobile experience without spending a lot of money.\n\nHere are some of the best smartphones you can buy in Pakistan right now under PKR 40,000. Each phone offers different strengths, catering to various needs. Whether you love photography, gaming, or just need a reliable daily phone, there is a choice for you.\n\nFor example, the Tecno Spark 30 Pro costs PKR 37,999. It features a 108 MP AI camera, 256GB storage, and 8GB RAM. This makes it perfect for people who enjoy taking pictures and running many apps at once.\n\nAnother great option is the Vivo Y19s, priced at PKR 35,900. It boasts a 50MP camera, a large 6.68-inch LCD screen, and a strong 5500mAh battery. Its smooth 90Hz display is ideal for stylish users who use their phone a lot.\n\nIf you are a gamer or enjoy streaming videos, consider the Infinix Hot 50 for PKR 36,499. It comes with an AMOLED display, a 50MP camera, 8GB RAM, and a 5000mAh battery. This combination provides a great experience for entertainment.'"""
#     summary = generate_summary(article, client)
#     print(summary)

    with sqlite3.connect('articles_data.db') as con:
        cur = con.cursor()
        df = pd.read_sql_query("SELECT * FROM article", con).iloc[:2]
        df['summary'] = df['text'].apply(generate_summary, client=client)
        print(df['summary'])
        # df.to_sql('article', con, if_exists='replace')

        
    