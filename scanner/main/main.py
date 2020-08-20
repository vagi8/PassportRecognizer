from flask import Flask,render_template
from flask import request
app = Flask(__name__)
from flask import jsonify
#api = Api(app)
from flask_cors import CORS, cross_origin
from waitress import serve
import flask_monitoringdashboard as dashboard
import os
from werkzeug import secure_filename
import ocr
import requests
import onboading as ob
import compare
from speech_text import speech_to_text
dashboard.bind(app)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/train": {"origins": "*"}})

os.makedirs(os.path.join(app.instance_path, 'AppData'), exist_ok=True)

@app.route("/web", methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content- Type'])
def web():
    if request.method == 'POST':
        global path
        f1 = request.files['img1']
        f2 = request.files['img2']
        
        filename1=secure_filename(f1.filename)
        filename2=secure_filename(f2.filename)
        
        f1.save(os.path.join(app.instance_path, 'AppData',filename1))
        f2.save(os.path.join(app.instance_path, 'AppData',filename2))
        
        path1=str(os.path.join(app.instance_path, 'AppData',filename1))
        path2=str(os.path.join(app.instance_path, 'AppData',filename2))
        arch1=ocr.page1(path=path1,web=1)
        arch2=ocr.page2(path=path2,web=1)
    #    path1='C:\\Users\\vageeshan.mankala\\passport1.JPG'
    #    arch1=ocr.page1(path1)
        return render_template('accuracy3.html' , accuracy=str(arch1)+'\n\n'+str(arch2))
    return render_template('test3.html')

@app.route("/api", methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content- Type'])
def api():
    if request.method == 'GET':
        img_path=request.args['img']
        pg=int(request.args['page'])
        name=request.args['name']
        cntry=request.args['cntry']
        print(img_path)
        print(pg)
        print(name)
        print(cntry)
        try:
            response = requests.get(img_path)
            content=response.content
        except:
            return jsonify({'Error':"ERROR"})
        if pg==1:
            arch1=ocr.page1(content)
            print(arch1)
            type(arch1)
            a=ob.extract_face(content,name)
            print(a)
            if type(arch1)==dict:
                arch1['Status']=str(a)
                return jsonify(arch1)
            else:
                ret={'Error':arch1}
            return jsonify(ret)
        if pg==2:
            arch2=ocr.page2(content,cntry)
            print(arch2)
            return arch2
        
@app.route("/compare", methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content- Type'])
def com():
    if request.method == 'GET':
        img_path=request.args['img']
        vid_path=request.args['vid']
        otp=request.args['otp']
        name=request.args['name']
        
        try:
            vid_content = requests.get(vid_path).content
        except:
            return "Video Blob File Not Found"
        out_dir=os.path.join(app.instance_path, 'AppData')
        vid_local_path=os.path.join(out_dir,name+'.mp4')
        with open(vid_local_path,"wb") as f:
            f.write(vid_content)
        
        try:
            text=speech_to_text(vid_local_path,name,out_dir)
            
        except:
            return "Could Not Process Speech to text"
        
        try:
            no=int(text.transcript)
            print(text.transcript)
            if no!=int(otp):
                return "MatchError"
            if no==int(otp):
                print("OTP Matched")
        except:
            return "OTP Error"
        
        a= compare.compare(img_path,vid_local_path)
        print(a)
        
        return str(a)
    
if __name__=='__main__':
#    app.run(debug=False,host='192.168.11.197',port=562)
    serve(app, host='0.0.0.0', port=562)