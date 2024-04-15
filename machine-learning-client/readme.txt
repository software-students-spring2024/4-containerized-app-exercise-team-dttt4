Code related to the machine learning client goes in this folder.
Running Docker container and script:
pipenv lock
docker build -t ml-client .
docker run --name ml-client ml-client

docker cp ml-client:/app/output_audio.wav /Users/denizqian/Desktop/Software Engineering/4-containerized-app-exercise-team-dttt4/machine-learning-client/audio

docker rm ml-client

