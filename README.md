# Project on Python, PostgreSQL, and Docker

## A few notes on the project

This Project is designed to give you a little overview on how to use Docker containers to save data from Python in a PostgreSQL database, then viewing the contents of the database in pgAdmin4. The entire code can be found in here which will hopefully give you some ideas on how to create similar tasks yourself. You won't need much knowledge on Python, SQL notation or Docker to follow along, but the more you have, the better. The dataset that I used stores information on everything on Netflix, it can be found [here](https://www.kaggle.com/shivamb/netflix-shows). However, you could use any data, created by yourself or not. Working in detail with Python and pandas should not be part of this project.

This README is two-fold. In the beginning, I will show you how to use this specific repository, while in the second part, I will try to get explain the steps that I took to give you a better understanding of the project which will make it easier for you to follow along.  

One of the advantages of Docker is that you can run any container, as long as you have Docker installed. So in order to get started you only need to have Docker installed, an installation guide can be found [here](https://docs.docker.com/get-docker/). If typing
```
$ docker -v
```
into your command line works, you're good to go!

If you want to follow along with the second part of this tutorial, I would recommend you to have [Anaconda](https://www.anaconda.com/products/individual) installed. 

## How to use this Repository

Clone this repository onto your hard drive after navigating into project folder and cd into it. You first need to create a network called postgres by typing
```
$ docker network create -d bridge postgres
```
into your command line. This creates a network that containers can connect to. You could create a network inside the docker-compose file instead (just uncomment the lines that do just that and comment out the network lines above) but if you later want to connect a new container to your postgres server, it won't work that way.

Open the Docker-Compose and change the volume path under your app, i.e. change /absolute/path/to/the/repo/netflix_app to the path of the repository.

Now that the network is set up you can type the following line into your terminal:
```
$ docker-compose up -d
```
to start the postgres and pgAdmin containers. In case you haven't already downloaded the needed images for those containers, docker will pull those from DockerHub which may take a few minutes. 

In addition to the databases docker-compose will also build the app image based on a Python image (again, if you don't have that already, it will be downloaded for you) and create a container from it. If all worked well, you schould see something like 
```
Starting postgres_container ... done
Starting netflix_container  ... done
Starting pgadmin_container  ... done 
```

If you made it this far, congratulations! Your containers were set up correctly. Some reasons for why it might not have worked are that the ports had already been allocated. If you have postgres installed, the default port 5432 is already in use. In that case, open the *docker-compose.yml* file and change the ports of the postgres container and try it again. 5432:5432 could become 5433:5432 for example. If it still won't work, try
```
$ docker-compose up
```
(so omit the -d for detached mode) and find the error message.

Nect, open your Browser and type in **localhost:5050**. It needs a few seconds to set up (so keep refreshing if it doesn't work the first time) and then you should see the starting page for pgAdmin4. Type in a password of your choice (remember it or else you need to start the container again!) then click on **add new server**. You can name the serve anything you like, the more important part is the tab *connection*. You have to specify your host, which can be a service name as well. Thus you can type in the name of the postgres container which has creatively been named *postgres_container* (See the top of the *docker-compose*). 

The information on the port, database name, user and password can directly be taken from the connection string in our *main.py* file. This makes sense because the python app needs to connect to the postgreSQL database with the same credentials as pgAdmin. Looking into the *docker-compose.yml* you can see where the environment variables were defined as:

- **Port**: 5432
- **Maintenance database**: test_netflix
- **Username**: user_net
- **Password**: password_net

If you save this connection and don't get an error message, you successfully connected the postgreSQL Server with pgAdmin and you can now view your database. Just open *Servers > YourServerName > test_netflix > Schemas > Tables* on the left side (Phew, that's a lot of subdirectories!). Then right-click on your table (which should be called *netflix_data*) and click refresh to load the newest data. By right-clicking on *netflix_data* again and selecting View/Edit you can take a look at your table and modify it using SQL queries.

## Tutorial: Setting up the Project yourself

Will follow...