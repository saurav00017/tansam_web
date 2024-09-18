from flask import Flask,render_template,request,redirect,url_for,flash, jsonify
import os
from flask_mail import Mail, Message
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User, Event
from app import db, app
from datetime import datetime,timedelta
from collections import defaultdict
import calendar as cal

myKey = os.urandom(24)
app.config['MAIL_SERVER'] = "smtp.hostinger.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'contact@tansam.org'
app.config['MAIL_DEFAULT_SENDER'] = 'contact@tansam.org'
app.config['MAIL_PASSWORD'] = 'Tansam@1234567'

mail = Mail(app)
app.secret_key=myKey

adminID='Tansam'
adminPassword='TANSAM@123'

relative_path = 'static'
absolute_path = os.path.join(os.getcwd(), relative_path)
current_directory = os.getcwd()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} 




@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


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
                recipients=['contact@tansam.org','hannahr@tansam.org'],
                reply_to=email,
                bcc=['hannahr@tansam.org']
            )
            mail.send(msg)
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})
    return render_template("contactus.html")

@app.route("/downloads",methods=['GET'])
def download():
    documents = [
        {"name": "Tansam Information Brochure 1", "file_url": "/static/brochures/Tansam Information Brochure 1.pdf"},
        {"name": "TANSAM Information Brochure 2", "file_url": "/static/brochures/TANSAM Information Brochure 2.pdf"},
        # Add more documents here
    ]
    return render_template('download.html', documents=documents)

@app.route("/socialmedia",methods=['GET'])
def social_media():
    return render_template('socialMedia.html')



# Admin urls
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            
            # Check for next parameter to redirect the user
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('admin_dashboard'))

    return render_template('login_cal.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if request.method == 'POST':
        title = request.form.get('title')
        date_str = request.form.get('date')
        description = request.form.get('description')
        
        # Convert string to date
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."
        
        event = Event(title=title, date=event_date, description=description)
        db.session.add(event)
        db.session.commit()
        
    return render_template('admin_dashboard.html')


@app.route('/edit_events', methods=['GET', 'POST'])
@login_required
def edit_events():
    if request.method == 'POST':
        month = request.form.get('month')
        year = request.form.get('year')
        start_date = datetime.strptime(f"{year}-{month}-01", '%Y-%m-%d')
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        events = Event.query.filter(Event.date >= start_date, Event.date <= end_date).all()
        # Group events by date
        grouped_events = defaultdict(list)
        for event in events:
            grouped_events[event.date].append(event)
        
        return render_template('edit_events.html', grouped_events=grouped_events, selected_month=month, selected_year=year, current_year=year, success_message=request.args.get('success_message'))

    # Default to current month and year if GET request
    current_month = datetime.now().strftime('%m')
    current_year = datetime.now().year
    start_date = datetime.strptime(f"{current_year}-{current_month}-01", '%Y-%m-%d')
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    
    events = Event.query.filter(Event.date >= start_date, Event.date <= end_date).all()
    grouped_events = defaultdict(list)
    for event in events:
        grouped_events[event.date].append(event)

    return render_template('edit_events.html', grouped_events=grouped_events, selected_month=current_month, selected_year=current_year, current_year=current_year)



@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        event.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('admin_dashboard', success_message='Event updated successfully!'))

    return render_template('edit_event.html', event=event)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar_view():
    # Handle POST request for adding/updating events
    if request.method == 'POST':
        event_date_str = request.form.get('event_date')
        event_title = request.form.get('event_title')
        
        if event_date_str and event_title:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            new_event = Event(date=event_date, title=event_title)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('calendar_view'))  # Redirect to avoid form resubmission

    # Handle GET request to display calendar
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))

    today = datetime.now().day if month == datetime.now().month else None

    # Get the month name
    month_name = cal.month_name[month]

    # Generate the calendar for the month
    cal_instance = cal.Calendar(firstweekday=6)  # Sunday as the first day of the week
    month_days = cal_instance.monthdayscalendar(year, month)

    events = Event.query.filter(
        db.extract('month', Event.date) == month,
        db.extract('year', Event.date) == year
    ).all()

    return render_template(
        'calendar.html', current_month=month_name, current_year=year,
        weeks=month_days, events=events, current_day=today,
        previous_month=(month - 1) or 12,
        previous_year=year - 1 if month == 1 else year,
        next_month=(month + 1) if month < 12 else 1,
        next_year=year + 1 if month == 12 else year
    )
