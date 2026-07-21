# Lotus Design — Full Stack Website

A full-stack website for **Lotus Design**, a graphic design service business in Mainpur, Jamalpur, Bangladesh. Built with Python (Flask + SQLite) on the backend and HTML/CSS/JS on the frontend.

## Features

- **Homepage** — hero section, services list (Logo, Business Card, Banner, Poster, Social Media Design), about section, and a contact/order form.
- **Order form** — visitors fill in their details, the order is saved to a SQLite database, and they're redirected to WhatsApp with a pre-filled message to send directly to Lotus Design (+8801729335788).
- **Admin dashboard** (`/admin`) — password-protected page to view all orders, update their status (New / In Progress / Completed), and delete old ones.
- Fully responsive design (mobile + desktop), orange/black brand theme.

## Project Structure

```
lotus_design/
├── app.py                  # Flask backend (routes, database models)
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html          # Main website
│   ├── admin_login.html    # Admin login page
│   └── admin.html          # Admin dashboard
└── static/
    ├── css/style.css       # All styling
    └── js/script.js        # Mobile menu + small interactions
```

## How to Run Locally

1. **Install Python** (3.9+) if you don't have it already.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. Open your browser to **http://localhost:5000**

The SQLite database file (`lotus_design.db`) is created automatically the first time you run the app.

## Admin Panel

- URL: `http://localhost:5000/admin`
- Default username: `admin`
- Default password: `lotus123`

**⚠️ Important:** Change the default admin password before putting this online. You can either:
- Edit `ADMIN_USERNAME` / `ADMIN_PASSWORD` directly in `app.py`, or
- Set them as environment variables before running:
  ```bash
  export ADMIN_USERNAME=your_username
  export ADMIN_PASSWORD=your_strong_password
  python app.py
  ```

Also change `app.secret_key` in `app.py` (or set the `SECRET_KEY` environment variable) to a random secret string before deploying.

## Deploying Online (e.g. Render, Railway, PythonAnywhere)

1. Push this folder to a GitHub repository.
2. On Render (or similar), create a new **Web Service** from the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app` (add `gunicorn` to `requirements.txt` first)
5. Set environment variables `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` in the hosting dashboard.

Note: on most free hosting tiers, the SQLite file resets when the service restarts/redeploys, since the filesystem isn't persistent. For a production business site, consider upgrading to a hosted database (like Render's free PostgreSQL) once you have real traffic.

## Business Info (already configured in the site)

- **Business:** Lotus Design
- **Address:** Mainpur, Jamalpur, Bangladesh
- **WhatsApp / Mobile:** +8801729335788
- **Email:** riazlotus01729335788@gmail.com

To change any of this later, edit the `BUSINESS` dictionary near the top of `app.py`.

## Customizing Services & Prices

Services are defined in the `SERVICES` list in `app.py` — edit the name, icon (emoji), price, and description for each one, or add new services by adding new entries to the list.
