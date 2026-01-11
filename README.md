# 🌐 BlogoSphere

> **A modern, feature-rich blogging platform built with Flask - Now Live!**

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://www.blogosphere.me)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1.0-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-Educational-green)](LICENSE)

**🚀 Live Site:** [https://www.blogosphere.me](https://www.blogosphere.me)

A production-ready blogging platform that combines curated content with user-generated blogs. BlogoSphere offers a seamless experience for readers and writers alike, featuring an intuitive admin panel, email notifications via SendGrid, and secure deployment on Render.com with a custom domain.

## ✨ Features

### 🎯 Core Functionality

- **User Subscription System** - Email-based registration with auto-generated passwords
- **Blog Publishing** - Users can submit blogs with images and rich content
- **Search Functionality** - Find blogs by title or keywords
- **Category System** - Organized content across 5 major categories
- **Admin Panel** - Secure OTP-based authentication for content moderation

### 📚 Content Categories

- **Technology** - AI, Quantum Computing, Healthcare Tech, Voice Technology
- **Astronomy** - Black Holes, Exoplanets, Mars, Galaxies, Comets, Auroras
- **Business & Finance** - Investment, Budgeting, Financial Planning
- **Sports** - Cricket, Esports, Iconic Moments, Indian Games
- **Food** - Vegan Cuisine, Culinary Arts, Food Photography, Innovations

### 🔐 Security Features

- Session-based authentication
- OTP verification for admin access
- Password auto-generation and email delivery
- Cache prevention on sensitive pages
- Image validation (PNG, JPG, JPEG only)

### 🎨 User Experience

- Dark/Light theme toggle
- Responsive card-based design
- Smooth scroll animations
- Flash messaging for user feedback
- Trending blog ticker

## 🛠️ Tech Stack

### Backend
- **Flask 3.1.0** - Python web framework
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations
- **SQLite** - Development database
- **SendGrid API** - Email delivery service (100 emails/day free)

### Frontend
- **HTML5, CSS3, JavaScript** - Core web technologies
- **Swiper.js** - Touch-enabled carousels
- **Locomotive Scroll** - Smooth scrolling animations
- **Font Awesome** - Icon library

### Deployment & Infrastructure
- **Render.com** - Cloud hosting platform (Free tier)
- **Gunicorn 23.0.0** - Production WSGI server
- **Namecheap** - Domain registration (.me domain via GitHub Student Pack)
- **Let's Encrypt** - Free SSL/TLS certificates
- **Git/GitHub** - Version control

### Development Tools
- **Python 3.13** - Production runtime
- **Virtual Environment** - Dependency isolation
- **GitHub Actions Ready** - CI/CD integration support

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Gmail account for SMTP (or modify email configuration)

## 🚀 Installation

### Local Development

1. **Clone the repository**

   ```bash
   git clone https://github.com/shashankpc7746/BlogoSphere.git
   cd BlogoSphere
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**

   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (Optional for local development)

   Create a `.env` file:
   ```env
   SECRET_KEY=your-secret-key-here
   SENDGRID_API_KEY=your-sendgrid-api-key
   SENDER_EMAIL=your-email@domain.com
   ```

6. **Run the application**

   ```bash
   python run.py
   ```

7. **Access the application**
   - Open your browser: `http://127.0.0.1:5000`

### Production Deployment (Render.com)

Our live deployment setup:

1. **Connect GitHub Repository** to Render
2. **Configure Build Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -c gunicorn_config.py run:app`
3. **Set Environment Variables:**
   - `SECRET_KEY` - Flask secret key
   - `SENDGRID_API_KEY` - SendGrid API key for emails
   - `SENDER_EMAIL` - Verified sender email address
4. **Custom Domain Setup:**
   - Add CNAME records in domain DNS
   - Configure custom domain in Render dashboard
   - SSL certificates auto-generated via Let's Encrypt

📖 **Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

## 📁 Project Structure

```
BlogoSphere/
├── run.py                      # Main application file
├── instance/
│   └── Blogosphere.db         # SQLite database
├── static/
│   ├── *.css                  # Stylesheets
│   ├── *.js                   # JavaScript files
│   ├── images/                # Blog images by category
│   └── upload_images/         # User-uploaded images
└── templates/
    ├── layout.html            # Base template
    ├── main.html              # Homepage
    ├── blogs.html             # Blog listing
    ├── content.html           # Blog submission form
    ├── admin/                 # Admin panel templates
    └── blogs/                 # Category-specific blogs
```

## 🗄️ Database Schema

### Tables

1. **blogosphere_subscribers**

   - User registration and authentication
   - Fields: id, name, email, password, verified, date

2. **blogosphere_blogs**

   - User-submitted blog content
   - Fields: id, name, email, title, content, date

3. **blogosphere_adminpanel**
   - Admin access logging
   - Fields: id, name, email, password, check, date

## 🔑 Configuration

### Email Setup (SendGrid)

1. **Create SendGrid Account** (100 emails/day free)
2. **Generate API Key** in SendGrid dashboard
3. **Verify Sender Email** in SendGrid settings
4. **Set Environment Variables:**
   ```env
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxx
   SENDER_EMAIL=your-verified-email@gmail.com
   ```

### Admin Credentials

Default admin users (configured in `run.py`):

- **Names:** yash, shashank, diti
- **Emails:** Configured in admin login route
- **Password:** group9 *(Change in production!)*

### Security Best Practices

- ✅ Use environment variables for sensitive data
- ✅ Enable 2FA on SendGrid account
- ✅ Rotate API keys regularly
- ✅ Use strong admin passwords
- ✅ Keep dependencies updated

## 📖 Usage

### For Users

1. **Subscribe** - Enter name and email on homepage
2. **Receive Password** - Check email for auto-generated password
3. **Browse Blogs** - Explore pre-written and user-submitted content
4. **Submit Blog** - Use "Add Blog" with your credentials
5. **Upload Image** - Include cover image with your blog

### For Admins

1. Navigate to admin panel URL
2. Enter admin credentials
3. Verify OTP sent to email
4. Manage subscribers and blogs
5. Verify/deny users, delete content

## 🎨 Customization

### Theme Colors

Modify theme colors in `static/style.css`:

```css
:root {
  --primary-color: #your-color;
  --secondary-color: #your-color;
}
```

### Categories

Add new categories by:

1. Creating route in `run.py`
2. Adding template in `templates/Category/`
3. Updating navigation in `layout.html`

## 🚧 Production Status

### ✅ Completed Features

- [x] **Production Deployment** - Live on Render.com
- [x] **Custom Domain** - www.blogosphere.me configured
- [x] **SSL/HTTPS** - Secured with Let's Encrypt certificates
- [x] **Email Service** - SendGrid integration for notifications
- [x] **Environment Variables** - Secure configuration management
- [x] **Production Server** - Gunicorn with optimized settings
- [x] **Dark Theme** - Set as default with toggle option
- [x] **Responsive Design** - Mobile and desktop optimized
- [x] **Error Handling** - Graceful failures with user feedback
- [x] **Database Persistence** - SQLite with proper migrations

### ⚠️ Known Limitations

- **Free Tier Constraints:**
  - App sleeps after 15 minutes of inactivity (50s cold start)
  - 100 emails per day limit (SendGrid free tier)
  - SQLite database (resets on redeploy)
- **Image Storage:** User uploads stored on Render disk (not persistent across deploys)
- **Rate Limiting:** Not implemented (consider for production scale)

### 🔮 Future Enhancements

- [ ] Upgrade to PostgreSQL for persistent storage
- [ ] Implement cloud storage (Cloudinary) for images
- [ ] Add caching layer (Redis) for performance
- [ ] Rate limiting and DDoS protection
- [ ] User profile pages with edit capabilities
- [ ] Comment system with moderation
- [ ] Social media sharing integration
- [ ] Blog analytics dashboard
- [ ] Advanced search with filters
- [ ] Newsletter automation
- [ ] Mobile app (React Native)

## 👥 Team

**Group 9**

- **Shashank** - Lead Developer & Deployment Engineer
- **Yash** - Backend Developer & Database Designer
- **Diti** - Frontend Developer & UI/UX Designer

## 📧 Contact

- **Website:** [www.blogosphere.me](https://www.blogosphere.me)
- **Email:** blogosphere009@gmail.com
- **Location:** Mumbai, India
- **GitHub:** [github.com/shashankpc7746/BlogoSphere](https://github.com/shashankpc7746/BlogoSphere)

## 🎓 Acknowledgments

This project was developed as part of our web development coursework and is deployed using:

- **GitHub Student Developer Pack** - Free .me domain (1 year)
- **Render.com Free Tier** - Cloud hosting
- **SendGrid Free Tier** - Email delivery service
- **Let's Encrypt** - Free SSL certificates

Special thanks to:
- Flask community for excellent documentation
- Render.com support team
- SendGrid developer resources
- Stack Overflow community

## 📄 License

This project is open source and available for educational purposes.

## 🏆 Project Milestones

- **Jan 2026** - Initial development and local testing
- **Jan 11, 2026** - Production deployment completed
  - ✅ Deployed to Render.com
  - ✅ Custom domain configured (blogosphere.me)
  - ✅ SSL certificates issued
  - ✅ Email service integrated (SendGrid)
  - ✅ Dark theme optimization
  - ✅ Production-ready configuration

---

**Made with ❤️ by Group 9**

*"Blogging made simple, deployment made easy."*

**Last Updated:** January 11, 2026  
**Version:** 2.0.0 (Production Release)  
**Status:** 🟢 Live and Running
