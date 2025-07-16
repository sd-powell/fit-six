# Fit Six - Train hard. Shop harder.

## Introduction

**Fit Six Store** is a Django-based full-stack e-commerce web application built to serve as the official online merch store for *Fit Six Gym*, a community-focused training space in South Wales. The platform enables gym members and fitness enthusiasts to browse, filter, and securely purchase branded apparel, accessories, nutritional products, and class bundles.

Designed with usability and performance in mind, the site offers a seamless and responsive shopping experience for both members and the wider public. Gym admins can efficiently manage inventory, update product listings, and track orders through a dedicated interface, making the platform a real-world solution for modern fitness retail needs.

This project was developed as part of the Code Institute Full Stack Web Development Diploma. It demonstrates core skills in backend development, user authentication, responsive front-end design, and secure payment integration using Stripe.

Visit the deployed site here: [Fit Six](https://vinyl-crate-ab3f8a285d4e.herokuapp.com/)

![GitHub last commit](https://img.shields.io/github/last-commit/sd-powell/fit-six) ![GitHub repo size](https://img.shields.io/github/repo-size/sd-powell/portfolio_project_3) ![GitHub language count](https://img.shields.io/github/languages/count/sd-powell/fit-six)

---

<a id="ux"></a>

##  User Experience (UX)

<a id="strategy-plane"></a>

### Strategy Plane

#### **Project Goals**

Fit Six Store is a Business to Consumer (B2C) e-commerce platform developed for *Fit Six Gym*, a community-focused training space based in South Wales.

The primary audience for this site includes gym members, fitness enthusiasts, and the wider local community who are looking to purchase branded gym merchandise, nutritional supplements, and exclusive training bundles. The store aims to offer a convenient, centralised hub for accessing high-quality products that support users’ fitness goals, whether they are new to training or seasoned athletes.

As a regular gym-goer myself, I’ve observed the increasing demand for on-brand, quality apparel and fitness products that reflect a gym’s identity and values. A dedicated online store not only helps members represent their gym community with pride but also provides a reliable revenue stream for the gym itself — particularly important in an industry that continues to recover from pandemic-related disruptions.

In recent years, there has been a significant shift toward online retail in the health and fitness sector, driven by a growing emphasis on self-care, at-home workouts, and brand loyalty among gym communities. This project aims to reflect these real-world trends by delivering a practical, user-friendly shopping experience backed by a robust Django-based back end and secure Stripe payment integration.

---

<a id="scope-plane"></a>

### Scope Plane

#### **Feature Planning**

The feature planning process for Fit Six Store involves identifying opportunities to enhance the user experience, streamline store management, and support real-world business needs. Each proposed feature has been scored for both **importance** and **viability** (rated 1–5), helping to prioritise features for the Minimum Viable Product (MVP). 

Features that score highly in both categories will form the foundation of the MVP and must be implemented early. Mid-range features are considered *should-haves* and will be developed once MVP is complete. Features with lower scores are *could-haves*, which may be deferred to future versions of the site if time allows.

User roles are integral to the structure of the application. The site supports three user types:
- **Guest users** – can browse and view products but must register to make purchases.
- **Registered users** – have access to full shopping functionality including order history, account settings, and secure checkout.
- **Admins (Superusers)** – can manage products, inventory, and orders through an internal dashboard. They also retain access to standard user functionality, such as making purchases.

This tiered approach allows for scalable functionality, supporting both everyday customer use and efficient business operations from a single application.

## Feature Planning Table

| User Type       | Feature                                      | Importance | Viability |  | Delivered |
|-----------------|----------------------------------------------|:----------:|:---------:|:--:|:---------:|
| All             | User roles (Guest, User, Admin)              | 5          | 5         | MVP |  |
| Guest           | Register for an account                      | 5          | 5         | MVP |  |
| User            | Login / Logout functionality                 | 5          | 5         | MVP |  |
| User & Admin    | Account dashboard/profile                    | 5          | 5         | MVP |  |
| User            | Password reset/recovery                      | 5          | 5         | MVP |  |
| Guest           | Social media login                           | 2          | 4         |     |   |
| All             | Search and filter products                   | 5          | 5         | MVP |  |
| All             | Browse product detail page                   | 5          | 5         | MVP |  |
| User            | Add to cart                                  | 5          | 5         | MVP |  |
| Guest           | Guest checkout                               | 3          | 4         |     |  |
| All             | Stripe payment integration                   | 5          | 5         | MVP |  |
| All             | Order confirmation (on-screen & email)       | 5          | 5         | MVP |  |
| User            | View order history                           | 4          | 5         | MVP |  |
| Admin           | Add new product (Create)                     | 5          | 5         | MVP |  |
| Admin           | Edit/update product                          | 5          | 5         | MVP |  |
| Admin           | Delete product                               | 5          | 5         | MVP |  |
| Admin           | Manage product stock levels                  | 4          | 4         | MVP |  |
| Admin           | View and manage orders                       | 4          | 4         | MVP |  |
| All             | Form validation with inline error feedback   | 5          | 5         | MVP |  |
| All             | Terms & Conditions page                      | 3          | 5         |     |  |
| All             | Privacy Policy page                          | 3          | 5         |     |  |
| All             | Delivery & Returns info page                 | 3          | 5         |     |  |
| All             | Contact form                                 | 3          | 4         |     |  |
| All             | Social media links                           | 3          | 5         |     |  |
| User            | Wishlist                                     | 3          | 3         |     |   |
| User            | Write product reviews                        | 3          | 3         |     |   |
| All             | Read product reviews                         | 3          | 3         |     |   |
| All             | Newsletter signup                            | 2          | 3         |     |   |
| Admin           | Discount vouchers / coupon codes             | 2          | 2         |     |   |
| All             | Blog / Articles section                      | 1          | 2         |     |   |