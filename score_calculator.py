
def corrector(typed_text, generated_text):
    """function to see if typed sentence is same as generated
    sentence"""
    generated_text = generated_text.split(' ')
    typed_text_splitted = typed_text.split(' ')
    typed_text_cleaned_list = []
    #cleaning the splitted list to elimate the space lagging behind
    for element in typed_text_splitted:
        element = element.rstrip()
        typed_text_cleaned_list.append(element)

    print(generated_text)
    print(typed_text_cleaned_list)
    if len(generated_text) != len(typed_text_cleaned_list):
        return False
    i = 0 
    while i <  len(typed_text_cleaned_list):
        if generated_text[i]!= typed_text_cleaned_list[i]:
            return False
        i+=1
    return True 

def score_calculator(typed_text,time_in_seconds):
    """calculate the score base of sentence's length and time taken to write it"""
    score = len(typed_text)//time_in_seconds
    return score
    
