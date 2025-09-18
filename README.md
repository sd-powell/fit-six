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

---

<a id="structure-plane"></a>

### Structure Plane

#### **User Stories**

| User Story ID | As a/an       | I want to be able to ...                              | So that I can... |
|---------------|---------------|--------------------------------------------------------|------------------|
| **VIEWING & NAVIGATION** |
| 1             | Guest          | Easily navigate the site                              | Find gym merchandise and information quickly |
| 2             | Guest          | View a list of product categories                     | Browse items by type (e.g. apparel, supplements) |
| 3             | Shopper        | View detailed product information                     | Decide if the item meets my needs |
| 4             | Shopper        | View my cart at any time                              | Track what I plan to purchase |
| 5             | Shopper        | See my cart total update in real-time                 | Track spending and avoid surprises at checkout |
| 6             | Shopper        | Access the site easily on mobile                      | Shop from any device conveniently |
| **REGISTRATION & ACCOUNTS** |
| 7             | Guest          | Register for an account                               | Make purchases and view order history |
| 8             | Shopper        | Receive confirmation after registering                | Know that my account is active |
| 9             | Shopper        | Log in and log out securely                           | Access my private information safely |
| 10            | Shopper        | View and update my profile                            | Change delivery address and personal info |
| 11            | Shopper        | View my previous orders                               | Track what I’ve bought and reorder easily |
| 12            | Shopper        | Reset my password                                     | Recover account access if I forget credentials |
| **SEARCHING & FILTERING** |
| 13            | Guest          | Filter products by category or type                   | Quickly narrow down my search |
| 14            | Guest          | Search for a product by name or keyword               | Find specific items faster |
| 15            | Shopper        | Sort products by price, name, or popularity           | Choose the most relevant or affordable options |
| **CART & CHECKOUT** |
| 16            | Shopper        | Add items to my cart                                  | Save products I intend to buy |
| 17            | Shopper        | Adjust quantities or remove items from cart           | Finalise exactly what I want to purchase |
| 18            | Shopper        | Proceed to a secure checkout                          | Buy items with confidence |
| 19            | Guest/Shopper  | Checkout with or without an account                  | Make quick purchases when needed |
| 20            | Shopper        | Enter payment details easily                          | Complete my order smoothly |
| 21            | Shopper        | Receive on-screen and email confirmation              | Ensure the order was successful |
| 22            | Shopper        | Know that my data is protected                        | Trust the site and continue using it |
| **ADMIN & STORE MANAGEMENT** |
| 23            | Admin          | Add new products to the store                         | Keep the shop up to date with new items |
| 24            | Admin          | Edit or update product info                           | Correct mistakes or make improvements |
| 25            | Admin          | Delete a product                                      | Remove items that are no longer for sale |
| 26            | Admin          | Monitor and manage product stock                      | Ensure products don’t oversell |
| 27            | Admin          | View and manage incoming orders                       | Fulfil customer purchases efficiently |
| 28            | Admin          | Access the admin panel securely                       | Manage store operations without public access |
| **EXPERIENCE & COMPLIANCE** |
| 29            | All users      | View accessibility-friendly content                   | Navigate the site with any device or ability |
| 30            | All users      | Receive clear feedback when something goes wrong      | Know how to fix errors and complete actions |
| 31            | All users      | Contact the store via a form                          | Ask questions or report issues |
| 32            | All users      | Read Terms & Conditions and Privacy Policy            | Understand how my data is used and my rights |

> [!NOTE]
> All user stories were manually tested. See [User Story Testing](TESTING.md) for full test results.

<a id="database-schema"></a>

### **Database Schema**

This project uses a **relational database (PostgreSQL)** to manage structured data with integrity, security, and scalability. PostgreSQL was chosen for its seamless integration with Django, robust transaction support, and clear handling of complex relationships — all critical for powering an e-commerce platform with user-specific functionality and secure transactions.

The schema is designed to support the needs of a fully functional online merch store for *Fit Six Gym*, incorporating essential entities such as **users, products, orders, and categories**, while ensuring extensibility for future features like stock management, admin dashboards, and user reviews.

The **core models** include `Product`, `Order`, and `OrderLineItem`, which work together to implement a flexible yet structured checkout process. Products are grouped by `Category`, and users can store default delivery information via an extended `UserProfile` model. A dedicated `ContactForm` model allows users to reach out through the site’s contact page, with backend flags to manage replies.

**To support products with multiple options (e.g. sizes and colours), the schema uses a separate `ProductVariant` model**, which links each variant back to a parent product. This allows a single product (e.g. a hoodie) to support multiple configurations without duplicating product-level data like descriptions or categories.

In line with best practices, the schema follows **normalisation principles** and includes:
- **One-to-many relationships** from orders to line items
- **One-to-many relationships** from products to their variants
- **Foreign key constraints** to maintain referential integrity
- **Timestamps** to track data changes and support future admin analytics
- **Enum fields** for order status (e.g. Pending, Processing, Shipped)

The schema also includes a `status` field on `Order` to reflect real-world business workflows such as *processing, shipped, and complete*, enhancing order tracking and admin oversight.

---

#### **Core Models**

- `User`  
  Authenticates site access and links to an extended profile

- `UserProfile`  
  One-to-one with `User`, storing default delivery info and phone number

- `Category`  
  Groups products by type (e.g. apparel, accessories, supplements)

- `Product`  
  Represents the base product (e.g. "Fit Six Hoodie"), including name, description, category, and image. Links to one or more variants via `ProductVariant`.

- `ProductVariant`  
  Represents a unique purchasable version of a product (e.g. Hoodie - Size M - Black). Includes SKU, price, size, colour, image, and stock.

- `Order`  
  Stores transaction metadata, user info, delivery address, and payment details (e.g. Stripe PID)

- `OrderLineItem`  
  Connects individual **product variants** and quantities to each order

- `ContactForm`  
  Captures user-submitted enquiries and tracks reply status

All models include `created_at` and `updated_at` timestamps for transparency and traceability. This schema supports distinction-level expectations by demonstrating **a realistic, scalable architecture** that can support admin functionality, order management, variant-based product listings, and secure data practices.

The database schema was visualised using [dbdiagram.io](https://dbdiagram.io), leveraging DBML syntax to generate a clear ERD outlining relationships between all core entities.

<details>
<summary>Click here to view the database schema</summary>

![Fit Six Database Schema](documentation/readme/structure_plane/database-schema.webp)

</details>