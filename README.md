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

To make sure the containers are running properly, type 
```
$ docker ps -a
```
into the command line and check wether all three are up and receive connections at specific ports.

Next, open your Browser and type in **localhost:5050**. It needs a few seconds to set up (so keep refreshing if it doesn't work the first time) and then you should see the starting page for pgAdmin4. Type in a password of your choice (remember it or else you need to start the container again!) then click on **add new server**. You can name the serve anything you like, the more important part is the tab *connection*. You have to specify your host, which can be a service name as well. Thus you can type in the name of the postgres container which has creatively been named *postgres_container* (See the top of the *docker-compose*). 

The information on the port, database name, user and password can directly be taken from the connection string in our *main.py* file. This makes sense because the python app needs to connect to the postgreSQL database with the same credentials as pgAdmin. Looking into the *docker-compose.yml* you can see where the environment variables were defined as:

- **Port**: 5432
- **Maintenance database**: postgres
- **Username**: username
- **Password**: password

If you save this connection and don't get an error message, you successfully connected the postgreSQL Server with pgAdmin and you can now view your database. Just open *Servers > YourServerName > test_netflix > Schemas > Tables* on the left side (Phew, that's a lot of subdirectories!). Then right-click on your table (which should be called *netflix_data*) and click refresh to load the newest data. By right-clicking on *netflix_data* again and selecting View/Edit you can take a look at your table and modify it using SQL queries.

## Tutorial: Setting up the Project yourself

#### Setting up the network

At first, we need to create our database. We are going to use PostgreSQL for that, as well as pgAdmin4 in order to be able to view the data. Both of these steps can be done in a docker-compose file similar to the one in the project. However, everything created in a docker-compose is closed in itself. Therefore, we need to create a network first, that several services can connect to. We can create a bridge terminal called postgres by typing into our terminal
```
$ docker network create -d bridge postgres
```
Now, whenever we create a new service in a completely different docker-compose, we can simply connect to that network and all the services that are already inside it. All you need to do is load the network in the *docker-compose.yml* with
```
networks:
  postgres:  # name we are using inside this docker-compose
    external:
      name: postgres  # name outside the docker-compose
```


#### Setting up the PostgreSQL server

If you take a look into the *docker-compose.yml* file that comes with this repo you are going to find a section near the very top that builds the DB server. I'm going to go through each parameter so you can create a similar project on your own
- **container_name** This is the name we are giving the container, so we can easily find or stop it in the terminal
- **image** This is the image we are using to build this server. You could use a specified version of postgres, as well (depending on the project, this could be helpful, especially when working in a team). In case you don't have the image yet, it will be downloaded automatically.
- **ports** Here we define the port of the container. The port is going to be used to communicate with the server. We are going to use the standard port for Postgres (5432), so a service can communicate with it (in order to retrieve or store data) by communicating with port 5432 in our network.
- **environment** Unlike the variables before, the environment is specific to PostgreSQL. We define the user with password, as well as the name of the database. Later when we want to store data from our Python container in the server, these are important. The last environment variable PGDATA is for storage.
- **volumes** This variable is crucial if your server is not running continuously. If you didn't define a volume, your database would be empty everytime you restart your computer. I created a directory *$HOME/docker/volumes/postgres* on my local machine that the container is allowed to access and store the data from inside the container in it. For every restart, it will look what it can find in this folder. Inside the container, the default storage place is */var/lib/postgresql/data*.
- **networks** In here we are using the network we created before: *postgres*. We could connect our server to multiple networks using multiple dashes but in our small example, one network is enough.
- **restart** This tells the container when to restart. Some options here are *on-failure*, *always* or *unless-stopped*. We are using the last one because that way it restarts once your computer is rebooted.

#### Setting up pgAdmin4

Several of th variables used for the PostgreSQL container are also being used in here. We give it a name, tell it what image, network and port to use and what volume it can store the data in. We also have environmental variables in here but they are not as important as above.

We are going to use the standard port for pgAdmin4 which is 5050. Therefore - after running the docker-compose up command - we can open it by typing **localhost:5050** into our browser. Next, you want to click on "Add New Server" and type in the environment variables of the Postgres server and you're done!

#### Creating the Python App

So far we have accommodated for the PostgreSQL Server and the visualization tool. Next, we want to store data in the database to demonstrate that the connection works.

To be continued ... :)