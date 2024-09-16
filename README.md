##Instructions to run the dockerized application
I have used the WIDER FACE Dataset. Unfortunately, I couldn't unzip the dataset using the URL. I have downlaoded the dataset and unzipped from the local.

docker build -t yolo-face-detector .

docker run yolo-face-detector <url_or_local_path_to_zip> <person_name>
