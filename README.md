# 🌐 BlogoSphere

A modern, feature-rich blogging platform built with Flask that combines curated content with user-generated blogs. BlogoSphere offers a seamless experience for readers and writers alike, with an intuitive admin panel for content management.

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

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Email**: SMTP integration for notifications
- **Libraries**:
  - Swiper.js for carousels
  - Locomotive Scroll for smooth scrolling
  - Font Awesome for icons

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Gmail account for SMTP (or modify email configuration)

## 🚀 Installation

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
   pip install flask flask-sqlalchemy
   ```

5. **Run the application**

   ```bash
   python run.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:5000`

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

### Email Setup

Update SMTP credentials in `run.py`:

```python
server.login('your-email@gmail.com', 'your-app-password')
```

**Note**: Use Gmail App Password for better security

### Admin Credentials

Default admin users (modify in `run.py`):

- Names: yash, shashank, diti
- Emails: Configured in admin login route
- Password: group9 (change in production!)

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

## 🚧 Known Limitations

- Email credentials hardcoded (move to environment variables)
- SQLite database (consider PostgreSQL for production)
- No password reset functionality
- Image upload limited to JPG/PNG/JPEG
- Development server (use WSGI server for production)

## 🔮 Future Enhancements

- [ ] AI-powered content suggestions
- [ ] Advanced search with filters
- [ ] User profile pages
- [ ] Comment system
- [ ] Social media sharing
- [ ] Email newsletter system
- [ ] Blog analytics dashboard
- [ ] Multi-language support
- [ ] SEO optimization
- [ ] Mobile app

## 👥 Team

**Group 9**

- Shashank
- Yash
- Diti

## 📧 Contact

- Email: blogosphere009@gmail.com
- Location: Mumbai, India
- Phone: +91 7977305279 / +91 8691907200

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Contributors and testers
- All blog readers and writers

---

**Made with ❤️ by Group 9**

_Last Updated: January 11, 2026_
