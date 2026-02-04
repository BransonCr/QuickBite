# Software Requirements Specification Document

## QuickBite - Food Delivery Application

**Team Name:** Group 15

**Github Repo:** https://github.com/BransonCr/cosc310-foodDelivery

**Project Backlog:** https://github.com/users/BransonCr/projects/3

**Date:** January 28th, 2026

---

## Table of Contents

1. [Project Description and Goal](#1-project-description-and-goal)
2. [Functional Requirements](#2-functional-requirements)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Requirements Traceability Matrix](#4-requirements-traceability-matrix)
5. [Contribution Statement](#5-contribution-statement)

---

# 1. Project Description and Goal

## 1.1 Project Overview

QuickBite, web-based food delivery application that connects customers with local restaurants. The platform allows users to browse restaurant menus, place orders, make secure payments, and track their deliveries. Restaurant owners can manage their menus and orders, while delivery drivers can accept and fulfill delivery requests.

## 1.2 Project Goal

The goal of QuickBite is to provide a user-friendly platform that is reliable, and simplifies the food ordering and delivery process for all stakeholders. The system aims to:

- Enable customers to order food from local restaurants effective
- Provide owners the tools to manage their presence and orders
- Allow delivery drivers to accept and complete deliveries
- Make sure payments methods are secure and have reliable payment processing
- Deliver a consistent and responsive user interface across web browsers.

## 1.3 Stakeholders

| Stakeholder | Description |
|-------------|-------------|
| Customer | Regular user that orders food, browses restaurants and receives food deliveries, and receives delivery updates |
| Restaurant Owner/Manager | Business owners who list their restaurants, manage menus, (Maybe integrated order system) |
| Systems Admins | Technical staff who performs platform maintenance, view all orders, and generate report, access list delivery employees |
| Delivery Drivers | Delivery of food orders and ensuring proper delivery of orders to customers. |

## 1.4 System Scope

- User registration and authentication for customers and restaurant owners/managers
- Restaurant and menu data management with validation
- Restaurant browsing and search with filtering and pagination
- Order management with business logic enforcement
- Delivery management with status tracking
- Price calculation including taxes and delivery fees
- Simulated payment processing
- Event based notifications for actions done by the system
- (Optional) Review and rating system for completed orders.
- (Optional) Admin features for viewing orders and generating reports

---

# 2. Functional Requirements

## 2.1 Core Feature: User Registration & Authentication (Feat1)

The system will allow users and restaurant owners/managers to create accounts and log in. It will handle user authentication (login), authorization (what each user is allowed to do), and basic user identity management. Different roles such as regular users and restaurant owners/managers will be supported.

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat1-FR1 | The system shall support four users roles: Customer, System Admin, Delivery Driver, and Restaurant Owner/Manager |
| Feat1-FR2 | The system will store user information after their account has successfully been created. |
| Feat1-FR3 | The system will support user authentication by using username and password. |
| Feat1-FR4 | The system will support account updates to user information like email and phone number. |

### Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| Feat1-NFR1 | The user login process must complete in less than 3 seconds under normal load. |
| Feat1-NFR2 | The user authentication service must always be up. |
| Feat1-NFR3 | System must store user passwords using a strong encryption algorithm |

### User Stories

**Feat1-US1: Account Registration**
> As a customer, I will register for my account by providing an email, password, username and phone number.

**Feat1-US2: User Login**
> As a user, I need to log in securely with a username/email and password so that I can access my features

**Feat1-US3: Account Creation**
> As a customer or Restaurant Owner, I need to be able to create a new account easily to access system features

**Feat1-US4: Password Recovery**
> As a user, I need a mechanism to recover or reset my password if I forget it.

**Feat1-US5: Login Feedback**
> As a user, I need to receive clear and immediate feedback if my login or registration attempt fails.

---

## 2.2 Core Feature: Menu Storing (Feat2)

The system will store information about restaurants and their menus. It will ensure that data is valid, properly connected (for example, menu items must belong to a restaurant), and that basic constraints are enforced, such as preventing invalid or missing values.

*(VINAY)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat2-FR1 | The system shall store restaurant information. |
| Feat2-FR2 | The system shall store menu information associated with a specific restaurant. |
| Feat2-FR3 | The system shall ensure that all menu items are correctly connected to an existing restaurant. |
| Feat2-FR4 | The system shall enforce data validation rules for all restaurant and menu data |
| Feat2-FR5 | The system shall prevent the entry of invalid or missing values for required data fields |
| Feat2-FR6 | The system shall allow restaurant owners to manage their restaurant and menu information |

### User Stories

**Feat2-US1:**
> "As a Restaurant Owner, I want a process to register my restaurant and set up my initial menu, so that my business can go up on Quickbite quickly and accurately."

*Acceptance Criteria:*
- Provide an interface for the owner to input all necessary restaurant details.
- Allow the creation of new menu items with required details (name, price, desc.)

**Feat2-US2:**
> "As a Customer, I want to only see menu items that are properly connected to the restaurant I am viewing so that I can trust the menu is accurate and don't order food from the wrong place"

*Acceptance Criteria:*
- When browsing a restaurant's menu, every displayed menu item must have an active link to the specific restaurant
- Prevent any menu items with missing or invalid required data from being displayed

**Feat2-US3:**
> "As an admin, I need that database to enforce all data validation and connection rules, so that I can be confident in the integrity of the core restaurant and menu data for reporting and maintenance.

*Acceptance Criteria:*
- Block any attempt to store a menu item that is not linked to an existing restaurant id
- Prevent database entries that violate data validation rules

---

## 2.3 Core Feature: Menu Browsing (Feat3)

The system will allow users to browse restaurant menus and search for items or restaurants. Backend logic will handle filtering, searching, and returning paginated results.

*(JULIAN)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat3-FR1 | The system will perform queries based on customer search terms to return restaurants based on restaurant name or food products they sell. |
| Feat3-FR2 | The system will return a temporary list of restaurants that matches search terms. |
| Feat3-FR3 | The system will implement navigation to a restaurant's page when a customer selects an option from the queried results. |
| Feat3-FR4 | The system will keep a maximum number of results per page so that the page only displays a certain number of results per page. |

### User Stories

**Feat3-US1:**
> "As a customer, I want to search the platform for specific food items or restaurants to match what food I'm in the mood for."

*Acceptance Criteria:*
- Provide customers with a clear search bar.
- Have the search term narrow down results in a list visible to the user.
- This will return restaurants whose name matches the search term or sells products that match the search term.
- There will be a limit of 10 results per page.

**Feat3-US2:**
> "As a restaurant owner/manager, I want to be able to update my menu with new items to follow trends in the restaurant industry."

*Acceptance Criteria:*
- Provide owners/managers with an interface that lets them add items to the menu.
- Sync changes made to menus with customer view of menus.
- Search results containing the added product should now return the restaurant that has added the product to its menu

**Feat3-US3:**
> "As a customer, I want to browse easily through restaurants without the page being cluttered."

*Acceptance Criteria:*
- Provide the customer with a pleasing user interface that shows only the number of results as specified by the system.
- Allow the user to browse pages with a simple paginated number bar at the bottom of the page.

---

## 2.4 Core Feature: Order Management (Feat4)

The system will allow users to create and manage food orders. It will ensure that orders are consistent, correctly stored, and follow business logic for the domain (for example, an order cannot be modified after it is completed).

*(VINAY)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat4-FR1 | The system shall allow customers to create a new order by adding items from a restaurant's menu |
| Feat4-FR2 | The system shall accurately store all necessary order details such as total price, customer ID and restaurant ID |
| Feat4-FR3 | The system shall allow customers to modify an order as long as order is pending or in cart |
| Feat4-FR4 | The system shall lock an order from further customer modification once its status changes to "confirmed" by restaurant |
| Feat4-FR5 | The system shall maintain and update the order status through the delivery process |
| Feat4-FR6 | Allow both the customer and restaurant to cancel an order, subject to predefined business rules based on orders status. |

### User Stories

**Feat4-US1:**
> "As a customer, I want to be able to easily create a new food order and make changes to it while still deciding, so that I can ensure my final order is exactly what I want before it's sent to the restaurant."

*Acceptance Criteria:*
- Allows to add multiple menu items from a single restaurant to order
- DIsplay an up-to-date running total of my order cost.

**Feat4-US2:**
> "As a restaurant owner, I need to confirm and process incoming orders promptly so that  I can start preparing the food and lock the order details to prevent late customer changes."

*Acceptance Criteria:*
- Interface to view new incoming orders with all necessary details
- Change order status from pending to confirmed

**Feat4-US3:**
> "As an admin, I need a log of all order status changes and cancellation attempts, so I can audit systems performance and ensure data integrity and compliance with business rules."

*Acceptance Criteria:*
- Record and store date,time, and person responsible for every change in order status.
- Retain full status history for every order, even after order is completed/cancelled.

---

## 2.5 Core Feature: Delivery Management (Feat5)

The system will manage delivery-related information. It will support assigning deliveries and tracking basic delivery status as part of the backend logic.

*(BRANSON)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat5-FR1 | The system shall store delivery information with associated orders |
| Feat5-FR2 | The system shall allow assignment of deliveries to orders |
| Feat5-FR3 | The system shall track delivery status (assigned, in-transit, delivered) |
| Feat5-FR4 | The system shall store delivery address and delivery instructions |
| Feat5-FR5 | The system shall shall update delivery status as part of the order flow |
| Feat5-FR6 | The system shall record delivery completion time |

### User Stories

**Feat5-US1: Track Delivery**
> "As a customer I want to track my deliveries status to know when I will receive  my order/delivery/food"

*Acceptance Criteria:*
- Delivery status is visible on the order details page
- Status shows current state of the delivery (assigned, in-transmit, delivered)
- Estimated delivery is displayed
- Status updates when state change on page

**Feat5-US2: Delivery Assignment**
> "As a restaurant manager, I want to mark orders as out for delivery so customers will see when their order is on the way"

*Acceptance Criteria:*
- Restaurant owner/manager can mark orders on the order page as "out for deliver"
- System records to show restaurant owners/managers previous order information
- Delivery assignment is reflected in order status
- Customer can view the updated order assignment updates

**Feat5-US3: Delivery Completion**
> "As a restaurant manager, I want to mark delivery status as completed to clear out the order queue (mark completed)"

*Acceptance Criteria:*
- Order status can be marked as completed
- System will record and display delivery time on order completion/delivery
- Customer may see the delivery was completed
- Order status updated to delivered

---

## 2.6 Core Feature: Price Calculation (Feat6)

The system will calculate the total cost of an order, including item prices, delivery fees, and taxes. These calculations will follow predefined business rules implemented in the backend.

*(LEO)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat6-FR1 | The system shall calculate the tax of the order based on location of customer |
| Feat6-FR2 | The system shall calculate delivery fee based on distance travelled |
| Feat6-FR3 | The item price should display accurately based on location (it should have different prices depending on the country). |
| Feat6-FR4 | The system will calculate tips based on the customer's total order before tax (tips are not tax). |

### User Stories

**Feat6-US1:**
> "My tax calculation should be accurate based on where my location"

*Acceptance Criteria:*
- Display the right tax calculation based on the customer's postal code.

**Feat6-US2:**
> "The price of the food should display according to my location"

*Acceptance Criteria:*
- Display the prices of the food based on the location of the customer.

**Feat6-US3:**
> "I want to tip my courier based on of my total cost order"

*Acceptance Criteria:*
- Percentage of the total cost order options will be given to the customer to decide how much tip to give to courier

---

## 2.7 Core Feature: Simulated Payment Processing (Feat7)

The system will simulate payment processing. No real payment gateway will be used, but the system will follow the correct workflow for accepting or rejecting a payment and updating the order status.

*(JULIAN)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat7-FR1 | The system will validate the user's payment information. |
| Feat7-FR2 | The system will update the payment status to "payment received" once the payment has been processed completely. |
| Feat7-FR3 | The system will require users to fill out all payment information completely before attempting payment. |
| Feat7-FR4 | The system will prevent users from cancelling their order after payment has been processed. |
| Feat7-FR5 | The system should generate a confirmation number after payment has been received. |

### User Stories

**Feat7-US1:**
> "As a customer, I want to complete payment for my order so that the restaurant can begin preparing my food right away.“

*Acceptance Criteria:*
- Payment form will collect payment information like card number, expiration date, and CVV.
- Payment is simulated and goes through if the card information is valid, not authenticated.
- Successful payment updates order to confirmed status.
- The confirmation number that is generated will be displayed to the customer.

**Feat7-US2:**
> "As a customer, I want to be notified if my payment fails so that I can correct the issue and try again.”

*Acceptance Criteria:*
- Failed payment displays a clear error message indicating the reason.
- Order remains in pending status after failed payment.
- Customer can retry payment with corrected information.
- System logs payment failure reason for troubleshooting.
- Customers should also be given the option to cancel their order at this point.

**Feat7-US3:**
> "As a customer, I want to receive confirmation of my payment so that I know my order is being processed.”

*Acceptance Criteria:*
- Confirmation page displays order number and total amount paid.
- Payment status is marked as complete in the system.
- Order moves to confirmed status after successful payment.
- Customer can view payment details in their order history.

**Feat7-US4:**
> "As a restaurant owner, I want to only receive orders that have been paid for so that I don't end up making orders that are eventually cancelled.”

*Acceptance Criteria:*
- Orders are only sent to restaurants once the confirmation number has been generated.
- Orders that have payment received are the only ones sent to restaurants.
- Orders that are cancelled should never reach a restaurant.

---

## 2.8 Core Feature: Notification Manager (Feat8)

The system will generate notifications or events when important actions occur, such as order creation or status changes.

*(LEO)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat8-FR1 | The system will display notifications in a popup badge to users. |
| Feat8-FR2 | The system will notify the customer that they have ordered food. |
| Feat8-FR3 | The system notifies the customer that courier has picked up their order |
| Feat8-FR4 | The system notified the customer that the restaurant taken their order |
| Feat8-FR5 | The system will notify a restaurant owner if an order hasn't gone through |

### User Stories

**Feat8-US1:**
> "It must always notify me what's happening to my order"

*Acceptance Criteria:*
- Notification of delay order
- Courier has picked up the order
- Notify if the courier has been in an accident
- Restaurant has picked up the customer's order
- The customer has ordered food
- Food has arrived at customer location

**Feat8-US2:**
> "As a restaurant owner, I want to know about the status of orders at my restaurant and if people are cancelling orders."

*Acceptance Criteria:*
- Notify the restaurant owners when an order is cancelled at their restaurant
- Notify the restaurant owner when an order is confirmed.
- Notify the restaurant owner when an order has been payed for.

---

## 2.9 Optional Feature: Review and Rating System (Feat9)

The system may allow users to rate and review completed orders or restaurants. This feature is optional and can be implemented if time permits.

*(BRANSON)*

### System Requirements

| ID | Requirement |
|----|-------------|
| Feat9-FR1 | The system shall allow rating of completed/delivered orders on a scale of 1-5 |
| Feat9-FR2 | The system shall allow customers to write text reviews for restaurants |
| Feat9-FR3 | The system shall only allow reviews of completed orders they placed |
| Feat9-FR4 | The system shall calculate a weighted average of the restaurants reviews |
| Feat9-FR5 | The system shall display reviews on the restaurants page sorted by most recent |

### User Stories

**Feat9-US1: Rate Order**
> "As a customer, I want to rate my completed order so other customers can see the experience I had"

*Acceptance Criteria:*
- Rating option appears if and only if the order was delivered
- Customer may only select on a scale of 1-5
- Rating contributes to the restaurants overall rating average
- Rating is associated with the completed order

**Feat9-US2: View Reviews (Restaurant)**
> "As a restaurant manager/owner, I want to see rated reviews to see what I can improve in the restaurant"

*Acceptance Criteria:*
- Reviews are displayed on the restaurants main page
- Average rating is a weighted average of the sum amount of reviews
- Reviews show associated rating
- Reviews are shown in most recently made first

**Feat9-US3: Write Review**
> "As a customer, I want to review such that I can provide detailed feedback on the experience I had"

*Acceptance Criteria:*
- Reviews are limited to 7bit ASCII and 500 characters
- Reviews are associated with the specific customer making the review
- Reviews are stored on the restaurants page
- Reviews are associated with the completed order.

---

## 2.10 Optional Feature: Admin Features (Feat10)

The system may include administrative features such as viewing all orders and generating simple reports or statistics (for example, average delivery time or most popular restaurants). This feature is optional.

---

# 3 Non-Functional Requirements

## 3.1 Performance Requirements

| ID | Requirement |
|----|-------------|
| NFR-1 | The system shall load any page within 3 seconds in normal network conditions |
| NFR-2 | The system shall support up to 500 concurrent users |
| NFR-3 | The system shall process payment information within 5 seconds |
| NFR-4 | The system will update order delivery information within 30 seconds of status change |

## 3.2 Security Requirements

| ID | Requirement |
|----|-------------|
| NFR-5 | The system shall encrypt all data using HTTPs |
| NFR-6 | The system shall use bcrypt hashing for passwords with a minimum factor cost of 10 |
| NFR-7 | The system shall use a rate limiting feature for login attempts up to a maximum of 5 |

## 3.3 Usability Requirements

| Id | Requirement |
|----|-------------|
| NFR-8 | The system shall allow users to complete orders in no more than 5 steps |
| NFR-9 | The system shall provide clear error messages that guide users to resolutions |

## 3.4 Reliability Requirements

| Id | Requirements |
|----|-------------|
| NFR-10 | The system shall automatically save cart contents to ensure persistence across user sessions |
| NFR-11 | The system shall implement database backups |

## 3.5 Scalability Requirements

| Id | Requirements |
|----|-------------|
| NFR-12 | The system shall be designed horizontally to handle increased user load |
| NFR-13 | The system shall support adding new restaurants without system downtime |

---

# Domain Requirements

Domain requirements reflect constraints that are inherent to the food delivery business domain.

| ID | Requirement | Rationale |
|----|-------------|-----------|
| DR-1 | An order must contain items from only one restaurant | Delivery logistics require single pickup location per order |
| DR-2 | Menu items must have a positive price greater than zero | Food items cannot be free or negatively priced |
| DR-3 | Orders cannot be placed from restaurants that are closed | Restaurants have operating hours that must be respected |
| DR-4 | Delivery addresses must be within the restaurant's delivery radius | Restaurants have geographic delivery limitations |
| DR-5 | Tax rates must comply with local tax regulations | Food delivery is subject to regional tax laws |
| DR-6 | Customers must provide a valid delivery address before checkout | Physical delivery requires a real destination |

---

# 4. Requirements Traceability Matrix

The following matrix shows the hierarchical relationships between high-level requirements (core features), system requirements (functional requirements), and user requirements (user stories), following forward traceability from requirements to implementation artifacts.

| High Level Requirements | | System Requirements | | User Requirements | Critical Components |
|---|---|---|---|---|---|
| **HR1** | **User Registration & Authentication:** Enables users to create accounts, authenticate, and manage credentials | **SR1** | The system shall support two users roles: Customer and Restaurant Owner/Manager | Feat1-US1, Feat1-US3 | UI, UserCreationAPI, LoginAPI, PasswordValidator
| | | **SR2** | The system will store user information after their account has successfully been created. | Feat1-US1 |
| | | **SR3** | The system will support user authentication by using username and password. | Feat1-US2 |
| | | **SR4** | The system will support account updates to user information like email and phone number. | Feat1-US1 |
| **HR2** | **Menu Storing:** Enables restaurant owners to manage restaurant profiles and menu items with data validation | **SR5** | The system shall store restaurant information. | Feat2-US1 | RestaurantMenuAPI |
| | | **SR6** | The system shall store menu information associated with a specific restaurant. | Feat2-US1, Feat2-US2 |
| | | **SR7** | The system shall ensure that all menu items are correctly connected to an existing restaurant. | Feat2-US2, Feat2-US3 |
| | | **SR8** | The system shall enforce data validation rules for all restaurant and menu data | Feat2-US3 |
| | | **SR9** | The system shall prevent the entry of invalid or missing values for required data fields | Feat2-US2, Feat2-US3 |
| | | **SR10** | The system shall allow restaurant owners to manage their restaurant and menu information | Feat2-US1, Feat2-US2 |
| **HR3** | **Menu Browsing:** Allows customers to discover restaurants and menu items through browsing, filtering, and searching | **SR11** | The system will perform queries based on customer search terms to return restaurants based on restaurant name or food products they sell. | Feat3-US1 | RestaurantMenuAPI, RestaurantSearch, RestaurantDB(csv file) |
| | | **SR12** | The system will return a temporary list of restaurants that matches search terms. | Feat3-US1 |
| | | **SR13** | The system will implement navigation to a restaurant's page when a customer selects an option from the queried results. | Feat3-US1 |
| **HR4** | **Order Management:** Enables customers to create orders and track their status, and restaurant owners to process orders | **SR14** | The system shall allow customers to create a new order by adding items from a restaurant's menu | Feat4-US1 | UI, OrderManagerAPI |
| | | **SR15** | The system shall accurately store all necessary order details such as total price, customer ID and restaurant ID | Feat4-US1, Feat4-US3 |
| | | **SR16** | The system shall allow customers to modify an order as long as order is pending or in cart | Feat4-US1 |
| | | **SR17** | The system shall lock an order from further customer modification once its status changes to "confirmed" by restaurant | Feat4-US2 |
| | | **SR18** | The system shall maintain and update the order status through the delivery process | Feat4-US2, Feat4-US3 |
| | | **SR19** | Allow both the customer and restaurant to cancel an order, subject to predefined business rules based on orders status. | Feat4-US1, Feat4-US2 |
| **HR5** | **Delivery Management:** Tracks delivery status and manages the delivery workflow for orders | **SR20** | The system shall store delivery information with associated orders | Feat5-US1 | DeliveryStatusAPI, OrderInfoDB (csv file) |
| | | **SR21** | The system shall allow assignment of deliveries to orders | Feat5-US2 |
| | | **SR22** | The system shall track delivery status (assigned, in-transit, delivered) | Feat5-US1 |
| | | **SR23** | The system shall store delivery address and delivery instructions | Feat5-US1 |
| | | **SR24** | The system shall shall update delivery status as part of the order flow | Feat5-US2, Feat5-US3 |
| | | **SR25** | The system shall record delivery completion time | Feat5-US3 |
| **HR6** | **Price Calculation:** Calculates order totals including subtotals, taxes, and delivery fees | **SR26** | The system shall calculate the tax of the order based on location of customer | Feat6-US1 | PriceCalculator |
| | | **SR27** | The system shall calculate delivery fee based on distance travelled | Feat6-US2 |
| | | **SR28** | The item price should display accurately based on location (it should have different prices depending on the country). | Feat6-US2 |
| | | **SR29** | The system will calculate tips based on the customer's total order before tax (tips are not tax). | Feat6-US3 |
| **HR7** | **Payment Processing (Simulated):** Simulates payment processing workflow without real payment gateway integration | **SR30** | The system shall simulate payment processing without connecting to real payment gateways | Feat7-US1 | PaymentValidator, PaymentAPI |
| | | **SR31** | The system shall follow the correct workflow for accepting or rejecting a payment | Feat7-US1, Feat7-US2 |
| | | **SR32** | The system shall update order status based on payment success or failure | Feat7-US1, Feat7-US3 |
| | | **SR33** | The system shall generate a confirmation number upon successful payment | Feat7-US3, Feat7-US4 |
| | | **SR34** | The system shall handle simulated payment failures and display appropriate error messages | Feat7-US2 |
| | | **SR35** | The system shall record payment status with each order | Feat7-US3 |
| **HR8** | **Notification Manager:** Generates notifications and logs events for important system actions | **SR36** | Exclusive offers will be presented to the user | Feat8-US1 | NotificationManager |
| | | **SR37** | The customer will notified as soon they order | Feat8-US2 |
| | | **SR38** | The customer is notified if the order is picked up by courier | Feat8-US2 |
| | | **SR39** | The customer is notified if the restaurant has taken the order of the customer | Feat8-US2 |
| **HR9** | **Reviews & Ratings (Optional):** Allows customers to rate and review restaurants after completing orders | **SR40** | The system shall allow rating of completed/delivered orders on a scale of 1-5 | Feat9-US1 | UserReview, OrderDB (csv file), ReviewDB (csv file) |
| | | **SR41** | The system shall allow customers to write text reviews for restaurants | Feat9-US3 |
| | | **SR42** | The system shall only allow reviews of completed orders they placed | Feat9-US1, Feat9-US3 |
| | | **SR43** | The system shall calculate a weighted average of the restaurants reviews | Feat9-US2 |
| | | **SR44** | The system shall display reviews on the restaurants page sorted by most recent | Feat9-US2 |

## User Requirements Reference

The following table has been copied and provides quick reference for user stories mapped in the traceability matrix:

| User Requirement ID | Description |
|---------------------|-------------|
| Feat1-US1 | As a customer, I will register for my account by providing an email, password, username and phone number. |
| Feat1-US2 | As a user, I need to log in securely with a username/email and password so that I can access my features |
| Feat1-US3 | As a customer or Restaurant Owner, I need to be able to create a new account easily to access system features |
| Feat1-US4 | As a user, I need a mechanism to recover or reset my password if I forget it. |
| Feat1-US5 | As a user, I need to receive clear and immediate feedback if my login or registration attempt fails. |
| Feat2-US1 | As a Restaurant Owner, I want a process to register my restaurant and set up my initial menu, so that my business can go up on Quickbite quickly and accurately. |
| Feat2-US2 | As a Customer, I want to only see menu items that are properly connected to the restaurant I am viewing so that I can trust the menu is accurate and don't order food from the wrong place |
| Feat2-US3 | As an admin, I need that database to enforce all data validation and connection rules, so that I can be confident in the integrity of the core restaurant and menu data for reporting and maintenance. |
| Feat3-US1 | As a customer, I want to search the platform for specific food items or restaurants to match what food I'm in the mood for. |
| Feat3-US2 | As a restaurant owner/manager, I want to be able to update my menu with new items to follow trends in the restaurant industry. |
| Feat4-US1 | As a customer, I want to be able to easily create a new food order and make changes to it while still deciding, so that I can ensure my final order is exactly what I want before it's sent to the restaurant. |
| Feat4-US2 | As a restaurant owner, I need to confirm and process incoming orders promptly so that I can start preparing the food and lock the order details to prevent late customer changes. |
| Feat4-US3 | As an admin, I need a log of all order status changes and cancellation attempts, so I can audit systems performance and ensure data integrity and compliance with business rules. |
| Feat5-US1 | As a customer I want to track my deliveries status to know when I will receive my order/delivery/food |
| Feat5-US2 | As a restaurant manager, I want to mark orders as out for delivery so customers will see when their order is on the way |
| Feat5-US3 | As a restaurant manager, I want to mark delivery status as completed to clear out the order queue (mark completed) |
| Feat6-US1 | My tax calculation should be accurate based on where my location |
| Feat6-US2 | The price of the food should display according to my location |
| Feat6-US3 | I want to tip my courier based on of my total cost order |
| Feat7-US1 | As a customer, I want to complete payment for my order so that the restaurant can begin preparing my food |
| Feat7-US2 | As a customer, I want to be notified if my payment fails so that I can correct the issue and try again |
| Feat7-US3 | As a customer, I want to receive confirmation of my payment so that I know my order is being processed |
| Feat7-US4 | As a customer, I want to receive confirmation of my payment so that I know my order is being processed. |
| Feat8-US1 | The app should notify me if there was exclusive offers |
| Feat8-US2 | It must always notify me what's happening to my order |
| Feat9-US1 | As a customer, I want to rate my completed order so other customers can see the experience I had |
| Feat9-US2 | As a restaurant manager/owner, I want to see rated reviews to see what I can improve in the restaurant |
| Feat9-US3 | As a customer, I want to review such that I can provide detailed feedback on the experience I had |

---

# 5. Contribution Statement

| Team Member | Contribution | Percentage |
|-------------|--------------|------------|
| **Julian Mohammed** | Feat3 (Menu Browsing), Feat7 (Simulated Payment Processing) | 25% |
| **Branson Crawford** | Feat5 (Delivery Management), Feat9 (Review and Rating System) | 25% |
| **Vinay Dhillon** | Feat2 (Menu Storing), Feat4 (Order Management) | 25% |
| **Leo Cabral** | Feat6 (Price Calculation), Feat8 (Notification Manager) | 25% |

---

# Appendix A: Glossary

| Term | Definition |
|------|------------|
| Customer | A user who orders food, browses restaurants, and receives food deliveries |
| Restaurant Owner/Manager | A business owner who lists their restaurant, manages menus, and processes orders |
| Delivery Driver | A user responsible for delivering food orders to customers |
| Order | A request from a customer for food items from a restaurant |
| Menu | A collection of food items offered by a restaurant |
| Authentication | The process of verifying user identity through credentials |
| Authorization | The process of determining what actions a user is allowed to perform |
| Functional Requirement | A specification of what the system should do |
| Non-Functional Requirement | A specification of system quality attributes (performance, security, etc.) |
| User Story | A requirement written from the perspective of an end user |
| Traceability Matrix | A document linking requirements to their sources and implementation |

---

# Appendix B: Project Backlog Reference

**GitHub Repository:** https://github.com/BransonCr/cosc310-foodDelivery

**Project Backlog:** https://github.com/users/BransonCr/projects/3

The backlog includes:
- Core Feature Issues (Feat1-Feat10) with unique identifiers
- Functional Requirements as sub-issues linked to their corresponding features
- User Stories as sub-issues linked to their corresponding features
- All issues prioritized with acceptance criteria
- User stories written in standard user story format






---

*EOD*
