
# coding: utf-8

# In[15]:


import smtplib
from os.path import basename,splitext


# In[20]:


#splitext(basename("../sss/file1.rsr"))[0]


# In[23]:



# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
def send_email(strFrom,strTo,subj,strhtml,*attachments):
    from email.mime.multipart import MIMEMultipart
    from email.mime  import text
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders




    # Define these once; use them twice!
    #strFrom = 'from@example.com'
    #strTo = 'to@example.com'

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    #msgRoot['Subject'] = 'test message'
    msgRoot['Subject'] = subj
    msgRoot['From'] = strFrom
    msgRoot['To'] = ','.join(strTo)
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText(strhtml)
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    #msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgText = MIMEText(strhtml, 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
##################LOGO#################
    #     fp = open(logo_pic, 'rb')
#     msgImage = MIMEImage(fp.read())
#     fp.close()
    # Define the image's ID as referenced above
#     msgImage.add_header('Content-ID', '<teb>')
#     msgRoot.attach(msgImage)
############################

    for img in attachments:
        fp = open(str(img), 'rb')
        if str(img)[-3:] =='jpg' or  str(img)[:-3] =='png' :
            
            
            msgImage = MIMEImage(fp.read())
            fp.close()

            # Define the image's ID as referenced above
            #msgImage.add_header('Content-ID', '<'+str(img)+'>')
            ####msgImage.add_header('Content-ID', '<'+str(img[:-4])+'>')
            msgImage.add_header('Content-ID', '<'+splitext(basename((img)))[0]+'>')
            msgRoot.attach(msgImage)
        else: #Addin ttached file 
#             if ctype is None or encoding is not None:
                    
            # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
#                     ctype = 'application/octet-stream'
#                     maintype, subtype = ctype.split('/', 1)

                     msg = MIMEBase('application', 'octet-stream')
                     msg.set_payload(fp.read())
                     fp.close()
        #            msgImage.add_header('Content-ID', '<'+str(img[:-4])+'>')
                     msg.add_header('Content-Disposition', 'attachment', filename=img)

                     msgRoot.attach(msg)
                     encoders.encode_base64(msg)

#                     print("mmmmmmmmmmmmmmmm")
#             fp = open(img, 'rb')
#             msgAttache = MIMEMultipart(fp.read())
#             fp.close()

#             part = MIMEBase('application', "octet-stream")
#             part.set_payload(open("text.txt", "rb").read())
#             Encoders.encode_base64(part)
#
#             part.add_header('Content-Disposition', 'attachment; filename="text.txt"')

#             msg.attach(part)


            # Define the image's ID as referenced above
            #msgImage.add_header('Content-ID', '<'+str(img)+'>')
            #msgAttache.add_header('Content-ID', '<'+str(img[:-4])+'>')
#            msgRoot.attach(msgAttache)
###############################
            #     fp = open('teb.jpg', 'rb')
            #     msgImage = MIMEImage(fp.read())
            #     fp.close()

            #     # Define the image's ID as referenced above
            #     msgImage.add_header('Content-ID', '<teb>')
            #     msgRoot.attach(msgImage)
            # ##-----------------
            #     fp = open('graph1.jpg', 'rb')
            #     msgImage = MIMEImage(fp.read())
            #     fp.close()

            #     # Define the image's ID as referenced above
            #     msgImage.add_header('Content-ID', '<graph1>')
            #     msgRoot.attach(msgImage)
            # ##-----------------
            #     fp = open('graph2.jpg', 'rb')
            #     msgImage = MIMEImage(fp.read())
            #     fp.close()

            #     # Define the image's ID as referenced above
            #     msgImage.add_header('Content-ID', '<graph2>')
            #     msgRoot.attach(msgImage)
    
########################################
    # Send the email (this example assumes SMTP authentication is required)
    smtp = smtplib.SMTP()
    smtp.connect('localhost')
    #smtp.login('exampleuser', 'examplepass')
    
     
    #header = 'To:' + ", ".join(to) + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: ' + subject + '\n'
    #msg = header + '\n' + subject + '\n\n'

    
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    
   
    
    
    smtp.quit()
#d3="Test Mail"


# In[3]:


# #d1=Data.to_html()
# with open('head1.txt' ,'r') as f:
#     d2=f.read()
# d3=d2+d1
# d3 = pynliner.fromString(d3)

# with open(outhtml(),'w') as f3:
#     f3.write(d3)
# try:
#     1/0
# except Exception as e:
#     #print (type(str(e)))
#     print(str(e))


# In[4]:


# recipients=['Mahmoud.iaboelenin@tedata.net']
# # #recipients='Mahmoud.iaboelenin@tedata.net  farid.farouk@tedata.net  saeed.yasser@tedata.net  ehab.afifi@tedata.net'
# send_email('Mahmoud.iaboelenin@tedata.net',recipients,'Mtest',"d3",'REJECT.html.gz')


# In[5]:


#Oroginal function 
# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
            # def send_email(strFrom,strTo,subj,strhtml):
            #     from email.mime.multipart import MIMEMultipart
            #     from email.mime  import text
            #     from email.mime.image import MIMEImage
            #     from email.mime.text import MIMEText


            #     # Define these once; use them twice!
            #     #strFrom = 'from@example.com'
            #     #strTo = 'to@example.com'

            #     # Create the root message and fill in the from, to, and subject headers
            #     msgRoot = MIMEMultipart('related')
            #     #msgRoot['Subject'] = 'test message'
            #     msgRoot['Subject'] = subj
            #     msgRoot['From'] = strFrom
            #     msgRoot['To'] = ','.join(strTo)
            #     msgRoot.preamble = 'This is a multi-part message in MIME format.'

            #     # Encapsulate the plain and HTML versions of the message body in an
            #     # 'alternative' part, so message agents can decide which they want to display.
            #     msgAlternative = MIMEMultipart('alternative')
            #     msgRoot.attach(msgAlternative)

            #     msgText = MIMEText(strhtml)
            #     msgAlternative.attach(msgText)

            #     # We reference the image in the IMG SRC attribute by the ID we give it below
            #     #msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
            #     msgText = MIMEText(strhtml, 'html')
            #     msgAlternative.attach(msgText)

            #     # This example assumes the image is in the current directory
            #     fp = open('te.png', 'rb')
            #     msgImage = MIMEImage(fp.read())
            #     fp.close()

            #     # Define the image's ID as referenced above
            #     msgImage.add_header('Content-ID', '<image1>')
            #     msgRoot.attach(msgImage)
            # ###############################
            #     fp = open('teb.jpg', 'rb')
            #     msgImage = MIMEImage(fp.read())
            #     fp.close()

            #     # Define the image's ID as referenced above
            #     msgImage.add_header('Content-ID', '<teb>')
            #     msgRoot.attach(msgImage)
            # ##-----------------
            #     fp = open('graph1.jpg', 'rb')
            #     msgImage = MIMEImage(fp.read())
            #     fp.close()

            #     # Define the image's ID as referenced above
            #     msgImage.add_header('Content-ID', '<graph1>')
            #     msgRoot.attach(msgImage)
            # ##-----------------
            #     fp = open('graph2.jpg', 'rb')
            #     msgImage = MIMEImage(fp.read())
            #     fp.close()

            #     # Define the image's ID as referenced above
            #     msgImage.add_header('Content-ID', '<graph2>')
            #     msgRoot.attach(msgImage)

            # ########################################
            #     # Send the email (this example assumes SMTP authentication is required)
            #     import smtplib
            #     smtp = smtplib.SMTP()
            #     smtp.connect('localhost')
            #     #smtp.login('exampleuser', 'examplepass')


            #     #header = 'To:' + ", ".join(to) + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: ' + subject + '\n'
            #     #msg = header + '\n' + subject + '\n\n'


            #     smtp.sendmail(strFrom, strTo, msgRoot.as_string())




            #     smtp.quit()
            #recipients=['Mahmoud.iaboelenin@tedata.net','farid.farouk@tedata.net','saeed.yasser@tedata.net', 'ehab.afifi@tedata.net']
            # recipients=['Mahmoud.iaboelenin@tedata.net']
            # #recipients='Mahmoud.iaboelenin@tedata.net  farid.farouk@tedata.net  saeed.yasser@tedata.net  ehab.afifi@tedata.net'
            # send_email('Mahmoud.iaboelenin@tedata.net',recipients,'Multiple-Login',d3)

