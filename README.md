# GT Movies Store

A full-stack Django web application for an online movie store with e-commerce functionality.

## Features

- User registration and authentication
- Movie catalog with search functionality
- Shopping cart system
- Movie reviews and ratings
- Order management
- Responsive design for all devices
- Admin panel for content management

## Technology Stack

- **Backend**: Django 5, Python
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd moviesstore
```

2. Install Django (if not already installed):
```bash
pip install django
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

- Browse movies in the catalog
- Search for specific movies by title
- Register an account to add reviews and make purchases
- Add movies to your cart and proceed to checkout
- View your order history in your account

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin` to manage:
- Movies
- Users
- Reviews
- Orders

## Project Structure

```
moviesstore/
├── accounts/          # User authentication and account management
├── cart/             # Shopping cart functionality
├── home/             # Home page and about page
├── movies/           # Movie catalog and reviews
├── moviesstore/      # Main project settings and configuration
├── media/            # User uploaded files (movie images)
├── manage.py         # Django management script
└── db.sqlite3        # SQLite database
```

## Contributing

This is a portfolio project. Feel free to fork and modify for your own learning purposes.

## License

This project is for educational purposes.
