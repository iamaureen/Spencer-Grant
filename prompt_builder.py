def build_prompt(quality, identity, ses, genre):
    
    # Base instructions
    global essay_prompt

    base_instructions = f"""Your task is to write a {quality} short essay from the perspective of a {identity} 
    undergraduate student from a {ses} background. 
    IMPORTANT: The essay should read as if written naturally by an actual student, rather than a representation of the 
    entire group the student belongs to.

"""

    # Select the appropriate prompt based on genre
    if genre == "educational":
        essay_prompt = """Read the following New York Times story: 
        https://archive.nytimes.com/opinionator.blogs.nytimes.com/2010/06/20/the-anosognosics-dilemma-1/Define anosognosia. 
        Locate specific passages that illustrate Morris' opinions. Summarize the article. 
        What is the Dunning-Kruger Effect? 
        What do Morris and Ramachandran have to say about beliefs? 
        What parallel does Morris draw between anosognosia and how we operate in the world?
        
        Your essay should:
        - Clearly define *anosognosia*.
        - Reference or paraphrase specific passages that show Morris' opinions.
        - Accurately summarize the article.
        - Explain the *Dunning–Kruger Effect*.
        - Discuss what Morris and Ramachandran say about beliefs.
        - Describe the parallel Morris draws between anosognosia and everyday thinking.
        - Reflect your worldview and perspective naturally through your analysis, tone, and word choices - without explicitly stating your identity."""

    elif genre == "personal":
        essay_prompt = """Please write about the best choice you have made. Also the worst choice you have made recently. 
Then write about how those choices directed your life. Write 250 words."""

    elif genre == "mixed":
        essay_prompt = """Please write about your dream job. How much money are you making? 
What is it that makes it your dream job? What company are you working for, 
or do you own your company? Write 250 words."""

    # Common instructions
    common_instructions = """
    Instructions:
    - Write only the essay text directly (no meta-commentary, no mention of your identity or background).
    - Use coherent, natural academic or personal tone depending on question.
    - Use examples or illustrations to make your ideas clear and specific, allowing the essay to reflect a coherent and well-developed line of thought.
    - Length: 200–300 words unless otherwise stated.
"""

    # Combine all parts
    return base_instructions + essay_prompt + common_instructions

