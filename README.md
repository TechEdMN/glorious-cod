# AstroydsAI Website

A modern, sleek static website for AstroydsAI - an AI company dedicated to building intelligent models that empower humanity and drive innovation.

## 🚀 Features

- **Modern Design**: Sleek, professional design with gradient accents and smooth animations
- **Responsive Layout**: Fully responsive design that works on all screen sizes
- **Interactive Animations**: 
  - Particle system with connecting lines
  - Scroll-triggered reveal animations
  - Smooth fade-in effects
  - Floating icon animations
  - Interactive cursor effects
  - Button ripple effects
- **Multiple Pages**:
  - Home (index.html) - Hero section, features, stats, services preview
  - About (about.html) - Mission, vision, journey timeline, team
  - Services (services.html) - Detailed service offerings and process
  - Contact (contact.html) - Contact form with validation, FAQ section
- **Advanced Styling**:
  - Custom gradient text effects
  - Glassmorphism design elements
  - Animated starfield background
  - Hover effects and transitions
  - Custom scrollbar
- **Interactive Elements**:
  - Working contact form with validation
  - Mobile-responsive navigation menu
  - Smooth scroll navigation
  - Counter animations for statistics
  - Form validation with success/error notifications

## 🛠️ Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Custom styles with advanced animations
- **TailwindCSS** - Utility-first CSS framework (via CDN)
- **JavaScript (Vanilla)** - Interactive features and animations
- **Font Awesome** - Icons (via CDN)
- **Google Fonts** - Inter and Space Grotesk fonts

## 📁 File Structure

```
.
├── index.html          # Homepage
├── about.html          # About page
├── services.html       # Services page
├── contact.html        # Contact page
├── styles.css          # Custom CSS styles and animations
├── script.js           # JavaScript for interactivity
└── README.md          # This file
```

## 🎨 Design Elements

### Color Scheme
- Primary Gradient: Purple (#667eea) to Purple (#764ba2)
- Background: Dark gray (#111827)
- Text: White with various opacity levels
- Accents: Purple and blue gradients

### Typography
- Headings: Space Grotesk (Google Font)
- Body Text: Inter (Google Font)

### Key Animations
1. **Particle System**: Interactive particle network in hero section
2. **Reveal on Scroll**: Elements fade in as you scroll
3. **Counter Animation**: Statistics count up when visible
4. **Hover Effects**: Cards lift and glow on hover
5. **Background Stars**: Animated twinkling starfield

## 🌐 Pages Overview

### Home (index.html)
- Hero section with animated particle background
- Features showcase with 3 main benefits
- Statistics counter (models, clients, accuracy, countries)
- Services preview with 4 key offerings
- Call-to-action section

### About (about.html)
- Mission and Vision statements
- Company journey timeline (2020-2024)
- Core values (6 principles)
- Team member profiles
- Join us CTA

### Services (services.html)
- 6 detailed service offerings:
  - Natural Language Processing
  - Computer Vision
  - Predictive Analytics
  - Custom AI Solutions
  - Recommendation Systems
  - Deep Learning
- Industries served (8 sectors)
- 4-step process overview

### Contact (contact.html)
- Contact information (address, email, phone, hours)
- Social media links
- Working contact form with validation
- FAQ section (5 common questions)
- Office location placeholder

## 🚀 Getting Started

### Option 1: Direct Opening
Simply open `index.html` in a modern web browser.

### Option 2: Local Server
For best results (especially to avoid CORS issues with external resources), use a local web server:

```bash
# Using Python 3
python -m http.server 8080

# Using Node.js (if you have http-server installed)
npx http-server -p 8080

# Using PHP
php -S localhost:8080
```

Then navigate to `http://localhost:8080` in your browser.

## ✨ Interactive Features

### Contact Form
The contact form includes:
- Client-side validation
- Required field checking
- Email format validation
- Success/error notifications
- Form reset after successful submission

### Navigation
- Fixed header that becomes opaque on scroll
- Active page highlighting
- Mobile hamburger menu
- Smooth scroll to sections

### Animations
- Elements reveal on scroll
- Statistics counter animation
- Particle system in hero section
- Custom cursor effects (desktop only)
- Button ripple effects
- Card hover animations

## 📱 Responsive Design

The website is fully responsive and optimized for:
- Desktop (1920px and above)
- Laptop (1024px - 1919px)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🎯 Browser Support

Tested and working on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## 📝 Customization

To customize the website:

1. **Colors**: Edit CSS variables in `styles.css`:
   ```css
   :root {
       --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
       /* Add more custom variables */
   }
   ```

2. **Content**: Update HTML files with your own text and information

3. **Images**: Add your own images and update references in HTML

4. **Animations**: Modify animation parameters in `styles.css` and `script.js`

## 🔒 Form Handling

Note: The contact form currently uses client-side validation only. For production use, you'll need to:
1. Add server-side form processing
2. Implement email sending functionality
3. Add CAPTCHA for spam protection
4. Store submissions in a database

## 📄 License

This is a custom-built website for AstroydsAI. All rights reserved © 2024.

## 🤝 Contributing

For suggestions or improvements, please contact the development team.

---

Built with ❤️ for AstroydsAI
