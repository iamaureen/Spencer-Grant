def build_prompt(quality, identity, ses, genre):
    
    # Base instructions
    base_instructions = f"""You are an academic writing assistant. Your task is to write a {quality} short essay 
from the perspective of a {identity} undergraduate student from a {ses} background.

IMPORTANT: Write the essay directly. Do NOT start with phrases like "As a [identity] student..." or 
mention your background explicitly. Instead, authentically reflect that student's social, cultural, 
and educational perspective through:
- Natural tone and voice
- Vocabulary choices appropriate to their background
- Lived experiences woven into the content
- Perspective evident in your analysis and examples

The essay should read as if written naturally by this student, not as a description of their identity.

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
- Reflect your worldview and perspective naturally through your analysis, tone, and word choices - without explicitly stating your identity."""

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
- Write only the essay text directly (no meta-commentary, no mention of your identity or background).
- Start the essay naturally - do not begin with "As a..." or similar phrases.
- Use coherent, natural academic or personal tone depending on genre.
- Let your perspective and experiences emerge naturally through your writing style and examples.
- Length: 200–300 words unless otherwise stated.
"""
    
    # Combine all parts
    return base_instructions + essay_prompt + common_instructions

