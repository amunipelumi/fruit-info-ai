# import smtplib
# import os

# try:
#     server = smtplib.SMTP(os.getenv('EMAIL_HOST'), 587) 
#     server.starttls()
#     server.login(os.getenv('SOURCE_EMAIL'), os.getenv('EMAIL_HOST_PASSWORD'))
#     print("Connection successful")
# except Exception as e:
#     print(f"Error: {e}")
# finally:
#     if 'server' in locals(): 
#         server.quit()

