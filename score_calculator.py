
def corrector(typed_text, generated_text):
    """function to see if typed sentence is same as generated
    sentence"""
    generated_text = generated_text.split(' ')
    typed_text_splitted = typed_text.split(' ')
    typed_text_cleaned_list = []
    mistaken_text = []
    #cleaning the splitted list to elimate the space lagging behind
    for element in typed_text_splitted:
        element = element.rstrip()
        typed_text_cleaned_list.append(element)
        
    # if len(generated_text) != len(typed_text_cleaned_list):
    #     return False
    longest_list = generated_text if len(generated_text) > len(typed_text_cleaned_list) else typed_text_cleaned_list
    i = 0 
    while i <  len(longest_list):
        try:
            if generated_text[i]!= typed_text_cleaned_list[i]:
                mistaken_text.append(generated_text[i])
            i+=1
        except IndexError:
            while i < len(longest_list):
                mistaken_text.append(longest_list[i])
                i+=1
    if len(mistaken_text) > 1:
        return [False, mistaken_text]
    
    return [True, mistaken_text] 

def score_calculator(generated_text, corrector_return ,time_in_seconds):
    """calculate the score base of sentence's length and time taken to write it"""
    if corrector_return[0] == False:
        score = len(generated_text)-len(corrector_return[1]) // 0.8
        # in case we typed more than we supposed to, we just give them 30
        if score < 0:
            score = 30
        return score
    return len(generated_text) //0.8
