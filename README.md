# **CafeBazzar Crawler**

---

### **What is this?**
This is a crawler for this [site](https://cafebazaar.ir/) which crawled all categories with its api and save data like:
* app name
* app path
* app link
* app author name
* app category name 
* app price
* app review count
* app install count

in mysql database.

---
### **Why should I make it?**
I make it for practice, fun and  work with Peewee ORM!

---
### **How Work it?**
This [site](https://cafebazaar.ir/) send json response to user
Its has api and crawler work with that.
api has a payload we can send app path with that and get information from site 
but before this we collect all categories from site and send in payload to other api and get all app path in that category and use app paths in get information app.

---

### **What we need?**
this crawler has a bug, but I can't find that.
what that? I get app path and convert to set which duplicate app path deleted and save in database and before this check exists app path if that exists don't save that but two or three app path save duplicate
and also this problem in information apps in database 


