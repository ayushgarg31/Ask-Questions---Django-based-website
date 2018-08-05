# Ask-Questions---Django-based-website
This is a fully functional Question and Answer website built using django (python), html, css, javascript.

## Prerequisites
* Python 3.7 (lower versions also work correctly)
* Django 2.0 or higher
* Pillow

## Setting up the project in your system
Download the whole project. You will get a zip file named "Ask-Questions---Django-based-website-master.zip" in your download folder. Extract the file at any location.

## Hosting the website on your system
Now open the terminal and change directory to the location where the project folder is located. Then chage directory using this command
```sh
$ cd Ask-Questions---Django-based-website-master/Project
```
Now to create a localhost in your system use this command
```sh
$ python manage.py runserver
```
The site is now hosted and ready for use. Open your web browser and use the url localhost:8000/

## Some features
- Beautiful GUI.

  <img src="https://github.com/ayushgarg31/Ask-Questions---Django-based-website/blob/master/images/image.JPG" alt="drawing" width="405px"/>
  <img src="https://github.com/ayushgarg31/Ask-Questions---Django-based-website/blob/master/images/profile.JPG" alt="drawing" width="400px"/>
- Only one account on one email and no two users can have same username.
- One can see questions and answers without an account but to post questions and answers one has to log in.
- Only the person who created the question/answer will get the options to update or delete the question/answer.
- Only the person who created the question can accept/unaccept the answer by other users for the question.
- If there is atleast one accepted answer the question will be considered answered and "answers" circle on the home page for the question and the question detail page will turn green.
- Everyone can give only one vote (+ive or -ive) to an answer.
- Once logged in one can access their profile page and edit profile pic and location. Also the page give quick access to all the questions and answers posted using the profile.
- One can open the profile page of any other user using the users page which displays all the users.
- There is also a point system in which user is awarded points for asking questions, answers and also when their answer is accepted. (details on profile page).
- Everywhere the usernames are linked to their profile pages so in case you find a question and want to open the profile page of its user then just click on the name being displayed below the question.
- Points system assign badges to everyone which define their rank and presence on the site. Badge progress are shown on each page after logging in.
- Some efforts have been made to stop hacking.


## Credentials
- Although you can create your own account but here are the credentials of the 2 test profiles.
  > username - abcd
  >
  > password - github1234

  > username - efgh
  >
  > password - efgh
- abcd is the admin account of the site and the admin dashboard can be accessed using the url localhost:8000/admin but I highly recommend not to change anything from the dashboard and also not to create a new admin.
