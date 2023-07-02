# Overview
This is a simple database app intended to build and demonstrate basic database skills. I built this using a free Firebase app and the django python framework.

[Software Demo Video](https://youtu.be/WP0Oaw7k9jQ)

# Cloud Database
My cloud database Has two main tables inside it. The "Shop" Table which contains the various things that appear in the shop, And the "User" Table which contains user specific information such as inventory and funds. 
  
  # Shop
  The shop only has one table in it now, But I plan to expand to other types as well. The "Aliens" tabledepicted below demonstrates how other tables will eventually work as well.
  
![image](https://github.com/DanielSaunders-SoftwarePortfolio/Public-Portfolio/assets/131573288/2bb0600d-18c3-4d7e-8f4d-c095da374434)
  
  The items name is the key of each table item and value contains certain useful information such as the stats and the price.

  # Users
  The users Table is not where user credentials are stored, but does contain the users ingame funds and curent inventory.
  
![image](https://github.com/DanielSaunders-SoftwarePortfolio/Public-Portfolio/assets/131573288/f6e777c1-82bc-49ac-8336-2eb41f8e0172)
  
  Each Key in the inventory will correspond to an item in one of the shop tables. When displaying the inventory, I should be able to use the key from the inventory to pull the information from the shop table.
  The key for each entry in the "Users" list is the user ID. Each time a new user signs up, in adition to creating an authenticated user for the database, the signup form creates a user entry in the user table and populates it with standardized beginner values such as starting funds.

# Development Environment
I built this app in visual studio code using python code and the django and pyrebase libraries.

# Useful Websites
The following sites helped me develop the code I used in this app.

- [Django Tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
- [Integration Tutorial]([http://url.link.goes.here](https://www.section.io/engineering-education/integrating-firebase-database-in-django/))
- [User Authentication - geeksforgeeks](https://www.geeksforgeeks.org/django-authentication-project-with-firebase/)


# Future Work
- Build a view for users to see their inventory
- Add a way for users to earn money
- Customize login and signup HTML
- Include better navigation buttons
