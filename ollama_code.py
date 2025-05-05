from ollama import Client
import pandas as pd


def generate_summary(article, client):
    prompt = f"""
    You are a professional news summarizer.
    Read the article below and produce a concise, three-bullet summary that captures its key facts, main events, and core takeaways.

    {article}

    Summary:
    • """

    response = client.generate(
    model="llama3",
    prompt=prompt
    )
    return response['response']
    

if __name__ == '__main__':
    client = Client()
    articles_df = pd.read_csv('articles.csv')
    articles_df['summary'] = articles_df['text'].apply(generate_summary, client)
    articles_df.to_csv('articles.csv', index=False)
    # articles_df['summary'] = articles_df['text'].apply(lambda)
    # generate_summary()
    