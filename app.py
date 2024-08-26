from flask import Flask,render_template,request,redirect,url_for,flash, jsonify
import os
from flask_mail import Mail, Message

myKey = os.urandom(24)
app = Flask(__name__, static_folder='static')
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'programmingraw@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'programmingraw@gmail.com'
app.config['MAIL_PASSWORD'] = 'fmha djmp neid tvcv'

mail = Mail(app)
app.secret_key=myKey

adminID='Tansam'
adminPassword='TANSAM@123'

relative_path = 'static'
absolute_path = os.path.join(os.getcwd(), relative_path)
current_directory = os.getcwd()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} 

# STATIC_FOLDER = os.path.join(current_directory, 'static')
UPLOAD_FOLDER1 = os.path.join(app.root_path, 'static', 'blog_images')
UPLOAD_FOLDER2 = os.path.join(app.root_path, 'static', 'blog_contents')
UPLOAD_FOLDER3 = os.path.join(app.root_path, 'static', 'news_images')
UPLOAD_FOLDER4 = os.path.join(app.root_path, 'static', 'news_contents')
UPLOAD_FOLDER5 = os.path.join(app.root_path, 'static', 'test_images')
UPLOAD_FOLDER6 = os.path.join(app.root_path, 'static', 'test_contents')

app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
app.config['UPLOAD_FOLDER3'] = UPLOAD_FOLDER3
app.config['UPLOAD_FOLDER4'] = UPLOAD_FOLDER4
app.config['UPLOAD_FOLDER5'] = UPLOAD_FOLDER5
app.config['UPLOAD_FOLDER6'] = UPLOAD_FOLDER6

#  for blog saving path

#recent_blog_path = r"static\recent.txt"

#print(f"Contents of {os.getcwd()}: {', '.join(os.listdir())}")

# Define the absolute path for recent.txt
recent_blog_path = os.path.join(app.root_path, 'static', 'recent.txt')

# Check if the file exists before attempting to read it
if not os.path.exists(recent_blog_path):
    # Handle the case where the file does not exist
    # You can create the file or handle the error accordingly
    # For example:
    flash("Error: recent.txt file does not exist.")
else:
    # Read the file
    with open(recent_blog_path, 'r') as file:
        lines = file.readlines()
        # Process the file content as needed


def get_unique_filename(title, file_extension, folder):
    filename = f'{title}{file_extension}'
    filepath = os.path.join(app.config[folder], filename.replace('\\', '/'))

    counter = 1
    while os.path.exists(filepath):
        counter += 1
        filename = f'{title}{counter}{file_extension}'
        filepath = os.path.join(app.config[folder], filename.replace('\\', '/'))

    return filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def retrieve(d1,d2):
    posts = []
    c=0
    blog_images_directory = os.path.join(app.config[d1])
    blog_contents_directory = os.path.join(app.config[d2])

    for filename in os.listdir(blog_images_directory):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.gif'):
            imagepath = os.path.join(blog_images_directory, filename)
            imagee = imagepath.split('static')
            newimagepath = '/static/'+imagee[1].replace('\\','/')
            posts.append([newimagepath])

    for filename in os.listdir(blog_contents_directory):
        if filename.endswith('.txt'):
            contentpath = os.path.join(blog_contents_directory, filename)
            with open(contentpath, 'r') as content_file:
                content = content_file.read()
                posts[c].append(contentpath)
                c+=1
    c=0
    for ele in posts:
        kk=ele[0].split('/')
        mm=kk[len(kk)-1].split('.')
        mm[0]=mm[0][::-1]
        mm2=''
        for ele in mm[0]:
            try:
                if(int(ele)>0 and int(ele)<10):
                    continue 
                else:
                    mm2+=ele
            except:
                mm2+=ele
        mm2=mm2[::-1]
        posts[c].append(mm2)
        c+=1
    return posts

def islike(s1,s2):
    s1=s1[::-1]
    s1_new = ''
    for ele in s1:
        try:
            if(int(ele)>0 and int(ele)<10):
                continue 
            else:
                s1_new+=ele
        except:
            s1_new+=ele
    s1=s1_new[::-1]
    if(s1==s2):
        return True
    else:
        return False

def collect(value):
    b_d = os.path.join(app.config['UPLOAD_FOLDER2'])
    b_im = os.path.join(app.config['UPLOAD_FOLDER1'])
    n_d = os.path.join(app.config['UPLOAD_FOLDER4'])    
    n_im = os.path.join(app.config['UPLOAD_FOLDER3'])
    t_d = os.path.join(app.config['UPLOAD_FOLDER6'])
    t_im = os.path.join(app.config['UPLOAD_FOLDER5'])

    temp1 = [b_d,n_d,t_d]
    temp2 = [b_im,n_im,t_im]

    res,temp=[],[]

    for ele in temp2:
        for filename in os.listdir(ele):
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.gif'):
                imagepath = os.path.join(ele, filename)
                imagee = imagepath.split('static')
                newimagepath = '/static/'+imagee[1].replace('\\','/')
                name=filename.split('.')
                if(islike(name[0],value)):
                    temp.append(newimagepath)

    res.append(temp)
    temp=[]
    for ele in temp1:
        for filename in os.listdir(ele):
            if filename.endswith('.txt'):
                contentpath = os.path.join(ele, filename)
                name = filename.split('.')
                if(islike(name[0],value)):
                    with open(contentpath, 'r') as content_file:
                        content = content_file.read()
                        temp.append(contentpath)
    res.append(temp)
    temp=[]
    return res
        
def convertDate(date):
    d=['Januray','February','March','April','May','June','July','August','September','October','November','December']
    date=date.split('-')
    date[1]=d[int(date[1])-1]
    date=date[2]+'-'+date[1]+'-'+date[0]
    return date

def is_file_empty(file_path):
    size =  os.path.getsize(file_path)
    if size:
        return False
    else:
        return True

def deletecollect(type):
    m = []
    
    if is_file_empty(recent_blog_path):
        return m

    with open(recent_blog_path, 'r') as recent_file:
        lines = recent_file.readlines()  

    for line in lines:
        if line == '\n':
            continue  

        recent = line.split('|')
        recent_type = recent[3].strip()
        recent_status = recent[4].strip()

        if recent_type == type and recent_status == 'uploaded':
            recent_date = recent[0].strip()
            recent_title = recent[1].strip()
            recent_author = recent[2].strip()
            m_date = convertDate(recent_date)
            m.append([m_date, recent_title, recent_author])

    return m
@app.route("/")
@app.route("/index")
def index():
    # blog_posts = retrieve('UPLOAD_FOLDER1','UPLOAD_FOLDER2')
    # news_posts = retrieve('UPLOAD_FOLDER3','UPLOAD_FOLDER4')
    # testimony_posts = retrieve('UPLOAD_FOLDER5','UPLOAD_FOLDER6')
    return render_template("index.html")


#HOME PAGE
@app.route("/blogsDetails/<value>",methods=['GET'])  
def blogsDetails(value):
    result = collect(value)
    text=[]
    if(len(result[1])>0):
        for ele in result[1]:
            if(ele.endswith('.txt')):
                with open(ele, 'r') as content_file:
                    content = content_file.read()
                    content = content.split('\n')
                    date = content[0]
                    author = content[1]
                    content = content[2]
                    text.append([date,author,content])
    images=result[0]
    history=[]
    with open(recent_blog_path, 'r') as recent_file:
        for line in recent_file:
            recent = line.split('|')
            recent_date = recent[0].strip()
            recent_title = recent[1].strip() 
            m_date = convertDate(recent_date)
            history.append([m_date, recent_title])
    history.reverse()
    if(len(history)>=3):
        history=history[:3]
    return render_template("blogsdetails.html",images=images,text=text,title=value,history=history)

#SERVICES
@app.route("/reverseEngineering")
def reverseEngineering():
    return render_template("reveng.html")

@app.route("/aisolution")
def  aisolution():
    return render_template("aipage.html")

@app.route("/digitaltwin")
def digitaltwin():
    return render_template("digitwin.html")

@app.route("/productInnovation")
def productInnovation():
    return render_template("pdinnov.html")

@app.route("/iot")
def iot():
    return render_template("iot.html")

@app.route("/innovationManufacturing")
def innovationManufacturing():
    return render_template("innovmanu.html")  


@app.route("/ar_vr")
def ar_vr():
    return render_template("arvr.html")    

@app.route("/digitaltechnology")
def digitaltechnology():
    return render_template("digitaltechnology.html")


@app.route("/naanmudhalvan")
def naanmudhalvan():
    return render_template("nanmudhalvan.html")

#/////////////////////////////  GALLERY START \\\\\\\\\\\\\\\\\\\\\\
    
@app.route("/hackathon")
def hackathon():
    return render_template("hackathangallery.html")

@app.route("/tansamgallery")
def  tansamgallery():
    return  render_template("tansamgallery.html")

#///////////////////// GALLERY ENDS \\\\\\\\\\\\\\\\\\\\\\\\\\\\

@app.route("/hakathon_events")
def hakathon_events():
    return render_template("hackathonevents.html")
#\\\\\\\\\\\\\\\\\\\\\\\\\ events END /////////////////////
#/////////////////////////Quick Links \\\\\\\\\\\\\\\\\\\\\
@app.route("/quicklinks")
def quicklinks():
    return render_template("quicklink.html")

#////////// ABOUT US Start /////////
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")
#///////// ABOUT US END \\\\\\\\\
    
#////////// ABOUT US Start /////////
@app.route("/contactus", methods = ['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        try:

            msg = Message( subject=f"Mail from {name}",
                body = f"Name: {name} \nE-Mail: {email}  \n\n\nMessage: {message}",
                recipients=[email]
            )
            mail.send(msg)
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})
    return render_template("contactus.html")



@app.route("/adminLogin",methods=['GET'])
def adminLogin():
    return render_template("login.html")

@app.route("/adminIndex",methods=['POST'])
def adminIndex():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username==adminID and password==adminPassword:
            return redirect(url_for('admin'))
    return render_template("index.html")

@app.route("/admin")
def admin():
    blog_count,news_count,testimony_count = 0,0,0   
    with open(recent_blog_path, 'r') as file:
        lines = file.readlines()
    for ele in lines:
        if(ele=='\n'):
            lines.remove(ele)
    if(len(lines)!=0):
        for l in lines:
            mm=l.split('|')
            if(mm[3].strip()=='blogs' and mm[4].strip()=='uploaded'):
                blog_count+=1
            elif(mm[3].strip()=='news' and mm[4].strip()=='uploaded'):
                news_count+=1
            else:
                if(mm[4].strip()=='uploaded'):
                    testimony_count+=1
    if is_file_empty(recent_blog_path):
        return render_template("admin.html",blog_count=blog_count,news_count=news_count,testimony_count=testimony_count,history=[])
    else:
        with open(recent_blog_path, 'r') as recent_file:
            lines = recent_file.readlines()
        history = []
        if(len(lines)!=0):
            for ele in lines:
                if(ele=='\n'):
                    lines.remove(ele)
        else:
            return render_template("admin.html",blog_count=blog_count,news_count=news_count,testimony_count=testimony_count,history=[])
        for line in lines:
            recent = line.split('|')
            recent_date = recent[0].strip()
            recent_title = recent[1].strip() 
            recent_type = recent[3].strip()
            recent_status = recent[4].strip()
            m_date = convertDate(recent_date)
            history.append([recent_title,m_date,recent_type,recent_status])
        return render_template("admin.html",blog_count=blog_count,news_count=news_count,testimony_count=testimony_count,history=history)


@app.route("/adminPosts/<Type>")
def adminPosts(Type):
    if(Type=='blogs'):
        result = deletecollect('blogs')
    elif(Type=='news'):
        result = deletecollect('news')
    else:
        result = deletecollect('testimony')
    return render_template("adminblogs.html",type=Type,result=result)        


@app.route('/postDetails/<Type>', methods=['GET', 'POST'])
def postDetails(Type):
    if request.method == 'POST':
        if(Type == 'blogs'):
            title = request.form.get('blogstitle')
            date = request.form.get('blogsdate')
            author = request.form.get('blogsauthor')
            
            if 'blogsimage' not in request.files:
                return redirect(request.url)
            image = request.files['blogsimage']
            if image.filename == '':
                return redirect(request.url)

            if image and allowed_file(image.filename):
                os.makedirs(app.config['UPLOAD_FOLDER1'], exist_ok=True)
                os.makedirs(app.config['UPLOAD_FOLDER2'], exist_ok=True)
                filename = image.filename
                file_extension = os.path.splitext(filename)[1].lower()
                filename =get_unique_filename(title, file_extension, 'UPLOAD_FOLDER1')
                image_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename.replace('\\', '/'))
                image.save(image_path)

                blog_content = request.form.get('blogscontent')
                blog_filename = get_unique_filename(title, '.txt', 'UPLOAD_FOLDER2')
                blog_path = os.path.join(app.config['UPLOAD_FOLDER2'], blog_filename)

                with open(blog_path, 'w') as blog_file:
                    blog_file.write(date)
                    blog_file.write('\n')
                    blog_file.write(author)
                    blog_file.write('\n')
                    blog_file.write(blog_content)
            else:
                flash("File format not supported....")
                return redirect(url_for('adminPosts'),Type='')
            
            recent_title = request.form.get('blogstitle')
            recent_author = request.form.get('blogsauthor')
            recent_date = request.form.get('blogsdate')

        elif(Type == 'news'):
            title = request.form.get('newstitle')
            date = request.form.get('newsdate')
            author = request.form.get('newsauthor') 
            if 'newsimage' not in request.files:
                return redirect(request.url)
            
            image = request.files['newsimage']
            if image.filename == '':
                return redirect(request.url)

            if image and allowed_file(image.filename):
                os.makedirs(app.config['UPLOAD_FOLDER3'], exist_ok=True)
                os.makedirs(app.config['UPLOAD_FOLDER4'], exist_ok=True)
                filename = image.filename
                file_extension = os.path.splitext(filename)[1].lower()
                filename = get_unique_filename(title,file_extension, 'UPLOAD_FOLDER3')
                image_path = os.path.join(app.config['UPLOAD_FOLDER3'], filename.replace('\\', '/'))
                image.save(image_path)
                blog_content = request.form.get('newscontent')
                blog_filename = get_unique_filename(title, '.txt', 'UPLOAD_FOLDER4')
                blog_path = os.path.join(app.config['UPLOAD_FOLDER4'], blog_filename)

                with open(blog_path, 'w') as blog_file:
                    blog_file.write(date)
                    blog_file.write('\n')
                    blog_file.write(author)
                    blog_file.write('\n')
                    blog_file.write(blog_content)
            else:
                flash("File format not supported....")
                return redirect(url_for('adminPosts'),Type='')
            
            recent_title = request.form.get('newstitle')
            recent_author = request.form.get('newsauthor')
            recent_date = request.form.get('newsdate')

        else:
            title = request.form.get('testimonytitle')
            date = request.form.get('testimonydate')
            author = request.form.get('testimonyauthor')    

            if 'testimonyimage' not in request.files:
                return redirect(request.url)
            
            image = request.files['testimonyimage']

            if image.filename == '':
                return redirect(request.url)

            if image and allowed_file(image.filename):
                os.makedirs(app.config['UPLOAD_FOLDER5'], exist_ok=True)
                os.makedirs(app.config['UPLOAD_FOLDER6'], exist_ok=True)
                filename = image.filename
                file_extension = os.path.splitext(filename)[1].lower()
                filename = get_unique_filename(title,file_extension, 'UPLOAD_FOLDER5')
                image_path = os.path.join(app.config['UPLOAD_FOLDER5'], filename.replace('\\', '/'))
                image.save(image_path)

                blog_content = request.form.get('testimonycontent')
                blog_filename = get_unique_filename(title, '.txt', 'UPLOAD_FOLDER6')
                blog_path = os.path.join(app.config['UPLOAD_FOLDER6'], blog_filename)

                with open(blog_path, 'w') as blog_file:
                    blog_file.write(date)
                    blog_file.write('\n')
                    blog_file.write(author)
                    blog_file.write('\n')
                    blog_file.write(blog_content)
            else:
                flash("File format not supported....")
                return redirect(url_for('adminPosts'),Type='')
            
            recent_title = request.form.get('testimonytitle') 
            recent_author = request.form.get('testimonyauthor')  
            recent_date = request.form.get('testimonydate')
            
        with open(recent_blog_path, 'a') as recent_file:
                    recent_file.write(recent_date)
                    recent_file.write("|")
                    recent_file.write(recent_title)
                    recent_file.write("|")
                    recent_file.write(recent_author)
                    recent_file.write("|")
                    recent_file.write(Type)
                    recent_file.write('|')
                    recent_file.write('uploaded')
                    recent_file.write('\n')

        flash("Details uploaded successfully....")

        return redirect(url_for('admin'))

    return render_template("adminblogs.html")

@app.route("/changePassword",methods=['GET','POST'])    
def changePassword():
    global adminPassword
    if(request.method=='POST'):
        oldPassword=request.form.get('oldPassword')
        newPassword=request.form.get('newPassword')
        confirmPassword=request.form.get('confirmPassword')
        if(oldPassword==adminPassword):
            if(newPassword==confirmPassword):
                adminPassword=newPassword
                flash("Password changed successfully....")
                return redirect(url_for('admin'))
            else:
                flash("New password and confirm password not matched....")
                return redirect(url_for('changePassword'))
        else:
            flash("Old password is wrong....")
            return redirect(url_for('changePassword'))
    return render_template("changePassword.html")

@app.route("/delete/<Type>/<title>",methods=['GET','POST'])
def delete(Type,title):
    if(Type=='blogs'):
        b_d = os.path.join(app.config['UPLOAD_FOLDER2'])
        b_im = os.path.join(app.config['UPLOAD_FOLDER1'])
        temp1 = [b_d,b_im]
        for ele in temp1:
            for filename in os.listdir(ele):
                if filename.endswith('.txt'):
                    contentpath = os.path.join(ele, filename)
                    name = filename.split('.')
                    if(islike(name[0],title)):
                        os.remove(contentpath)
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.gif'):
                    imagepath = os.path.join(ele, filename)
                    name = filename.split('.')
                    if(islike(name[0],title)):
                        os.remove(imagepath)
    elif(Type=='news'):
        n_d = os.path.join(app.config['UPLOAD_FOLDER4'])    
        n_im = os.path.join(app.config['UPLOAD_FOLDER3'])
        temp1 = [n_d,n_im]
        for ele in temp1:
            for filename in os.listdir(ele):
                if filename.endswith('.txt'):
                    contentpath = os.path.join(ele, filename)
                    name = filename.split('.')
                    if(islike(name[0],title)):
                        os.remove(contentpath)
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.gif'):
                    imagepath = os.path.join(ele, filename)
                    name = filename.split('.')
                    if(islike(name[0],title)):
                        os.remove(imagepath)
    else:
        t_d = os.path.join(app.config['UPLOAD_FOLDER6'])
        t_im = os.path.join(app.config['UPLOAD_FOLDER5'])
        temp1 = [t_d,t_im]
        for ele in temp1:
            for filename in os.listdir(ele):
                if filename.endswith('.txt'):
                    contentpath = os.path.join(ele, filename)
                    name = filename.split('.')
                    if(islike(name[0],title)):
                        os.remove(contentpath)
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.gif'):
                    imagepath = os.path.join(ele, filename)
                    name = filename.split('.')
                    if(islike(name[0],title)):
                        os.remove(imagepath)

    with open(recent_blog_path, 'r') as file:
        lines = file.readlines()    
        line_to_delete = None
        for ele in lines:
            if(ele=='\n'):
                lines.remove(ele)
        for l in lines:
            deletitle = l.split('|')
            if islike(deletitle[1].strip(),title) and deletitle[3].strip() == Type:
                line_to_delete = l

    for line in lines:
        if(line==line_to_delete):
            l = line_to_delete.split('|')
            l[4] = 'deleted'
            o=''
            for i in range(len(l)-1):
                o+=l[i]+'|'
            o+=l[4]
            lines[lines.index(line)] = o+'\n'

    with open(recent_blog_path, 'w') as file:
        file.writelines(lines)


    flash("Post deleted successfully....")
    return redirect(url_for('adminPosts',Type=Type))

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port = 5000)
    except:
        print("Error in running the app")