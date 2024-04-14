Code related to the web app goes in this folder.
In 4-Containerized-APP-exercise so the root directory:
docker build -t webapp ./web-app
docker run --name my-webapp -p 5000:5000 --env-file ./web-app/.env webapp


To stop container: 
docker stop my-webapp
docker rm my-webapp