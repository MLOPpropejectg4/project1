
import PyPDF2 # type: ignore
from transformers import pipeline ,AutoTokenizer, AutoModelForSeq2SeqLM
import requests
def extract_text_from_pdf(pdf_path):
    
    with open(pdf_path, 'rb') as file:

        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        # Loop through each page and extract the text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return text
    
# model 
summarizer = pipeline(task="summarization",model="Falconsai/text_summarization")
# function to do the summarization
def summarize(text,model = summarizer,max_length = 100,min_length= 10,do_sample = False):
      '''
      parms: text :str -> text to summarize
            max_length : int -> maximum length wanted for the ouput 
            min_length : int -> minimum length wanted for the ouput 
            do_sample : bool -> state if the ouput has to be sample or the one with high proba

      return : text : str -> summarized text

    '''
      return model(text,max_length = 200,min_length = 100,do_sample = False)[0]["summary_text"]






# Assuming you have your text2 and sum variables defined as in the previous code

# Load a RAG model and tokenizer
model_name = "google/flan-t5-base"  # Or any other RAG model you prefer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Define a function for RAG
def rag(question, context):
  """
  Performs retrieval augmented generation (RAG) using a question and a context.

  Args:
    question: The question to be answered.
    context: The context containing relevant information.

  Returns:
    The generated answer based on the question and context.
  """

  prompt = f"Question: {question}\nContext: {context}\nAnswer:"
  inputs = tokenizer(prompt, return_tensors="pt")
  outputs = model.generate(**inputs)
  answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
  return {"question":question,"answer":answer}



#function to get an article
def get_article(url = ""):
      # Specify the URL of the article
      # url = 'https://www.dissentmagazine.org/online_articles/the-omnivorous-james-c-scott/'

    # Send a GET request to fetch the content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the article as text
        article_text = response.text
        print(article_text)  # Or process the text as needed
    else:
        print(f"Failed to retrieve the article. Status code: {response.status_code}")
    




if __name__ == "__main__":
    pipeline 
    # AutoTokenizer
    # AutoModelForSeq2SeqLM
    # text = extract_text_from_pdf(pdf_path="data/Poster_DLI2024_Atou.pdf")
    # sum = summarize(text)
    # rag()
    # print(sum) 