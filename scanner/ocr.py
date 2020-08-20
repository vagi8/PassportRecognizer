from google.cloud import vision
import os 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\vageeshan.mankala\\apikeynew.json"
client = vision.ImageAnnotatorClient()
import io
from datetime import datetime as dt
from difflib import get_close_matches

global countries
countries=['IND','1ND','KEN']

def page2(path,cntry=None,web=0):
    try:
#        with io.open(path, "rb") as image_file:
#            content = image_file.read()
#        response = requests.get(path)
#        content=response.content
        if web==1:
            with io.open(path, "rb") as image_file:
                content = image_file.read()
        else:
            content=path
    except:
        return "Image Not Found"
    try:
        image = vision.types.Image(content=content)
        
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        for text in texts:
            a=text.description
            break
    except:
        return "Google API Error"        
    try:
        b=a.split("\n")
               
        if cntry=="KEN":
            word = 'place of residence'
            try:
                match=get_close_matches(word, b,n=1,cutoff=0.25)[0]
                ind=b.index(match)+1
                return b[ind]
            except:
                return ""
    
        else:  
            for i in range(len(b)):
                if max(b[i].find("PIN"), b[i].find("P1N")) > -1:
                    x="\\n".join(b[i-2:i+1])
            return x
    except:
        return "INVALID"
    

def page1(path,cntry=None,web=0):
    try:
#        response = requests.get(path)
#        content=response.content
#        with io.open(path, "rb") as image_file:
#            content = image_file.read()
        if web==1:
            with io.open(path, "rb") as image_file:
                content = image_file.read()
        else:
            content=path
    except:
        return "Image Not Found"
    try:
        image = vision.types.Image(content=content)
        
        response = client.text_detection(image=image)
        texts = response.text_annotations
        if len(texts)==0:
            return 3
        for text in texts:
            a=text.description
            if 'republic' not in a.lower():
                return 3
            break
    except:
        return "Google API Error"
    try:
        a=a.replace("c","<")
        a=a.replace("e","<")
        a=a.replace("!","I")
        b=a.split("\n")
        mx1=mx2=m1=m2=0
        for s in range(len(b)-1,0,-1):
            if not any(c.isalpha() for c in b[s]):
                continue
            c=b[s].count("<")
            if mx1 < c:
                mx2=mx1
                m2=m1
                mx1=c
                m1=s
            elif mx2 < c:
                mx2=c
                m2=s
        m=[m1,m2]
        m.sort()
    except:
        return "INVALID"
    try:
        dic={"PassportType":"",
             "PassportNo" :"",
             "Country":"",
             "Surname":"",
             "FullName":"",
             "Gender":"",
             "DOB":"",
             "DOE":""
             }
        
        line=b[m[0]]
        lines=line.split("<")
        while("" in lines):
            lines.remove("")
            
        for l in lines:
            if not any(c.isalpha() for c in l):
                lines.remove(l)
                continue
            if l.islower():
                lines.remove(l)
                continue
            elif not l.isupper():
                lines.remove(l)
                continue
            
        for cnt in countries:
            if cnt in a:
                cntry=cnt
                break
            
        if cntry==None:
            cntry="IND"
        if cntry=="KEN":
            country=["KEN"]
        elif cntry=="IND" or cntry=="1ND":
            country=["IND","1ND","!ND"]
                
            
        for c in country:
            if len(lines)>=4:
                dic['PassportType']=line[0]
                dic['Country']=lines[1][0:3]
                dic['Surname']=lines[1][3:]
                dic['FullName']=' '.join(lines[2:])
                break
            elif len(lines)==3:
                temp=" ".join(lines)
                dic['PassportType']=temp[0]
                if c in lines[0]:
                    dic['Country']=country[0]
                    x=lines[0].index(c)+len(c)
                    dic['Surname']=lines[0][x:]
                    dic['FullName']=" ".join(lines[1:])
                    break
                elif c in lines[1]:
                    dic['Country']=country[0]
                    x=lines[1].index(c)+len(c)
                    dic['Surname']=lines[1][x:]
                    dic['FullName']=" ".join(lines[2:])
                    break
                elif c in lines[2]:
                    dic['Country']=country[0]
                    x=lines[2].index("IND")+3
                    dic['Surname']=lines[2][x:]
                    break
            elif len(lines)==2:
                temp=" ".join(lines)
                dic['PassportType']=temp[0]
                if c in lines[0]:
                    dic['Country']=country[0]
                    x=lines[0].index(c)+len(c)
                    dic['Surname']=lines[0][x:]
                    dic['FullName']=" ".join(lines[1:])
                    break
                elif c in lines[1]:
                    dic['Country']=country[0]
                    x=lines[1].index(c)+len(c)
                    dic['Surname']=lines[1][x:]
                    dic['FullName']=" ".join(lines[2:])
                    break
            else:
                dic['PassportType']=line[0]
                if c in lines[0]:
                    dic['Country']=country[0]
                    x=lines[0].index(c)+len(c)
                    dic['Surname']=lines[0][x:]
                    break
        
        
        line=b[m[1]]
        lines=line.split("<")
        
        if not line[0].isalpha():
            pass
        dic["PassportNo"]=line[0:8]
        
        try:
            ind=line.index(dic['Country'])+3
        except:
            try:
                ind=line.index("1ND")+3
            except:
                ind=13
        
        if int(str(dt.now().year)[2:]) <= int(line[ind:ind+2]):
            yr=str(int(str(dt.now().year)[0:2])-1)
        else:
            yr=str(dt.now().year)[0:2]
        date=line[ind+4:ind+6]+"/"+line[ind+2:ind+4]+"/"+yr+line[ind:ind+2]
        dic["DOB"]=date
        
        if "M" in line:
            dic["Gender"]="M"
            
        elif "F" in line:
            dic["Gender"]="F"
            
        try:
            ind=line.index(dic["Gender"])+1
        except:
            ind=21
            
        yr=str(dt.now().year)[0:2]
        date=line[ind+4:ind+6]+"/"+line[ind+2:ind+4]+"/"+yr+line[ind:ind+2]
        dic["DOE"]=date
        return dic
    except:
        return dic

if __name__=='__main__':
    img_path = 'Akash Chatti.jpg'
#    img_path = 'kp1f.jpg'
    a=page1(img_path,web=1)

