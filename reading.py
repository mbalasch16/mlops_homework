
print("reading from a file")

with open("/mlops_sentiment_lab/email_text.txt",'r') as file:
    lines = file.readlines()
    
print(lines)
    
    