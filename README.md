# Milestone 3 Project of Seán Carley
## Bucket Lists

### Technologies
1. HTML - Used to define the structure of webpages
1. CSS - Used to style web pages
1. Bootstrap - Framework to simplify webpage design
1. Python - Python is a programming language that lets you work more quickly 
    and integrate your systems more effectively.
1. Flask Framework - lightweight WSGI web application framework.
1. MongoDB - general purpose, document-based, distributed database

### Chosen Idea: Website to store users lists
#### Site Owner:
As the developer of this site, I want a site that meets the criteria for a
project assigned for the completion of an Data-Centric Milestone Project. The
site should allow the users to create a list of media that they would like to
consume. The list will contain various info about the list itself and about the
individual entries.

### User Stories
The below user stories are for the website Bucket Litsts. This purpose of the site
is to allow users to be able to create, edit, and view lists and be ale to keep
track of the entries on the list.

#### Home Page
* As a user of this site, I want the Home page to provide information to what the 
site is about. The information should be concise, so as to not be a distraction for 
repeat users, but informative so that new users can get the required information to 
use the site.
* As a user of this site, I want the Home page to provide a list of the content of 
the site. There should also be some limited information for each of the entries of 
the list (eg: list category, list author, last updated).
* As a user of this site, I want the Home page to provide the means to navigate the 
site. The list entries should jump to the relevant list. The Nav Bar should provide 
the option to jump to regularly used pages.
* As a user of this site, I want the Home page to provide information about the 
developer and the means to view their social media.

#### Home Page - List Details Page
* As a user of this site, I want the Home page - List Details to provide the list of 
lists. The list of lists again should provide limited information of each list (eg: 
the list title, list category).
* As a user of this site, I want the Home page - List Details to provide the means 
to add to the list, edit the list information, delete the list.
* As a user of this site, I want the Home page - List Details to show the items of 
the list. Each list item should also provide all the relevant information for it 
which is the information from the user. It should also get some general information 
which is not input by the user.

#### Create List Page
* As a user of this site, I want the Create List page to provide the means to create a 
new list
* As a user of this site, I want the Create List page to allow me enter a list title, 
the list author and the category.
* As a user of this site, I want the Create List page to allow me input items to be added
the new list.

#### Add Items Page
* As a user of this site, I want the Add Items to show the list information just 
entered. I also want the date and time of the last edit to the list to be displayed.
* As a user of this site, I want the Add Items to provide the fields to input the relevant
information, the fields should be relevant to the category chosen in the Create List page.
* As a user of this site, I want the Add Items page to allow entering further items or to 
finish and return to the Home Page.

#### Add Items Page
* As a user of this site, I want the Add Additional Items page to allow me to add additional 
items to an existing list.
* As a user of this site, I want the Add Additional Items page to show information of the list, 
existing items, and items that were just added.
* As a user of this site, I want the Add Items page to allow entering further items or to 
finish and return to the Home Page.

### Deployed site
The site was developed, for the most part by using Atom text editor with a number of add-ons for 
HTML, CSS, and Python on a Ubuntu machine. GitPod was also used when working when access to this machine 
was not available. This site is version controlled via GitHub, and 
deployed via Heroku. The link to the deployed site is 
[https://seans-wishlist-app.herokuapp.com/](https://seans-wishlist-app.herokuapp.com/). The deployment 
to heroku was done using the Heroku CLI. There were no additional configuration changes made to Heroku. 
MongoDB was used as the database solution. The environment variables are stored in the env.py.

### Credits
The Nav Bar used was obtained from the W3Schools web site at this link 
[https://www.w3schools.com/bootstrap4/bootstrap_navbar.asp](https://www.w3schools.com/bootstrap4/bootstrap_navbar.asp)

```html
<nav class="navbar navbar-expand-md bg-dark navbar-dark">
<!-- Brand -->
    <a class="navbar-brand" href="{{ url_for('home') }}">Bucket Lists</a>
<!-- Toggler/collapsibe Button -->
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
        <span class="navbar-toggler-icon"></span>
    </button>
<!-- Navbar links -->
    <div class="collapse navbar-collapse" id="collapsibleNavbar">
<!-- added ml-auto to right align the menu on desktop -->
        <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('home') }}">
                    <i class="fa fa-home" aria-hidden="true"></i> Home
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('create') }}">
                    <i class="fa fa-sign-in-alt" aria-hidden="true"></i> Create list
                </a>
            </li>
        </ul>
    </div>
</nav>
```

Further learning relating to Flask was obtaind from numerous sources, mainly [https://flask.palletsprojects.com/en/1.1.x/](https://flask.palletsprojects.com/en/1.1.x/)  
[Stack Overflow](https://stackoverflow.com/) amongst others were used to assist in trouble-shooting, and expanding ideas.