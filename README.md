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


-> Get All movies in the DB(for all users) <br/>
-> Search movies by name (for all users) <br/>
-> Search movie by ID (admin only) <br/>
-> Add a movie (admin only) <br/>
-> Update a movie (admin only) <br/>
-> Delete a movie (admin only) <br/>

2 levels of access is there -> user and admin <br/>

For testing all the above APIs you can do the following : <br/>

First of all you need to login : for that we have two options(admin/user) <br/>

-> For login -> make a post request to url :  /login with username and password as form data <br/>

After that you can make request according to the permissions for your role(admin/user) <br/>

-> For Getting All movies in the DB -> make a get request to the url :  /api/movies <br/>
-> For searching movie by name in the DB -> make a post request to /api/movies/searchMovie with form data field “movie_name” <br/>
-> For searching single movie by id -> admin can make a get request to url : /api/movies/{movie_id} <br/>
-> For adding a movie -> admin can make a post request to url : /api/movies/add with form data field : “movie_details” , also movie details should be a json format string <br/>
-> For updating a movie -> admin can make a put request to url : api/movies/{movie_id} <br/>
with updated details in json format in request body <br/>
-> For deleting a movie -> admin can make a delete request on url : /api/movies/{movie_id} <br/>
