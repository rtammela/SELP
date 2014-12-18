SELP
====
Git repository: contained at root level of the SELP folder submitted.
Project reposrt: contained at root leve; Report.pdf.

Installation & setup
====
Commands necessary:
pip install django  (if not already installed)
From git repository root folder:
cd \sitecode
python manage.py migrate

Local deployment
===
From git repository root folder:
cd \sitecode
python manage.py runserver

Source code structure
===
\sitecode\guessing contains the views, urls, forms and models; these provide the majority of the site's functionality.
\sitecode\guessing\templates\guessing contains HTML code associated with each view, with base.html as the template for each.
\sitecode\guessing\static contains the CSS file applied to the HTML pages, and is where any static files would go.

Site usage
===
Once the site has been deployed locally, the admin page is located at 127.0.0.1:8000/ (or whichever port is used).
This can be accessed with:
  username: admin
  password: admin
and provides tools to manage the database contents.

The admin account can be used within the site: 127.0.0.1:8000/guessing/
to set the winners for matches.

Non-staff accounts can be freely registered, and used to create matches and vote.

