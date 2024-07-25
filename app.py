from flask import Flask, make_response, render_template, request, redirect, flash, get_flashed_messages,session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from email.message import EmailMessage
import smtplib
import random

# Flask(__name__) creates a Flask application instance
app = Flask(__name__)

app.secret_key = os.urandom(20)
# specifies the database URL.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blogosphere.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLAlchemy(app) initializes the database object with the Flask app
db = SQLAlchemy(app)
app.app_context().push()

#Database_section
# db.Model tells SQLAlchemy that the class is a table in the database.
class Blogosphere_subscribers(db.Model):
    __tablename__ = 'blogosphere_subscribers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable = False, unique=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#Blogs by user
class Blogosphere_blogs(db.Model):
    __tablename__ = 'blogosphere_blogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class AdminPanel(db.Model):
    __tablename__ = 'blogosphere_adminpanel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    check = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/home')
def home():
  return render_template('main.html')

def password_generator_subscriber(name):
  while True:
    username = name.replace(' ','')
    password = username + ''.join([str(random.randint(0, 9)) for _ in range(random.randint(7, 9))])
    existing_password = Blogosphere_subscribers.query.filter_by(password=password).first()
    if not existing_password:
      return password

def send_email_to_subscriber(name, email, password):
  msg = EmailMessage()
  msg.set_content( f'Hello {name}, \n your password for Uploding Blogs is {password}. Don\'t share it will anyone 🫣.')
  msg['Subject'] = 'Thanks for Subscribing ❤'
  msg['From'] = "blogosphere009@gmail.com"
  msg['To'] = email
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login('blogosphere009@gmail.com', 'hlsz tpxf ostq voxc')
  server.sendmail('blogosphere009@gmail.com', email, msg.as_string())
  server.quit()
  print('Email sent')

# This route is used to check if the user has subscibed or not
@app.route('/subscribe', methods=["POST", "GET"])
def subscribe():
  if request.method == "POST":
    name = request.form.get("name")
    email = request.form.get("email")
    existing_user = Blogosphere_subscribers.query.filter_by(email=email).first()
    if not existing_user:
      password = password_generator_subscriber(name.lower())
      send_email_to_subscriber(name,email,password)
      new_user = Blogosphere_subscribers(name=name, email=email, password=password)
      db.session.add(new_user)
      try:
        db.session.commit()
        flash('Thanks for subscribing!', 'success')
      except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'error')
      return redirect('home')
    else:
      flash('You are already subscribed', 'info')
      return render_template('main.html')
  return render_template('main.html')

# This function is used to rename the image file and store it in upload images folder
def image_saver(image, blog_id):
    if not os.path.exists('static/upload_images'):
      os.makedirs('static/upload_images')
    filename = f"image_blogid_{blog_id}.jpg"
    file_path = os.path.join('static/upload_images', filename)
    image.save(file_path)
    print("Image Saved")

@app.route('/content', methods=["GET", "POST"])
def content():
  if request.method == "POST":
    name = request.form.get('name')
    email = request.form.get('email')
    title = request.form.get('title')
    message = request.form.get('message')
    image = request.files['image']
    password = request.form.get('password')
    if not (name and email and title and message and image):
        flash("please upload everything", "info")
    # Checking if user exists
    user = Blogosphere_subscribers.query.filter_by(name=name, email=email).first()
    if user and (image and allowed_image(image.filename)):
      if password == user.password:
      # storing name,email, title and message in database
        blog = Blogosphere_blogs(name=name, email=email, title=title, content=message)
        db.session.add(blog)
        db.session.commit()
        try:
          image_saver(image, blog.id)
          return redirect('/blogs')
        except Exception as e:
          db.session.rollback()
          flash(f"An error occurred while saving the image: {e}", "error")
          return render_template('content.html')
      else:
        flash(f"wrong Password", "error")
        return render_template('content.html')
    else:
        flash(f"Something wrong went!!", "error")
        return render_template('content.html')
  return render_template('content.html')

# Starting page
@app.route('/')
def start():
  count = Blogosphere_subscribers.query.count()
  return render_template('start.html', count = count)

@app.route('/blogs', methods=['GET', 'POST'])
def blog():
  if request.method == 'POST':
    topic = request.form.get('topic')
    if topic:
      result = Blogosphere_blogs.query.filter(Blogosphere_blogs.title.ilike(f'%{topic}%')).all()
      if result:
        remaining_blogs = [blog for blog in Blogosphere_blogs.query.all() if blog not in result]
        return render_template('blogs.html', blogs=result + remaining_blogs, blogosphere_subscribers = Blogosphere_subscribers, Searched=True)
      else:
        flash('Sorry, No blogs found.', 'info')
        return redirect('/blogs')
  # fetching all blogs from blogoshere_blogs table
  blogs = Blogosphere_blogs.query.all()
  return render_template('blogs.html',blogs = blogs,blogosphere_subscribers = Blogosphere_subscribers, Searched = False)

@app.route('/blogs/<email>/<int:blog_id>', methods=['GET'])
def full_blog(email, blog_id):
    blog = Blogosphere_blogs.query.filter_by(email=email, id=blog_id).first()
    if blog:
        return render_template('full_blog.html', blog=blog)
    else:
        flash('Blog not found!', 'error')
        return redirect('/home')

@app.route('/about_us')
def about_us():
  return render_template('About_us.html')
  
@app.route('/contact_us')
def contact_us():
  return render_template('Contact_us.html')

# Catergories------>
@app.route('/categories')
def categories():
  return render_template('Categories.html')

@app.route('/technology')
def technology():
  return render_template('Category/Technology/technology.html')

@app.route('/astronomy')
def astronomy():
  return render_template('Category/Astronomy/astronomy.html')

@app.route('/b&f')
def finance():
  return render_template('Category/Business&Finance/b&f.html')

@app.route('/sports')
def sports():
  return render_template('Category/Sports/sports.html')

@app.route('/foods')
def foods():
  return render_template('Category/Foods/food.html')

#-------------------Blogs--------------------

# Technology-->
@app.route('/ai_drug')
def ai_drug():
  return render_template('blogs/Technology/ai_drug.html')

@app.route('/ai_healthcare')
def ai_healthcare():
  return render_template('blogs/Technology/ai_healthcare.html')

@app.route('/ai_m')
def ai_m():
  return render_template('blogs/Technology/ai_m&m.html') 

@app.route('/ai_er')
def ai_er():
  return render_template('blogs/Technology/ai_reality.html') 

@app.route('/ai_meta')
def ai_meta():
  return render_template('blogs/Technology/ai_metaverse.html') 

@app.route('/voice_tech')
def voice_tech():
  return render_template('blogs/Technology/voice_technology.html') 

@app.route('/quantum')
def quantum():
  return render_template('blogs/Technology/quantum.html') 

# Astronomy-->
@app.route('/blackhole')
def blackhole():
  return render_template('blogs/Astronomy/blackhole.html')

@app.route('/exoplanet')
def exoplanet():
  return render_template('blogs/Astronomy/exoplanet.html')

@app.route('/mars')
def mars():
  return render_template('blogs/Astronomy/mars.html')

@app.route('/galaxy')
def galaxy():
  return render_template('blogs/Astronomy/galaxy.html')

@app.route('/comets')
def comets():
  return render_template('blogs/Astronomy/comets.html')

@app.route('/magnetic')
def magnetic():
  return render_template('blogs/Astronomy/magnetic.html')

@app.route('/auroras')
def auroras():
  return render_template('blogs/Astronomy/auroras.html')

#Finance
@app.route('/finance_mistakes')
def finance_mistakes():
  return render_template('blogs/Business&Finance/financial_mistakes.html')

@app.route('/invest_stock')
def invest_stock():
  return render_template('blogs/Business&Finance/invest_stock.html')

@app.route('/investment')
def investment():
  return render_template('blogs/Business&Finance/investment.html')

@app.route('/personal_budget')
def personal_budget():
  return render_template('blogs/Business&Finance/personal_budget.html')

@app.route('/relation_finance')
def relation_finance():
  return render_template('blogs/Business&Finance/relation_finance.html')

@app.route('/rent_home')
def rent_home():
  return render_template('blogs/Business&Finance/rent_home.html')

@app.route('/save_money')
def save_money():
  return render_template('blogs/Business&Finance/save_money.html')

#Sports-->
@app.route('/cricket_india')
def cricket_india():
  return render_template('blogs/Sports/cricket_india.html')

@app.route('/esports')
def esports():
  return render_template('blogs/Sports/esports.html')

@app.route('/iconic_moment')
def iconic_moment():
  return render_template('blogs/Sports/iconic_moment.html')

@app.route('/indian_games')
def indian_games():
  return render_template('blogs/Sports/indian_games.html')

@app.route('/life_of_cricketer')
def life_of_cricketer():
  return render_template('blogs/Sports/life_of_cricketer.html')

@app.route('/new_technology')
def new_technology():
  return render_template('blogs/Sports/new_technology.html')

@app.route('/sports_world')
def sports_world():
  return render_template('blogs/Sports/sports_world.html')

#Food-->
@app.route('/vegan')
def vegan():
  return render_template('blogs/Foods/vegan.html')

@app.route('/ftof')
def ftof():
  return render_template('blogs/Foods/ftof.html')

@app.route('/culinary')
def culinary():
  return render_template('blogs/Foods/culinary.html')

@app.route('/innovation')
def innovation():
  return render_template('blogs/Foods/innovation.html')

@app.route('/habits')
def habits():
  return render_template('blogs/Foods/habits.html')

@app.route('/paring')
def paring():
  return render_template('blogs/Foods/paring.html')

@app.route('/photography')
def photography():
  return render_template('blogs/Foods/photography.html')

# -------------------------------------------------------------------------------------------------------------------
                                   # AdminPanel
# -------------------------------------------------------------------------------------------------------------------

from functools import wraps
from flask import make_response
# Preventing caching in the browser.
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return no_cache


# Sending otp via email for accessing admin panel
def send_email(name, email, otp):
  msg = EmailMessage()
  msg.set_content(f'Hello {name}, your otp is {otp}')
  msg['Subject'] = 'Admin Panel Access'
  msg['From'] = "blogosphere009@gmail.com"
  msg['To'] = email
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login('blogosphere009@gmail.com', 'hlsz tpxf ostq voxc')
  server.sendmail('blogosphere009@gmail.com', email, msg.as_string())
  server.quit()
  print('Email sent')

# Generating random otp number
def generate_random_otp():
  return ''.join([str(random.randint(0, 9)) for _ in range(6)])

@app.route('/levaze/blogosphere/admin/adminpanel', methods=["GET", "POST"])
def adminpanel():
  # If any person gose from subscriberspage to adminpanel without logging out then it will consider as logout user
  session.pop('admin_logged_in', None)
  generate = False
  if request.method == "POST":
      # fetching details from admin_panel.html throught post request
      name = request.form.get('name')
      email = request.form.get('email')
      password = request.form.get('password')
      # Checking if name and email is in the list
      if name.lower() in ['yash', 'shashank', 'diti'] and email.lower() in ['yash.patkar2004@gmail.com', 'yashpatkar194@gmail.com', 'dgadia87@gmail.com', 'shashankpc7746@gmail.com']:
          # Checking if password matches
          if password == "group9":
            # generate otp
            otp = generate_random_otp()
            # Storing details in the session
            session['otp'] = otp
            session['name'] = name
            session['email'] = email
            session['password'] = password
            # Sending email
            send_email(name, email, otp)
            print(session['otp'], session['name'], session['email'])
            # if generate True then admin will able to see the verification otp input
            generate = True
            return render_template('/admin/admin_panel.html', generate=generate)
          else:
            # Flashing message
            flash("Wrong Password", "error")
            return redirect(url_for('adminpanel'))
      else:
        flash("Wrong name or email", "error")
        return redirect(url_for('adminpanel'))
  return render_template('/admin/admin_panel.html', generate=generate)

@app.route('/levaze/blogosphere/admin/verify_otp', methods=["POST"])
# using the @nocache decorator, the browser will not store the cache 
@nocache
def verify_otp():
    # Fetching data from session and from adminpanel.html
    user_otp = request.form.get('otp')
    name = session.get('name')
    email = session.get('email')
    password = session.get('password')
    generated_otp = session.get('otp')
    if name is not None and email is not None and password == 'group9' and generated_otp == user_otp:
        approved = "Approved"
        # Entry to database when the user try to access the admin panel
        new_entry = AdminPanel(name=name, email=email, password=password, check=approved)
        db.session.add(new_entry)
        db.session.commit()
        print('Entry added to the database')
        # Delecting all the data inside session
        session.clear()
        session['admin_logged_in'] = True
        return redirect(url_for('subscriberspage'))
    else:
      approved = "Not approved"
      new_entry = AdminPanel(name=name, email=email, password=password, check=approved)
      db.session.add(new_entry)
      db.session.commit()
      session.clear()
      return redirect(url_for('blog'))

@app.route('/logout', methods = ['POST'])
@nocache
def logout():
  if 'admin_logged_in' not in session or not session['admin_logged_in']:
    return redirect(url_for('home'))
  session.pop('admin_logged_in', None)
  return redirect(url_for('home'))
# -------------------------------------------------------------------------------------------------------------------
                                   # End of AdminPanel 
# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
                                   # AdminPage 
# -------------------------------------------------------------------------------------------------------------------

@app.route('/levaze/blogosphere/admin/subscriberspage')
@nocache
def subscriberspage():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
      return redirect(url_for('adminpanel'))
    subscribers = Blogosphere_subscribers.query.all()
    return render_template('/admin/subscribers.html', subscribers=subscribers, blogosphere_blogs = Blogosphere_blogs)

@app.route('/levaze/blogosphere/admin/delete_subscriber', methods=['POST'])
@nocache
def delete_subscriber():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
      return redirect(url_for('adminpanel'))
    email = request.form.get('email')
    subscriber = Blogosphere_subscribers.query.filter_by(email = email).first()
    if subscriber:
      blogs = Blogosphere_blogs.query.filter_by(email = email).all()
      for blog in blogs:
        try:
          blog_photo = os.path.join('static','upload_images',f'image_blogid_{blog.id}.jpg')
          if blog_photo:
            # deleting the blog image
            os.remove(blog_photo)
        except:
          pass
        # deleting each blog of specific email
        db.session.delete(blog)
      db.session.commit()
      # deleting the subscriber
      db.session.delete(subscriber)
      db.session.commit()
      print("subscriber and there blog has been deleted")
    else:
      flash("no subscriber found.","error")
      return redirect('subscriberspage')      
    return redirect(url_for('subscriberspage'))
# -------------------------------------------------------------------------------------------------------------------
                                             # End of AdminPage 
# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
                                   # Subscriber Blogs 
# -------------------------------------------------------------------------------------------------------------------

@app.route('/levaze/blogosphere/admin/subscriber_blogpage')
@nocache
def subscribers_blogpage():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
      return redirect(url_for('adminpanel'))
    blogs = Blogosphere_blogs.query.all()
    return render_template('/admin/subscribers_blog.html', blogs=blogs)

@app.route('/levaze/blogosphere/admin/delete_blog', methods=['POST'])
@nocache
def delete_blog():
  if 'admin_logged_in' not in session or not session['admin_logged_in']:
    return redirect(url_for('adminpanel'))
  id = request.form.get('id')
  blog = Blogosphere_blogs.query.filter_by(id=id).first()
  if blog:
    try:
      # Joining the path
      blog_photo = os.path.join('static','upload_images',f'image_blogid_{blog.id}.jpg')
      # if photo exist
      if blog_photo:
        #deleting the blog image
        os.remove(blog_photo)
      else:
        print("Blog image not found")
    except:
      pass
    db.session.delete(blog)
    db.session.commit()
    print("Blog deleted successfully")
  else:
    flash("The blog does not exist", "error")
  return redirect(url_for('subscribers_blogpage'))
# -------------------------------------------------------------------------------------------------------------------
                                   # End of Subscriber Blog Page 
# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
                                   # Verified Subscriber 
# -------------------------------------------------------------------------------------------------------------------
@app.route('/levaze/blogosphere/admin/verified_subscriber', methods = ['POST'])
@nocache
def verified_subscriber():
  if 'admin_logged_in' not in session or not session['admin_logged_in']:
    return redirect(url_for('adminpanel'))
  email = request.form.get('verified')
  subscriber = Blogosphere_subscribers.query.filter_by(email=email).first()
  if subscriber:
    subscriber.verified = True
    db.session.commit()
    print("Subscriber {email} has been verified")
    return redirect(url_for('subscriberspage'))
  else:
    print("No subscriber Found")
    return redirect(url_for('subscriberspage'))
# -------------------------------------------------------------------------------------------------------------------
                                   # End of Subscriber Blog Page 
# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
                                   # Denied Subscriber 
# -------------------------------------------------------------------------------------------------------------------
@app.route('/levaze/blogosphere/admin/denied_subscriber', methods = ['POST'])
@nocache
def denied_subscriber():
  if 'admin_logged_in' not in session or not session['admin_logged_in']:
    return redirect(url_for('adminpanel'))
  email = request.form.get('denied')
  subscriber = Blogosphere_subscribers.query.filter_by(email=email).first()
  if subscriber:
    subscriber.verified = False
    db.session.commit()
    print("Subscriber {email} has been denied.")
    return redirect(url_for('subscriberspage'))
  else:
    print("No subscriber Found")
    return redirect(url_for('subscriberspage'))
# -------------------------------------------------------------------------------------------------------------------
                                   # End of Subscriber Blog Page 
# -------------------------------------------------------------------------------------------------------------------

# THis function is used to check the image extension
def allowed_image(image):
    return '.' in image and image.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

#Database section
# THis function is used to give the flash message globally to all html files
@app.context_processor
def global_flash_message():
  messages = get_flashed_messages(with_categories=True)
  return dict(messages=messages)
 
