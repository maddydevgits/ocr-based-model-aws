import streamlit as st
import boto3
from PIL import Image
import os
import gtts

accessKey='' # ask admin to share access key
secretAccessKey='' # ask admin to share secret access
region='us-east-1'

st.title('OCR Based Model')

img_file=st.file_uploader('Upload Image',type=['png','jpg','jpeg'])

def load_img(img):
    img=Image.open(img)
    return img

if img_file is not None:
    file_details={}
    file_details['name']=img_file.name
    file_details['size']=img_file.size
    file_details['type']=img_file.type
    st.write(file_details)
    st.image(load_img(img_file),width=255)

    with open(os.path.join('uploads','src.jpg'),'wb') as f:
        f.write(img_file.getbuffer())
    
    st.success('Image Saved')
    client=boto3.client('textract',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    image=open('uploads/src.jpg','rb')
    response=client.detect_document_text(Document={'Bytes':image.read()})
    #st.write(response)
    text=''
    for item in response["Blocks"]:
        if item["BlockType"]=="LINE":
            lp=(item["Text"])
            st.write(lp)
            text+=lp
            text+=' '
    t1 = gtts.gTTS(text,lang = 'en')
        # save the audio file
    t1.save("welcome.mp3")
    audio_file = open("welcome.mp3",'rb')
    audio_bytes = audio_file.read()
    st.subheader('Audio Output of Text')
    st.audio(audio_bytes, format='audio/ogg', start_time=0)