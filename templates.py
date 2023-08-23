from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from image_resizer import resize
from reportlab.lib.units import inch

def template1(doc,name_text, location_text, summary_text, logo_path, flow_list, details, alumni, alumni_links,alumni_logos,link,owner=[], owner_images=[],quote=False,speaker=False,speaker_image=False):

    # defining the frames
    frames = []
    top_frame = Frame(0.8*inch,doc.height/1.15, doc.width, doc.height/5)#, showBoundary=1)
    left_frame = Frame(0.8*inch, 1.5*inch, doc.width/2.15, doc.height/1.15-inch)#, showBoundary=1)
    top_right_frame = Frame(doc.width/2.15+0.8*inch, doc.height/2+inch/2, (doc.width+0.8*inch)-(doc.width/2.15+0.8*inch), doc.height/1.15-doc.height/2)#, showBoundary=1)
    bottom_right_frame = Frame(doc.width/2.15+0.8*inch, inch, (doc.width+0.8*inch)-(doc.width/2.15+0.8*inch), doc.height/2-inch/2)#, showBoundary=1)
    bottom_frame = Frame(0.8*inch, inch/2,doc.width,inch)

    top_dimensions = ((doc.width+0.8*inch)-(doc.width/2.15+0.8*inch)-50, doc.height/1.15-doc.height/2-50)
    bottom_dimensions = ((doc.width+0.8*inch)-(doc.width/2.15+0.8*inch)-50, doc.height/2-inch/2-50)

    
    owner_images = resize(owner_images, top_dimensions)
    alumni_logos = resize(alumni_logos, bottom_dimensions)

    frames.append(top_frame)
    frames.append(left_frame)
    frames.append(top_right_frame)
    frames.append(bottom_right_frame)
    frames.append(bottom_frame)

    doc.addPageTemplates([PageTemplate(id='framess', frames=frames)])
    
    styles = getSampleStyleSheet() 
    name_style = ParagraphStyle('namestyle',parent=styles['Heading1'], fontSize = 24, leading=28,fontName="Times-Roman")
    location_style = ParagraphStyle('locationstyle', parent=styles['Heading2'], fontSize=16, leading=19,fontName="Times-Roman")
    summary_style = ParagraphStyle('summarystyle', parent=styles['Normal'], fontSize=12, leading=15,fontName="Times-Roman")
    program_details_header_style = ParagraphStyle('programdetailsheader',parent=styles['Heading2'], textColor = 'black',fontName="Times-Roman", fontSize=16, borderPadding = (7,1,20), alignment=1)
    program_details_style = ParagraphStyle('programdetails', parent=styles['Normal'],fontName="Times-Roman", fontSize=12, leading=15)
    owner_style = ParagraphStyle('ownerstyle',parent=styles['Heading2'], fontSize=12, leading=15, alignment=1,fontName="Times-Roman")
    table_style = TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')])
    bottom_table_style = TableStyle([('VALIGN',(0,0),(-1,-1),'BOTTOM')])
    link_style = ParagraphStyle('linkstyle', parent=owner_style, textColor='blue')
    quote_style = ParagraphStyle('quotestyle', parent=summary_style,fontSize=20, leading=24)
    more_info_style = ParagraphStyle('programdetails', parent=styles['Normal'],fontName="Times-Roman", fontSize=12, leading=15)
    
    # TOP FRAME
    name_flowable = Paragraph("<b>" + name_text+"</b>", style=name_style)
    location_flowable = Paragraph(location_text, style=location_style)

    # LEFT FRAME
    summary_flowable = Paragraph(summary_text, style=summary_style)
    program_details_header_flowable = Paragraph("<u>Program Details</u>", style=program_details_header_style)
    program_details_list_flowable = ListFlowable([Paragraph("<b>"+k+":</b> " + v, program_details_style) for k,v in details.items()], bulletType='bullet')

    # TOP RIGHT FRAME
    top_right_frame_table = []

    if quote:
        quote_and_speaker_flowable = Paragraph("<b><font color='#5A5A5A'>\"" +str(quote) + "\"</font><br/><br/> <font size=16>"+ str(speaker)+"</font></b>", style=quote_style)
        speaker_image_flowable = resize([speaker_image],(top_dimensions[0]/2,top_dimensions[1]))
        top_right_frame_table.append(TopPadder(Table([[quote_and_speaker_flowable,speaker_image_flowable]], style=table_style)))

    else:
        temp = []
        temp_names = []
        images_in_a_row = 3
        for i in range(len(owner)): # putting images into arrays of length 3 and creating a table object for each
            owner_flowable = Paragraph(owner[i], style=owner_style)

            temp.append(owner_images[i])
            temp_names.append(owner_flowable)

            i=i+1
            if i%images_in_a_row ==0 and i!=0:
  
                top_right_frame_table.append(Table([temp], style=table_style))
                top_right_frame_table.append(Table([temp_names], style=table_style))
                temp=[]
                temp_names = []
            
            elif i == len(owner_images):
                top_right_frame_table.append(Table([temp], style=table_style))
                top_right_frame_table.append(Table([temp_names], style=table_style))
    
    # BOTTOM RIGHT FRAME
    highlighted_alumni_header_flowable = Paragraph("<u>Highlighted Alumni</u>", style=program_details_header_style)

    bottom_right_frame_table = []
    temp = []
    temp_names = []
    images_in_a_row = 3
    for i in range(len(alumni_logos)): # putting images into arrays of length 3 and creating a table object for each
        #alumn_li = alumni_links[alumni[i]]
        #alumni_flowable = Paragraph("<link href = %s><u>"%alumn_li + str(alumni[i]) + "</u></link>", style=link_style)

        temp.append(alumni_logos[i])
        #temp_names.append(alumni_flowable)

        i=i+1
        if i%images_in_a_row ==0 and i!=0:
            bottom_right_frame_table.append(Table([temp], style=bottom_table_style))
            #bottom_right_frame_table.append(Table([temp_names], style=table_style))
            temp=[]
            #temp_names = []
        
        elif i == len(alumni_logos):
            bottom_right_frame_table.append(Table([temp], style=bottom_table_style))
            #bottom_right_frame_table.append(Table([temp_names], style=table_style))

    # BOTTOM FRAME
    link_flowable = Paragraph("<link href = %s><u>"%link + str(link) + "</u></link>", style=link_style)
    more_info_flowable = ListFlowable([Paragraph("<b>Application Info:</b> ", more_info_style), 
                                       Paragraph("<b>Website: </b><a href = %s color='blue'><u>"%link + str(link) + "</u></a>", more_info_style),
                                       Paragraph("<b>Contact:</b> ", more_info_style)], bulletType='bullet')
                                        
    



    logo_flowable = resize([logo_path],(doc.width-36,15))[0]
    logo_flowable.hAlign = 'RIGHT'

    flow_list.append(logo_flowable)
    flow_list.append(name_flowable)
    flow_list.append(location_flowable)
    flow_list.append(FrameBreak())

    flow_list.append(program_details_header_flowable)
    flow_list.append(Spacer(1, 0.25*inch))
    flow_list.append(program_details_list_flowable)
    flow_list.append(Spacer(1, 0.25*inch))
    flow_list.append(summary_flowable)
    flow_list.append(FrameBreak())

    for i in top_right_frame_table:
        flow_list.append(i)
    flow_list.append(FrameBreak())

    flow_list.append(Spacer(1, 0.01*inch))
    flow_list.append(highlighted_alumni_header_flowable)
    flow_list.append(Spacer(1, 0.25*inch))
    for i in bottom_right_frame_table:
        flow_list.append(i)
    flow_list.append(FrameBreak())

    flow_list.append(more_info_flowable)
    flow_list.append(PageBreak())

def template2(doc,name_text, location_text, summary_text, logo_path, flow_list, details, alumni, alumni_links,alumni_logos,owner=[], owner_images=[],quote=False,speaker=False,speaker_image=False):
    pass