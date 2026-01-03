# Jikoni Journals 🍳🌍

**Jikoni Journals** is a culinary tourism platform that connects food lovers with immersive local culinary experiences. Users can explore curated meal plans, book culinary tours, and discover the rich history behind local cuisines.

## 🚀 Features

*   **Culinary Tours:** Book guided food tours with local experts.
*   **Meal Plans:** Discover and subscribe to international meal plans.
*   **Interactive Map:** Explore food destinations visually.
*   **Payments:** Secure payments via **Stripe** (Credit Card) and **M-Pesa** (Mobile Money).
*   **Splash Screen:** Engaging animated entrance.

## 🛠️ Tech Stack

*   **Backend:** Django (Python)
*   **Frontend:** HTML, CSS, JavaScript (Two.js for animations)
*   **Database:** SQLite (Development)
*   **Payments:** Stripe API, Safaricom Daraja API (M-Pesa)

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/martndere/Jikoni-Journals.git
    cd Jikoni-Journals
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the server:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```