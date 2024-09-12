from llama_index.llms.groq import Groq
def if_zero(order_val):
    GROQ_API_KEY = "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"
    llm = Groq(model="llama3-8b-8192", api_key=GROQ_API_KEY)
    response = llm.complete("Determine if the following order value retrieved from a pdf document of a company award/order type is zero or not. Strictly answer in a yes or no format , and nothing else. Your answer should be entirely one word, being either yes or no . The order value is as follows : \n"  + order_val)
    return response

#print(if_zero(" 0 Crore"))