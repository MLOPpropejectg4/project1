

import transformers
from functions import extract_text_from_pdf,summarize,rag
 




pdf_path1 = "data/Poster_DLI2024_Atou.pdf"

pdf_path2 = "data/Admission letter_2023-24_Atou Koffi Kougbanhoun.pdf"

def task():
    print("\nWhat task do you want to do?\n")
    print("Enter 1 for summarization\n")
    print("Enter 2 for Question and Answer")

    choice = int(input("your choice : "))
    try:

        if choice == 1:
            print("#"*20 ,"summarizing......... ","#"*20)
            # Extract the text from a pdf
            text = extract_text_from_pdf(pdf_path=pdf_path1)
            # summarize the  text
            text_summarize = summarize(text)
            #printting
            #print(text)
            print("\n\n\n")
            print("#"*50 ,"Summarize text", "#"*50)
            print("\n\n")

            print(text_summarize)

            print("\n \n")
        if choice == 2:

            print("Question & Answer  in context of the pdf")

            while True:


                question = input("Your question : ")

                context = extract_text_from_pdf(pdf_path2) 

                result = rag(question=question,context=context)

                print("\n")

                print(f"Question:{result['question']}\n Anwser:{result['answer']}")

                print("\n")

                status = input("You want to continue?(Y/N): ")



                status  = status.lower()

                if status == "n":
                    print("####bye!!!####")
                    break
    except ValueError:
        print("enter 1 or 2")



if __name__ == "__main__":
    task()










