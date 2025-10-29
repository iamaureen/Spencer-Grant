def build_prompt(quality, identity, ses, genre):
    
    # Base instructions
    base_instructions = f"""You are an academic writing assistant. Your task is to write a {quality} short essay 
from the perspective of a {identity} undergraduate student from a {ses} background.

The essay should authentically reflect that student's social, cultural, and educational perspective 
through tone, vocabulary, and lived experience.

"""
    
    # Select the appropriate prompt based on genre
    if genre == "educational":
        essay_prompt = """Read the following New York Times story: 
https://archive.nytimes.com/opinionator.blogs.nytimes.com/2010/06/20/the-anosognosics-dilemma-1/
Define anosognosia. Locate specific passages that illustrate Morris' opinions.
Summarize the article. What is the Dunning-Kruger Effect? 
What do Morris and Ramachandran have to say about beliefs? 
What parallel does Morris draw between anosognosia and how we operate in the world?

Your essay should:
- Clearly define *anosognosia*.
- Reference or paraphrase specific passages that show Morris' opinions.
- Accurately summarize the article.
- Explain the *Dunning–Kruger Effect*.
- Discuss what Morris and Ramachandran say about beliefs.
- Describe the parallel Morris draws between anosognosia and everyday thinking.
- Reflect the worldview, tone, and experiences of the specified student identity."""

    elif genre == "personal":
        essay_prompt = """Please write about the best choice you have made. Also the worst choice you have made recently. 
Then write about how those choices directed your life. Write 250 words."""

    elif genre == "mixed":
        essay_prompt = """Please write about your dream job. How much money are you making? 
What is it that makes it your dream job? What company are you working for, 
or do you own your company? Write 250 words."""

    else:
        essay_prompt = f"Write a {genre} essay based on your academic experiences."
    
    # Common instructions
    common_instructions = """
    
Instructions:
- Write only the essay text (no commentary or metadata).
- Use coherent, natural academic or personal tone depending on genre.
- Length: 200–300 words unless otherwise stated.
"""
    
    # Combine all parts
    return base_instructions + essay_prompt + common_instructions

