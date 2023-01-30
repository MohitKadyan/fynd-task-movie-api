Steps to start the server locally:
1. Install the dependencies in requirements.txt using the following command:
```
pip install -r requirements.txt 
```

2. Run this command to start the server
```
py _init_.py
```
3. Admin credentials to login :
Username : mohit@kadyan.com
Password : abc456

4. Non-admin credentials to login : 
Username : akash@gupta.com
Password : abc123

5. Features of API and how to use:


-> Get All movies in the DB(for all users)
-> Search movies by name (for all users)
-> Search movie by ID (admin only)
-> Add a movie (admin only)
-> Update a movie (admin only)
-> Delete a movie (admin only)

2 levels of access is there -> user and admin

For testing all the above APIs you can do the following : 

First of all you need to login : for that we have two options(admin/user)

-> For login -> make a post request to url :  /login with username and password as form data

After that you can make request according to the permissions for your role(admin/user)

-> For Getting All movies in the DB -> make a get request to the url :  /api/movies
-> For searching movie by name in the DB -> make a post request to /api/movies/searchMovie with form data field “movie_name”
-> For searching single movie by id -> admin can make a get request to url : /api/movies/{movie_id}
-> For adding a movie -> admin can make a post request to url : /api/movies/add with form data field : “movie_details” , also movie details should be a json format string
-> For updating a movie -> admin can make a put request to url : api/movies/{movie_id}
with updated details in json format in request body
-> For deleting a movie -> admin can make a delete request on url : /api/movies/{movie_id}
