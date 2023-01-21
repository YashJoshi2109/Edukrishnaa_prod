#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pdfminer.high_level import extract_text
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)
text=extract_text_from_pdf("C:/Users/Pranav/Desktop/EduKrishnaa/New Edukrishnaa/edukrishnaa/templates/parserfiles/PranavResume.pdf")


# In[2]:


#import docx2txt
#def extract_text_from_docx(docx_path):
 #   txt = docx2txt.process(docx_path)
 #   if txt:
 #       return txt.replace('\t', ' ')
 #   return None
#text=extract_text_from_docx("")


# In[3]:


import spacy
import en_core_web_sm


# In[4]:


nlp=spacy.load("en_core_web_sm")


# In[5]:


print(text)


# In[6]:


text = text.lower()
lines = text.split("\n")


# In[7]:


from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
from spacy.language import Language
from spacy.pipeline import EntityRuler


# In[8]:


#Education List
Education = ['BE','BCA','MCA', 'B.E', 'BS', 'B.S','C.A.','c.a.','B.Com','B. Com','M. Com', 'M.Com','M. Com .',
          'ME', 'M.E', 'M.E.', 'M.S','MCA','BTECH', 'B.TECH', 'M.TECH', 'MTECH','M TECH',
          'PHD', 'ph.d', 'Ph.D.','MBA','mba','graduate', 'post-graduate','5 year integrated masters','masters',
          'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII','ITIL','chsc','diploma','bsc','cisce','nios','diploma']
EDUCATION = (map(lambda x: x.lower(), Education))


# In[9]:


patterns = [nlp.make_doc(text) for text in EDUCATION]


# In[66]:


import pandas as pd
df = pd.read_csv("C:/Users/Pranav/Desktop/EduKrishnaa/New Edukrishnaa/edukrishnaa/templates/parserfiles/university.csv")
mylist = df['pattern'].tolist()
mylist = (map(lambda x: x.lower(), mylist))
university = [nlp.make_doc(text) for text in mylist]


# In[67]:


import pandas as pd
df = pd.read_csv("C:/Users/Pranav/Desktop/EduKrishnaa/New Edukrishnaa/edukrishnaa/templates/parserfiles/engineering colleges in India.csv") 
college_list = df['College Name'].tolist()
college_list = (map(lambda x: x.lower(), college_list))
eng_colleges = [nlp.make_doc(text) for text in college_list]


# In[12]:


import pandas as pd
df = pd.read_csv("C:/Users/Pranav/Desktop/EduKrishnaa/New Edukrishnaa/edukrishnaa/templates/parserfiles/Technology Skills.csv")
# can also index sheet by name or fetch all sheets
skills = df['pattern'].tolist()
skills = (map(lambda x: x.lower(), skills))
skills_list = [nlp.make_doc(text) for text in skills]
print(skills_list)
from spacy.matcher import PhraseMatcher
skills_matcher=PhraseMatcher(nlp.vocab)
skills_matcher.add("SKILLS",None,*skills_list)


# In[13]:


from spacy.matcher import Matcher
email_matcher=Matcher(nlp.vocab)
emails=[{"TEXT":{"REGEX":"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"}}]
email_matcher.add("EMAIL ADDRESS",[emails])
phone_matcher=Matcher(nlp.vocab)
phone_numbers=[{"TEXT":{"REGEX":"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]"}}]
phone_matcher.add("CONTACT NUMBER",[phone_numbers])


# In[ ]:





# In[14]:


# import pandas as pd
# df = pd.read_csv("C:/Users/Hp/Desktop/companies_sorted.csv") #can also index sheet by name or fetch all sheets
# company = df['pattern'].tolist()
# companies = [nlp.make_doc(text) for text in company]
# company_matcher=PhraseMatcher(nlp.vocab)
# company_matcher.add("COMPANIES",None,*companies)


# In[15]:


# import pandas as pd
# df = pd.read_csv("C:/Users/Hp/Desktop/job roles.csv")
# df["pattern"]=df["pattern"].fillna("")
# roles=df['pattern'].tolist()
# job_title = [nlp.make_doc(text) for text in roles]
# job_matcher=PhraseMatcher(nlp.vocab)
# job_matcher.add("JOB ROLES",None,*job_title)


# In[16]:


cgpa_matcher=Matcher(nlp.vocab)
cgpa=[{"TEXT":{"REGEX":"^(([0-9]{1}\s)|([0-9]{1}\.\d{0,3}\s))|[1][0]\.[0]{0,2}\s$"}}]
cgpa_matcher.add("CGPA MARKS",[cgpa])
grades_matcher=Matcher(nlp.vocab)
grades=[{"TEXT":{"REGEX":"^A-?|[OBCD][+-]?|[SN]?F|W$"}}]
grades_matcher.add("GRADE MARKS",[grades])
duration_matcher=Matcher(nlp.vocab)
duration=[{"TEXT":{"REGEX":"^(?:(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|(?:19|20)[0-9]{2})|(?:\/|-|\.|to)|(?:till|present)|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|(?:19|20)[0-9]{2}$"}}]
duration_matcher.add("DURATION",[duration])


# In[17]:


def extract_address(text):
    for ent in doc.ents:
        if ent.label_ in ['LOC','GPE']:
            return ent.text


# In[18]:


@Language.component("extract_component")
def extract_component(doc):
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add("EDUCATION",None,*patterns)
    matcher.add("COLLEGE",None,*eng_colleges)
    matcher.add("UNIVERSITY",None,*university)
    #Educational Matcher
    edu_matcher = matcher(doc)
    spe_matcher=matcher(doc)
    edu_span = [Span(doc, start, end, label=match_id) for match_id, start, end in edu_matcher]
    edu_tuple = list(set((span.text,span.label_) for span in edu_span))
    print(edu_tuple)
    print("These are the educational qualifications of the candidate")
    for i in edu_tuple:
        print(i[0])
    print("\n")
    #CGPA Matcher
#     cgpa=cgpa_matcher(doc)
#     cgpa_span = [Span(doc, start, end, label=match_id) for match_id, start, end in cgpa]
#     cgpa_tuple = list(set((span.text,span.label_) for span in cgpa_span))
#     print("The cgpa of the candidate")
#     for i in cgpa_tuple:
#         print(i[0])
#     print("\n")
    #Year Matcher
#     years=duration_matcher(doc)
#     years_span = [Span(doc, start, end, label=match_id) for match_id, start, end in years]
#     years_tuple = list(set((span.text,span.label_) for span in years_span))
    #print("The duration of candidate")
    #for i in years_tuple:
       #print(i[0])
    #print("\n")
    #Skills Matcher
    skills=skills_matcher(doc)
    span_skills=[Span(doc, start, end, label=match_id) for match_id, start, end in skills]
    skills_tuple = list(set((span.text,span.label_) for span in span_skills))
    print("The skills of the candidate")
    for i in skills_tuple:
        print(i[0])
    print("\n")
#     data_analyst_skills=['MATLAB','Python','Data Management','Data visualization','Linear Algebra and Calculus','Microsoft Excel',
# 'Data Visualization','Machine Learning','R']
#     count=0
#     for i in data_analyst_skills:
#         if i.lower() in skills_tuple:
#             count+=1
            
#     print("Following are the skills required for a data analyst")
#     print("Your profile has {} skills required for a data analyst . To know more click here".format(count))
            
    #Email Macther
    emails=email_matcher(doc)
    spans_email = [Span(doc, start, end, label=match_id) for match_id, start, end in emails]
    email_tuple = list(set((span.text,span.label_) for span in spans_email))
    print("The email of the candidate")
    for i in email_tuple:
        print(i[0])
    print("\n")
    #Phone Number Matcher
    phone_matches=phone_matcher(doc)
    spans_phone = [Span(doc, start, end, label=match_id) for match_id, start, end in phone_matches]
    phone_tuple = list(set((span.text,span.label_) for span in spans_phone))
    print("The contact number of candidate")
    for i in phone_tuple:
        print(i[0])
    print("\n")
    print('Location of Candidate',extract_address(doc).upper())
    #Companies Matcher
#     companies=company_matcher(doc)
#     roles=job_matcher(doc)
#     company_span = [Span(doc, start, end, label=match_id) for match_id, start, end in companies]
#     company_tuple = list(set((span.text,span.label_) for span in company_span))
#     print("The companies in which candidate has worked")
#     for i in company_tuple:
#         print(i[0])
#     print("\n")
    #Role Matcher
#     role_span = [Span(doc, start, end, label=match_id) for match_id, start, end in roles]
#     job_tuple = list(set((span.text,span.label_) for span in role_span ))
#     print("The job role of the candidate")
#     for i in job_tuple:
#         print(i[0])
#     print("\n")
    #doc.ents = edu_span+cgpa_span+years_span+marks_span+grades_span+spans_email+spans_phone+span_skills
    return doc


# In[19]:


nlp.add_pipe("extract_component", first=True)


# In[20]:


print(nlp.pipe_names)


# In[21]:


doc=nlp(text)
#my_tuple = list(set((e.text,e.label_) for e in doc.ents))
#print([(ent.text, ent.label_) for ent in doc.ents])


# In[ ]:



    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




