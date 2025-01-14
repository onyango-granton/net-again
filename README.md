# NetFix: Home Services Marketplace

Welcome to **NetFix**, a web-based marketplace for home services. This platform allows companies to provide a variety of services while enabling customers to request them with ease. Built using Django, the project ensures a smooth and user-friendly experience for all.

---

## **Features**

### **User Roles**

1. **Customer**:
   - Register with email, username, date of birth, and password.
   - Login to manage service requests.
   - View profile, including past requested services.

2. **Company**:
   - Register with email, usernamMachinese, field of work, and password.
   - Create and manage services based on their field of expertise.
   - View profile, including all provided services.

### **Services**

- Categories include:
  - Air Conditioner
  - All In One
  - Carpentry
  - Electricity
  - Gardening
  - Home Machines
  - Housekeeping
  - Interior Design
  - Locks
  - Painting
  - Plumbing
  - Water Heaters

- All services include:
  - Name, description, field, price per hour, and creation date.
  - Display of the company providing the service.

### **Browsing Options**

- View most requested services.
- Browse all services (newest first).
- Filter services by category.

### **Service Requests**

- Customers can request services by providing:
  - Address for the service.
  - Required service time in hours.
- View calculated cost, request date, and provider details in their profile.

---

## **Installation**

### **Requirements**

- Python 3.8+
- Django 3.1.14
- A database supported by Django (e.g., SQLite, PostgreSQL).

### **Setup**

1. Clone the repository:
   ```bash
   git clone https://learn.zone01kisumu.ke/git/gonyango/netfix.git
   cd netfix
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## **Usage**

1. Register as a Customer or a Company.
2. Login to access features specific to your role.
3. Companies can create and manage services.
4. Customers can browse and request services.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Contributing**

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. Please ensure your code adheres to the project guidelines.

---

## **Contact**

For questions or support, please reach out to **Granton Onyango** at:
1. [LinkedIn](https://www.linkedin.com/in/granton-onyango-298ba6213/)
2. [Githun](https://github.com/onyango-granton)

---

Thank you for exploring NetFix! We hope you find it helpful and inspiring.

