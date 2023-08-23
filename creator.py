import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image as PI
from google_search import search_google
import templates
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from image_resizer import resize


data = pd.read_csv("Sample Data.csv")
doc = BaseDocTemplate(
            "Sample Ventures.pdf",
            pagesize=letter,
            rightMargin=0.8*inch, leftMargin=0.8*inch,
            topMargin=inch/2, bottomMargin=inch/2)#, showBoundary=1)



# parts of the pdf
flowables = []
index = 0

############################################################################### MAIN LOOP ####################################################################

while index<5:

    name = str(data['NAME'].iloc[index])
    location = str(data['LOCATION'].iloc[index])
    summary = str(data['NOTES/SUMMARY'].iloc[index])
    if len(summary)>1000: # limit number of characters in the summary to 1010
        summary=summary[0:1000]
    owners = str(data['FOUNDERS/TEAM'].iloc[index]).split('; ')
    quote =  None #data['Quote'].iloc[index]
    alumni_list = str(data['Alumni Name'].iloc[index]).split(", ")
    if pd.isnull(data['Alumni Name'].iloc[index]):
        alumni_list = ['Placeholder']
    
    link = str(data['Links'].iloc[index])

    # populating alumni logos list with images in file alumni logos
    alumni_logos = []
    alumni_links = {}
    for i in range(len(alumni_list)):
        alumni = alumni_list[i].split('---')[0]
        alumni_list[i] = alumni
        try:
            img = PI.open("alumni logos/%s.png"%alumni)
            alumni_logos.append("alumni logos/%s.png"%alumni)
        except:
            try:
                img = PI.open("alumni logos/%s.jpg"%alumni)
                alumni_logos.append("alumni logos/%s.jpg"%alumni)
            except:
                img = PI.open("alumni logos/Placeholder.png")
                alumni_logos.append("alumni logos/Placeholder.png")
        

        #alumni_links[alumni]=search_google(str(alumni) + " the company")
        alumni_links[alumni] = "google.com"


    # populating owner images
    owner_images = []
    for i in range(len(owners)):
        own = owners[i]
        try:
            img = PI.open("owner images/%s.png"%own)
            owner_images.append("owner images/%s.png"%own)
        except:
            try:
                img = PI.open("owner images/%s.jpg"%own)
                owner_images.append("owner images/%s.jpg"%own)
            except:
                try:
                    img = PI.open("owner images/%s.jpeg"%own)
                    owner_images.append("owner images/%s.jpeg"%own)
                except:
                    img = PI.open("owner images/Placeholder.png")
                    owner_images.append("owner images/Placeholder.png")

    # Logos must be saved locally with the company name as the file name
    try:
        img = PI.open("company logos/%s.png" % (str(name)))
        logo = "company logos/%s.png" % (str(name))
    except:
        img = PI.open("company logos/%s.jpg" % (str(name)))
        logo = "company logos/%s.jpg" % (str(name))



    #details
    details = {}
    industry = data['INDUSTRY'].iloc[index]
    size = data['SIZE'].iloc[index]
    money = data['MONEY'].iloc[index]
    affiliation = data['AFFILIATION'].iloc[index]
    timeline = data['TIMELINE'].iloc[index]
    stage = data['STAGE TO JOIN'].iloc[index]
    equity = data['EQUITY TAKEN'].iloc[index]


    test_owner_pics = ["owner images/test3.png",  "owner images/test2.jpg"]

    

    if not pd.isnull(industry):
        details['Industry'] = industry
    if not pd.isnull(size):
        details['Cohort Size'] = size
    if not pd.isnull(money):
        details['Funding'] = money
    if not pd.isnull(affiliation):
        details['Affiliation'] = affiliation
    if not pd.isnull(timeline):
        details['Duration'] = timeline
    if not pd.isnull(stage):
        details['Stage'] = stage
    if not pd.isnull(equity):
        details['Equity'] = equity
    if pd.isnull(quote):
        quote=False
    

    


    print("Building PDF...")
    if index%5 == 0 and index!=0:
        print("-----------")
    templates.template1(doc,name, location, summary, logo, flowables, details, alumni_list, alumni_links, alumni_logos, link,owner=owners, owner_images= owner_images,quote=quote, speaker=owners[0], speaker_image=test_owner_pics[0])

    index+=1



if __name__ == '__main__':
    
    doc.build(flowables)