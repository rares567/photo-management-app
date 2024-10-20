# Photo Management App

### To build and run the website, make sure [Docker](https://www.docker.com/) is installed and run:
`docker build -t *NAME* .`

`docker run -p 5000:5000 -it *NAME*`
### Then, the website can be accessed through https://localhost:5000/

## Functions:
- Login in to be able to upload images (username: admin, password: secret). Each image will have to be assigned to a category to be displayed prorperly on the main page
- Create thumbnails for each image automatically so that it can be shown on the main page (clicking on the image will open it in original quality)
- Visualise photos uploaded through admin (even if not logged in) split into categories
