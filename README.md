# Fit Six - Train hard. Shop harder.

## Introduction

**Fit Six Store** is a Django-based full-stack e-commerce web application built to serve as the official online merch store for *Fit Six Gym*, a community-focused training space in South Wales. The platform enables gym members and fitness enthusiasts to browse, filter, and securely purchase branded apparel, accessories, nutritional products, and class bundles.

Designed with usability and performance in mind, the site offers a seamless, responsive shopping experience for both members and the wider public. Gym admins can efficiently manage inventory, update product listings, and track orders through a dedicated interface, making the platform a real-world solution for modern fitness retail needs.

This project is the fourth milestone in the Code Institute Full Stack Web Development Diploma and demonstrates core skills in backend development, user authentication, responsive front-end design, and secure payment integration using Stripe.

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

#### Primary Target Audiences
- Gym members (existing)
- Fitness enthusiasts and athletes
- Local community and casual supporters

#### Business Goals
- Provide a scalable revenue stream for the gym
- Build brand loyalty through merch and bundles
- Offer a centralised platform for product management

#### User Goals
- Browse and buy branded Fit Six products online
- Access exclusive training bundles and offers
- Enjoy a smooth, secure, responsive shopping experience

> **Success Criteria:**  
> This project will be considered successful if it delivers a seamless, intuitive user experience, a secure and responsive e-commerce flow, and a professional administrative interface that enables Fit Six Gym to manage orders and products with ease.

---

<a id="scope-plane"></a>

### Scope Plane

#### **Feature Planning**

The feature planning process for Fit Six Store involves identifying opportunities to enhance the user experience, streamline store management, and support real-world business needs. Each proposed feature has been scored for both **importance** and **viability** (rated 1–5), helping to prioritise features for the Minimum Viable Product (MVP). 

#### Prioritisation Strategy

Features that score highly in both categories will form the foundation of the MVP and must be implemented early. Mid-range features are considered *should-haves* and will be developed once MVP is complete. Features with lower scores are *could-haves*, which may be deferred to future versions of the site if time allows.

#### User Roles

User roles are integral to the structure of the application. The site supports three user types:
- **Guest users** – can browse and view products but must register to make purchases.
- **Registered users** – have access to full shopping functionality including order history, account settings, and secure checkout.
- **Admins (Superusers)** – can manage products, inventory, and orders through an internal dashboard. They also retain access to standard user functionality, such as making purchases.

This tiered approach allows for scalable functionality, supporting both everyday customer use and efficient business operations from a single application.

## Feature Planning Table

The following table outlines all planned features across different user roles, with scores based on importance to user/business goals and technical viability. Delivered features are marked as ✅.

| User Type       | Feature                                      | Importance | Viability | MVP | Delivered |
|-----------------|----------------------------------------------|:----------:|:---------:|:--:|:---------:|
| All             | User roles (Guest, User, Admin)              | 5          | 5         | MVP |  |
| Guest           | Register for an account                      | 5          | 5         | MVP | ✅ |
| User            | Login / Logout functionality                 | 5          | 5         | MVP | ✅ |
| User & Admin    | Account dashboard/profile                    | 5          | 5         | MVP | ✅ |
| User            | Password reset/recovery                      | 5          | 5         | MVP | ✅ |
| Guest           | Social media login                           | 2          | 4         |     |   |
| All             | Search and filter products                   | 5          | 5         | MVP | ✅ |
| All             | Browse product detail page                   | 5          | 5         | MVP | ✅ |
| User            | Add to cart                                  | 5          | 5         | MVP | ✅ |
| Guest           | Guest checkout                               | 3          | 4         |     |  |
| All             | Stripe payment integration                   | 5          | 5         | MVP | ✅ |
| All             | Order confirmation (on-screen & email)       | 5          | 5         | MVP | ✅ |
| User            | View order history                           | 4          | 5         | MVP | ✅ |
| Admin           | Add new product (Create)                     | 5          | 5         | MVP |  |
| Admin           | Edit/update product                          | 5          | 5         | MVP |  |
| Admin           | Delete product                               | 5          | 5         | MVP | ✅ |
| Admin           | Manage product stock levels                  | 4          | 4         | MVP |  |
| Admin           | View and manage orders                       | 4          | 4         | MVP |  |
| All             | Form validation with inline error feedback   | 5          | 5         | MVP |  |
| All             | Terms & Conditions page                      | 3          | 5         |     |  |
| All             | Privacy Policy page                          | 3          | 5         |     |  |
| All             | Delivery & Returns info page                 | 3          | 5         |     |  |
| All             | Contact form                                 | 3          | 4         |     |  |
| All             | Social media links                           | 3          | 5         |     | ✅ |
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

To support products with multiple options (e.g. sizes and colours), the schema uses a separate `ProductVariant` model, which links each variant back to a parent product. This allows a single product (e.g. a hoodie) to support multiple configurations without duplicating product-level data like descriptions or categories.

In line with best practices, the schema follows **normalisation principles** and includes:

- **One-to-many relationships** from orders to line items  
- **One-to-many relationships** from products to their variants  
- **Optional one-to-many relationship** from user profiles to newsletter signups  
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

- `NewsletterSignup`  
  Stores email addresses submitted through the newsletter form. Optionally links to a `UserProfile` for logged-in users. Includes signup timestamp and ensures email uniqueness.

All models include `created_at` and/or `updated_at` timestamps for transparency and traceability. This schema supports distinction-level expectations by demonstrating **a realistic, scalable architecture** that can support admin functionality, order management, variant-based product listings, newsletter signups, and secure data practices.

The database schema was visualised using [dbdiagram.io](https://dbdiagram.io), leveraging DBML syntax to generate a clear ERD outlining relationships between all core entities.

<details>
<summary>Click here to view the database schema</summary>

![Fit Six Database Schema](documentation/readme/surface_plane/database-schema.webp)

</details>


<a id="skeleton-plane"></a>

### Skeleton Plane

<a id="wireframes"></a>

#### **Wireframes**

Initial wireframes were created using [Balsamiq](https://balsamiq.com/) to plan the layout, information hierarchy, and user flow of the **Fit Six Store** e-commerce platform. Wireframes were developed for **mobile, tablet, and desktop** breakpoints to ensure a consistent and responsive shopping experience across all modern devices.

The wireframing process focused on key customer-facing views including the **homepage**, **product listing**, **product detail**, **shopping bag**, and **checkout flow**. Additional views were sketched for the **account dashboard** and **order confirmation**, reflecting the expected user journey for both guests and registered users.

These wireframes served as the **visual foundation** for layout decisions throughout development, guiding the positioning of navigation, filters, product cards, and form inputs. A **mobile-first** approach was taken from the outset, ensuring accessibility and usability on smaller screens.

> [!NOTE]  
> Admin-related views were not wireframed, as Django’s built-in admin panel was used to manage products and orders. Similarly, individual form layouts (e.g. profile edit, checkout form) were rendered using Django Crispy Forms to ensure consistent spacing and alignment across viewports.

<br>
<hr>

<a id="mobile-frames"></a>

#### **Mobile Wireframes - User Flow**

<details>
<summary> Click here to see the User Mobile Wireframes </summary>

#### **Core Pages**

| Base Template | Home page | Sign up page |
| :-----------: | :-------: | :-----------: |
| ![Base Template](documentation/readme/skeleton_plane/wireframe-mobile-base.webp) | ![Home](documentation/readme/skeleton_plane/wireframe-mobile-home.webp) | ![Sign up](documentation/readme/skeleton_plane/wireframe-mobile-signup.webp) |

#### **Authentication**

|  Login page | Logout page | Profile page |
| :---------: | :---------: | :----------: |
| ![Login](documentation/readme/skeleton_plane/wireframe-mobile-signin.webp) | ![Logout](documentation/readme/skeleton_plane/wireframe-mobile-logout.webp) | ![Profile](documentation/readme/skeleton_plane/wireframe-mobile-profile.webp) |

#### **Shopping Flow**

| Bag page (Empty Bag) | Bag page | Checkout page |
| :------------------: | :------: | :-----------: |
| ![Bag Empty](documentation/readme/skeleton_plane/wireframe-mobile-bag-empty.webp) | ![Bag](documentation/readme/skeleton_plane/wireframe-mobile-bag.webp) | ![Checkout](documentation/readme/skeleton_plane/wireframe-mobile-checkout.webp) |

| Product page | Product Detail | Checkout Success |
|:------------:|:--------------:|:----------------:|
| ![Product Page](documentation/readme/skeleton_plane/wireframe-mobile-product.webp) | ![Product Detail](documentation/readme/skeleton_plane/wireframe-mobile-product-detail.webp) | ![Checkout Success](documentation/readme/skeleton_plane/wireframe-mobile-checkout-success.webp) |

#### **Content & Legal Pages**

| 404 Error | Privacy Policy | Terms & Conditions |
|:---------:|:--------------:|:------------------:|
| ![404 Error](documentation/readme/skeleton_plane/wireframe-mobile-404-error.webp) | ![Privacy Policy](documentation/readme/skeleton_plane/wireframe-mobile-privacy-policy.webp) | ![Terms](documentation/readme/skeleton_plane/wireframe-mobile-terms.webp) |

| Contact Us | Returns & Exchanges | Shipping Policy |
|:----------:|:-------------------:|:----------------:|
| ![Contact Us](documentation/readme/skeleton_plane/wireframe-mobile-contact-us.webp) | ![Returns](documentation/readme/skeleton_plane/wireframe-mobile-returns.webp) | ![Shipping](documentation/readme/skeleton_plane/wireframe-mobile-shipping.webp) |

#### **UI Feedback**

| Toast Message |
|:-------------:|
| ![Toast Message](documentation/readme/skeleton_plane/wireframe-mobile-toast-message.webp) |

</details>

#### **Mobile Wireframes - Admin Flow**

<details>
<summary>Click to view Admin Mobile Wireframes</summary>

- Add Product

![Add Product](documentation/readme/skeleton_plane/wireframe-mobile-add-product.webp)

- Edit Product

![Edit Product](documentation/readme/skeleton_plane/wireframe-mobile-edit-product.webp)

- Product Management

![Product Management](documentation/readme/skeleton_plane/wireframe-mobile-admin-dashboard.webp)

</details>

<br>
<hr>

<a id="desktop-frames"></a>

#### **Desktop Wireframes - User Flow**

<details>
<summary> Click here to see the User Desktop Wireframes </summary>

#### **Core Pages**

- Base Template

![Base Template](documentation/readme/skeleton_plane/wireframe-desktop-base.webp)

- Home page

![Home](documentation/readme/skeleton_plane/wireframe-desktop-home.webp)

- Sign up page

![Sign up](documentation/readme/skeleton_plane/wireframe-desktop-signup.webp)

#### **Authentication**

- Login page

![Login](documentation/readme/skeleton_plane/wireframe-desktop-signin.webp)

- Logout page

![Logout](documentation/readme/skeleton_plane/wireframe-desktop-logout.webp)

- Profile page

![Profile](documentation/readme/skeleton_plane/wireframe-desktop-profile.webp)

#### **Shopping Flow**

- Bag page (Empty Bag)

![Bag Empty](documentation/readme/skeleton_plane/wireframe-desktop-bag-empty.webp)

- Bag page

![Bag](documentation/readme/skeleton_plane/wireframe-desktop-bag.webp)

- Checkout page
![Checkout](documentation/readme/skeleton_plane/wireframe-desktop-checkout.webp)

- Product page

![Product Page](documentation/readme/skeleton_plane/wireframe-desktop-product.webp)

- Product Detail

![Product Detail](documentation/readme/skeleton_plane/wireframe-desktop-product-detail.webp)

- Checkout Success

![Checkout Success](documentation/readme/skeleton_plane/wireframe-desktop-checkout-success.webp)

#### **Content & Legal Pages**

- 404 Error

![404 Error](documentation/readme/skeleton_plane/wireframe-desktop-404-error.webp)

- Privacy Policy

![Privacy Policy](documentation/readme/skeleton_plane/wireframe-desktop-privacy-policy.webp)

- Terms & Conditions

![Terms](documentation/readme/skeleton_plane/wireframe-desktop-terms.webp)

- Contact Us

![Contact Us](documentation/readme/skeleton_plane/wireframe-desktop-contact-us.webp)

- Returns & Exchanges

![Returns](documentation/readme/skeleton_plane/wireframe-desktop-returns.webp)

- Shipping Policy

![Shipping](documentation/readme/skeleton_plane/wireframe-desktop-shipping.webp) |

#### **UI Feedback**

- Toast Message

![Toast Message](documentation/readme/skeleton_plane/wireframe-desktop-toast-message.webp)

</details>

#### **Desktop Wireframes - Admin Flow**

<details>
<summary>Click to view Admin Desktop Wireframes</summary>

- Add Product

![Add Product](documentation/readme/skeleton_plane/wireframe-desktop-add-product.webp)

- Edit Product

![Edit Product](documentation/readme/skeleton_plane/wireframe-desktop-edit-product.webp)

- Delete Product

![Delete Product](documentation/readme/skeleton_plane/wireframe-desktop-delete-product.webp)

- Product Management

![Product Management](documentation/readme/skeleton_plane/wireframe-desktop-admin-dashboard.webp) |

</details>

<br>
<hr>

<a id="surface-plane"></a>

### Surface Plane

<a id="colour-scheme"></a>

#### Colour Scheme

The **Fit Six** colour palette is designed to reflect the brand’s identity as a bold, modern, and performance-driven gym — while maintaining a clean, accessible user interface for all devices.

This colour scheme combines **vibrant energy**, **professional clarity**, and **trust-building contrast**, aligning with the expectations of an e-commerce site focused on health, strength, and active lifestyles.

The primary colour variables defined in `style.css` are:

- `#001aaf` (**Highlight Blue**)  
  A strong, confident blue used for **buttons**, **headings**, and **interactive elements**. This shade represents **discipline, trust, and energy** — ideal for a brand promoting fitness and commitment. It provides a high-contrast accent without overwhelming the interface.

- `#dddddd` (**Base Grey**)  
  A light neutral used as a **background tone**, **card borders**, and **UI separators**. It offers subtle contrast against white, helping content blocks and images stand out without visual clutter.

- `#d6d6d6` (**Dark Border**)  
  A slightly deeper grey used for **form outlines**, **footer dividers**, and secondary UI elements. It ensures **visual hierarchy** and clean separation of content sections.

- `#ffffff` (**Background White**)  
  The dominant **site background**, chosen for its clean, modern look and **maximum readability**. It allows product images, CTAs, and content to shine with clarity and focus.

These colours were chosen to:
- Reinforce **brand consistency**
- Improve **readability and contrast** across devices
- Maintain a clean, **minimalist aesthetic** that supports both the gym’s identity and the needs of online shoppers

All colour variables are stored as **CSS custom properties** and reused consistently throughout the site for buttons, alerts, cards, nav elements, and banners.

> **Note:**  
> Colour variables are defined in `/static/css/style.css` for centralised control and maintainability.

```css
:root {
    --highlight-blue: #001aaf;
    --base-grey: #dddddd;
    --dark-border: #d6d6d6;
    --background-white: #ffffff;
}
```

> [!NOTE]
> Contrast compliance was fully tested and reported. For full detail, see [TESTING.md](TESTING.md)

<details>
<summary>- Toggle to view the colour swatches used throughout the site</summary>

![Fit Six Swatch Palette](documentation/readme/surface_plane/colours-swatches.webp)

</details>

<br>
<hr>

<a id="typography"></a>

#### Typography

[Google Fonts](https://fonts.google.com/) was used to import the selected fonts for the site, ensuring high‑quality and accessible typography across all devices and browsers. Fonts are imported using CSS `@import` with appropriate fallbacks defined for maximum cross‑device compatibility.

- **Headings (h1, h2, h3):** The font [Poppins](https://fonts.google.com/specimen/Poppins) was chosen for its bold, geometric yet friendly style that provides a clean, modern look. Its balanced curves and contemporary design help headlines stand out, giving the site a distinctive and polished visual identity while remaining easy to read.

![Poppins Font Example](documentation/readme/surface_plane/typography-poppins.webp)

- **Paragraphs and body text:** The font [Open Sans](https://fonts.google.com/specimen/Open+Sans) was selected for body copy due to its neutral tone, excellent legibility at various sizes, and compatibility across screen types. It complements Poppins without competing for attention, supporting a harmonious and user‑friendly reading experience throughout the site.

![Open Sans Font Example](documentation/readme/surface_plane/typography-open-sans.webp)

- Together, **Poppins** and **Open Sans** provide strong typographic contrast—balancing bold headlines with highly readable body text for an accessible, modern feel.

- **Icons and UI elements:** The [Font Awesome](https://fontawesome.com/) icon library was used to support the visual interface with clear, scalable icons. These icons align stylistically with the modern fonts and enhance user experience through recognizable visual cues for actions, navigation, and social media links.

> **Note:**  
> Font families are defined in `static/css/style.css` for consistency and maintainability.

```css
:root {
    /************ Typography ************/
    --primary-font: "Open Sans", sans-serif;
    --secondary-font: "Poppins", sans-serif;
}
```

<br>
<hr>

<a id="imagery"></a>

#### Imagery

The imagery used throughout the Fit Six site was selected to reflect the energy, focus, and community spirit of the gym and its members. High-quality stock images were sourced from [Adobe Stock](https://stock.adobe.com/) to give the platform a polished, brand-aligned aesthetic while remaining accessible and professional.

Key banners and product visuals feature themes of:
- **Strength and movement** – capturing workouts, dynamic training environments, and activewear in motion.
- **Community and support** – showcasing diverse gym-goers training together, reinforcing Fit Six's inclusive and motivational brand values.
- **Clean product displays** – focusing on fitness gear, apparel, and nutrition with neutral backgrounds to ensure clarity and professionalism.

Images were carefully selected and edited to ensure consistency in **tone, lighting, and composition**, providing visual cohesion across all views. This consistent imagery reinforces trust, supports branding, and contributes to a modern, aspirational e-commerce experience that appeals to both regular members and first-time visitors.

> **Note:** All hero banners and promotional images were optimised for web and stored in `media/` or `static/images/` as appropriate.

<br>
<hr>

<a id="features"></a>

### Features

**Fit Six Store** is a full-stack e-commerce platform built for *Fit Six Gym*, allowing members and visitors to browse, filter, and securely purchase gym merchandise, supplements, and class bundles. The site delivers a clean, intuitive shopping experience backed by robust Django functionality and Stripe integration.

Key features include:

- **Product Catalogue with Variant Support** – Products can have multiple variants (e.g. size, colour), improving flexibility for gym apparel and accessories.
- **Secure Stripe Checkout** – Integrated payment system with order summary, on-screen confirmation, and email receipts.
- **User Accounts and Order History** – Registered users can manage their profile, view past orders, and save delivery preferences.
- **Admin Product Management** – Superusers can add, edit, and remove products, adjust stock, and manage incoming orders.
- **Responsive Design** – All views adapt seamlessly across mobile, tablet, and desktop, ensuring accessibility and ease of use.
- **Form Validation and Feedback** – Inline validation and custom messages for improved usability and accessibility.
- **Custom Error Pages** – Branded 404 and 500 pages to guide users if something goes wrong.

These features combine to deliver a reliable and professional user experience, whether customers are browsing for the latest gym gear or staff are managing backend operations.

All pages on the website include:

- A favicon in the browser tab.

<details>
<summary>Click here to view the favicon</summary>

![favicon](documentation/readme/surface_plane/features-home-favicon.webp)

</details>

#### Defensive Programming

**Defensive programming principles** have been applied throughout the **Fit Six Store** to safeguard functionality and ensure that only **authorised users** can access sensitive features. Permission checks are enforced to restrict **admin-level actions** — such as adding, editing, or deleting products, or managing orders — to **superusers only**.

If a user attempts to access a **restricted page** or perform an unauthorised action, they are redirected appropriately — usually to the login page or homepage — depending on the context. This approach enhances both **security** and **user experience** by clearly communicating boundaries and preventing system misuse or unexpected errors.

<a id="design"></a>

### Design & Visuals

- [Balsamiq](https://balsamiq.com/) – Used to create wireframes for mobile, tablet, and desktop layouts.
- [Adobe Illustrator](https://www.adobe.com/uk/products/illustrator.html) – Used to design the logo and key UI elements.
- [Adobe Photoshop](https://www.adobe.com/uk/products/photoshop.html) – Used for cropping, resizing, and exporting images in WebP format to ensure faster load times and modern compression efficiency.

<a id="development-tools"></a>

### Development & Deployment

- [Heroku](https://www.heroku.com/) – Cloud platform used to deploy the final version of the application.
- [Cloudinary](https://cloudinary.com/) – Used to host and deliver user-uploaded images.
- [Git](https://git-scm.com/) – Used for version control throughout development.
- [GitHub](https://github.com/) – Repository hosting and collaboration platform.
- [Pip](https://pypi.org/project/pip/) – Python package manager used to install project dependencies.
- [Visual Studio Code](https://code.visualstudio.com/) – Primary code editor used for writing and debugging code.
- [Google Fonts](https://fonts.google.com/) – Used to integrate custom typography into the UI.
- [Font Awesome](https://fontawesome.com/) – Icon library used to enhance visual elements across the interface.

<a id="testing-tools"></a>

### Testing & Accessibility Tools

- [Coverage.py](https://coverage.readthedocs.io/) – Evaluates test suite effectiveness by reporting code coverage.
- [Google Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) – Used for debugging, inspecting elements, and responsive testing across screen sizes.
- [Mobile First Plugin](https://www.webmobilefirst.com/en/) – Simulates mobile device views to verify layout and responsiveness.
- [Aria DevTools](https://github.com/ziolko/aria-devtools) – Assesses screen reader accessibility and ARIA landmark use.
- [Webpage Spell-Check](https://chrome.google.com/webstore/detail/webpage-spell-check/mgdhaoimpabdhmacaclbbjddhngchjik) – Chrome extension for detecting typos across page content and documentation.

> [!NOTE]
> Manual testing covered all user flows, including edge cases and JavaScript interactions. For full detail, see [TESTING.md](TESTING.md)

<a id="content"></a>

## Content

The content displayed throughout the site is based on real-world products, services, and branding provided by Fit Six Gym, with kind permission from owner Sam Watson.

Product names, descriptions, categories, and pricing were either adapted from real items or created to reflect a realistic online store experience for a fitness-focused audience.

All other written content — including UI text, labels, instructions, button copy, and page descriptions — was written by me to support the site’s structure, tone, and user experience goals.

<a id="media"></a>

### Media

- [Adobe Stock](https://stock.adobe.com/) - Used to source royalty free imagery for the site.

<a id="acknowledgement"></a>

### Acknowledgments

I would like to acknowledge the following people:

- [Jubril Akolade](https://github.com/Jubrillionaire) - My Code Institute Mentor.

- Ax de Klerk, Jordan Acomba & Robert Lewis - My fellow Code Institute cohort, who helped each other over the course of our milestone projects.

- Special thanks to **Sam Watson at Fit Six** for granting permission to build this project around his gym and for his ongoing support.

- The Code Institute Slack channel Peer Code Review - Thank you to everyone who took the time to view my site and look over the code.

<br><hr>
[🔼 Back to top](#contents)