# QuickBite - Software Architecture & Design Document
## Milestone 2 Submission

**Team Members:** Julian Mohamed, Vinay Dhillon, Branson Crawford, Leo Cabral

**Project:** QuickBite Food Delivery System

**Date:** February 2026

---

## Table of Contents
1. [High-Level Architecture](#1-high-level-architecture)
2. [Low-Level Design](#2-low-level-design)
3. [Traceability Matrix](#3-traceability-matrix)

---

## 1. High-Level Architecture

### 1.1 Use Case Diagram

**See Diagram:** `UseCase_QuickBite.png`

---

### 1.2 Architecture Overview

**See Diagram:** `Architecture.pdf`

We chose MVC because it separates the user interface (View) from the business logic (Model). This allows our team (Julian, Vinay, Branson, Leo) to work on the front end and back end in parallel without conflicts, accelerating development. This is also known as the Model, View, Controller architecture, and is how our system will interact with itself.

**Model** (Data & Business Logic) – Responsible for managing the data, state, and DB interaction. It also enforces rules of the application.

**View** (User Interface) – Responsible for displaying information from the Model to the user and sending user actions to the controller.

**Controller** (Intermediary) – Acts as the intermediate middle man for the view and model, receiving user input from the view, and sending to the model for interactions with the DB, and then selects the view for rendering.

With our specific system, an example would include the login feature, where users are displayed a login button (from the view), clicking/interacting with the button (controller), the controller sends the login information to the model where the data is validated (model), and then sent back to the controller, where the correct view is displayed based on the state of the controller (success login/fail login).

With a non-functional requirement (e.g., supporting 500 concurrent users), MVC supports NFR-2 (Scalability) by decoupling the View from the Model. This allows us to optimize the database queries (Model) independently of the user interface, ensuring that heavy back end processing does not freeze the user's browser experience.

---

## 2. Low-Level Design

### 2.1 Component Identification

**See Diagram:** `Component Idenfication.pdf`

**Feature 1:** Main Class is `UserCreation`, its responsibilities are to handle account creation.
- Supporting two roles: Customer (the one ordering food) and Restaurant owner
- Storing user information after it's created
- Validating username and password and updating it
- Login system

**Feature 2:** Main Class is `RestaurantMenu`, its responsibility is ensuring correct information about the restaurant are stored inside the system.
- Storing restaurant information including menu and location of the restaurant
- Restaurant owners can edit their menu and display its availability

**Feature 3:** Main Class is `MenuBrowsing`, its responsibility is filter out restaurant given customer's requested food options.
- Query system for customer to choose their order
- Matching customer's searched item to database
- Limiting the restaurant pages to display
- Navigation system for page requested by the customer

**Feature 4:** Main Class is `OrderManager`, its responsibility is to handle customer's order.
- Order creation by the customer and correctly storing order information
- Following business rules based on location
- Modification of order by customer and restaurant owner
- Updates on order status
- Canceling orders within certain time

**Feature 6:** Main Class is `PriceCalculator`, its responsibility is calculate total order cost.
- Properly handle tax and currency based on location
- Tips system
- Display the right currency (location)

**Feature 7:** Main Class is `PaymentHandler`, its responsibility is validate customer payment.
- Validating information of customer's payment method
- Accepting the payment method and rejecting them

**Feature 8:** Main Class is `NotificationManager`, its responsibility is notify the customer or restaurant about the order.
- Notification of the order placed to customer and notify the restaurant about the order
- Notifying the customer of status of their order (Pickup by the courier, delivered, delays, cancellations)
- Notifying issues about the customer's order from the restaurant

**Feature 9:** Main Class is `UserReview`, its responsibility is display review of certain restaurants.
- Rating system is 1star-5star review
- Only those that have completed their order can rate
- Calculate the average review from the customers

#### Connections

- Feature 2 gives information for Feature 4 to handle the right order for the customer
- Feature 6 handles the amount deduction so Feature 7 can deduce the right amount for customer's valid information
- Feature 7 can validate customer's payment to make Feature 4 deny or accept the customer's order
- Feature 3 should accurately grab information from Feature 2
- Feature 9 allows store review to corresponding restaurant (Feature 2)
- Feature 8 acts as messenger to customer about their order (Feature 4)

---

### 2.2 Design Diagrams

#### 2.2.1 Data Flow Diagram (Level 1)

**See Diagram:** `QuickBite Data Flow Diagram: Level 1.pdf`

---

#### 2.2.2 Class Diagram

**See Diagram:** `Class diagram.pdf`

---

#### 2.2.3 Sequence Diagrams

##### Sequence Diagram 1: User Login

**See Diagram:** `Login Sequence Diagram.pdf`

##### Sequence Diagram 2: User Registration

**See Diagram:** `Registration Sequence Diagram.pdf`

##### Sequence Diagram 3: Create Order (Place Order)

**See Diagram:** `Sequence_PlaceOrder.png`

---

## 3. Traceability Matrix

| Req ID | Requirement Description | User Story | Component(s) |
|--------|------------------------|------------|--------------|
| FR-1.1 | System shall allow users to create accounts | As a customer, I want to register an account so I can place orders | UserCreation |
| FR-1.2 | System shall support Customer and Restaurant Owner roles | As a user, I want to select my role during registration | UserCreation |
| FR-1.3 | System shall validate credentials during login | As a user, I want to securely log in to my account | UserCreation |
| FR-1.4 | System shall store user information securely | As a user, I want my data protected | UserCreation |
| FR-2.1 | System shall display restaurant menus | As a customer, I want to view restaurant menus | RestaurantMenu, MenuBrowsing |
| FR-2.2 | Restaurant owners can edit menus | As a restaurant owner, I want to update my menu | RestaurantMenu |
| FR-2.3 | System shall show item availability | As a customer, I want to see available items | RestaurantMenu |
| FR-3.1 | System shall allow menu/restaurant search | As a customer, I want to search for food | MenuBrowsing |
| FR-3.2 | System shall filter search results | As a customer, I want to filter restaurants | MenuBrowsing |
| FR-3.3 | System shall paginate results | As a customer, I want to browse results page by page | MenuBrowsing |
| FR-4.1 | System shall create orders | As a customer, I want to place an order | OrderManager |
| FR-4.2 | System shall allow order modification | As a customer, I want to modify my order | OrderManager |
| FR-4.3 | System shall track order status | As a customer, I want to see my order status | OrderManager, NotificationManager |
| FR-4.4 | System shall allow order cancellation | As a customer, I want to cancel within time limit | OrderManager |
| FR-6.1 | System shall calculate order totals | As a customer, I want to see accurate pricing | PriceCalculator |
| FR-6.2 | System shall apply location-based taxes | As a customer, I want correct tax calculation | PriceCalculator |
| FR-6.3 | System shall support tipping | As a customer, I want to add a tip | PriceCalculator |
| FR-7.1 | System shall validate payment methods | As a customer, I want secure payment | PaymentHandler |
| FR-7.2 | System shall process/reject payments | As a customer, I want payment confirmation | PaymentHandler |
| FR-8.1 | System shall notify order placement | As a customer/restaurant, I want order notifications | NotificationManager |
| FR-8.2 | System shall notify order status updates | As a customer, I want delivery updates | NotificationManager |
| FR-8.3 | System shall notify issues | As a customer, I want to know about problems | NotificationManager |
| FR-9.1 | System shall allow rating (1-5 stars) | As a customer, I want to rate my experience | UserReview |
| FR-9.2 | Only completed orders can be rated | As a customer, I want to review after delivery | UserReview, OrderManager |
| FR-9.3 | System shall display average ratings | As a customer, I want to see restaurant ratings | UserReview |

---

## Appendix: Diagram Files

| Diagram | File Name |
|---------|-----------|
| Use Case Diagram | `UseCase_QuickBite.png` |
| Architecture Overview | `Architecture.pdf` |
| Class Diagram | `Class diagram.pdf` |
| Data Flow Diagram (Level 1) | `QuickBite Data Flow Diagram: Level 1.pdf` |
| Login Sequence Diagram | `Login Sequence Diagram.pdf` |
| Registration Sequence Diagram | `Registration Sequence Diagram.pdf` |
| Place Order Sequence Diagram | `Sequence_PlaceOrder.png` |
| Component Identification | `Component Idenfication.pdf` |

---

*Document prepared for COSC 310 - Milestone 2 Submission*
