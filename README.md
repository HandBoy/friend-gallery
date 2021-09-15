# friend-gallery

The Problem: Friend's gallery

You got a request from a friend to create a gallery for his wedding where his friends will be able to upload their photos and he will have a unified gallery with all friend's photos.
He wants to be able to approve the photos before being visible to everyone. He and his wife should be the only ones able to approve new photos.
Users must be able to like photos and add comments to photos.

## Links
- [Documentation](https://HandBoy.github.io/friend-gallery/)
- [Project Online](https://friend-gallery.herokuapp.com/)

## Setup Development to run the project
```shell
# Clone the project
$ git clone https://github.com/HandBoy/friend-gallery.git

# Create Virtual Env.
$ python3 -m venv venv-friend  

# Activate Virtual Env.
$ source venv-friend/bin/activate

# Install Requirments.
$ pip install -r requirements/dev.txt

# create .env file and past the values sended for you email.
$ cp .env.template .env

# Run the project.
$ flask run

 * Serving Flask app 'gallery/app.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with watchdog (inotify)
 * Debugger is active!
 * Debugger PIN: 796-444-423
```

### Documentation
```shell
# Run and access Mkdocs
$ mkdocs serve

INFO     -  Building documentation...
INFO     -  Cleaning site directory
INFO     -  Documentation built in 0.30 seconds
INFO     -  [19:46:59] Serving on http://127.0.0.1:8000/
INFO     -  [19:46:59] Browser connected: http://127.0.0.1:8000/

# Deploy documentation
$ mkdocs gh-deploy
```

### Testes

```shell
# Run all tests
$ pytest

# Run all tests with coverage
$ pytest --cov=gallery

$ pytest --cov-report term-missing --cov=gallery

$ pytest --cov-report html --cov=gallery

# Run all the tests in a particular test file
$ pytest tests/fields/test_fields.py

# Run only particular test class in that file
$ pytest tests/fields/test_fields.py::TestField
```

## Project Struture
The project use the MVC to share as responsibilities:
- Model: Contains all documents salved in MongoDB, file: documents.py  
- Views: Contains all endpoints, file: resources/views.py
- Controllers: Contains the business logic, file: controllers/*py

Below we have a explanation about all project files:
```
├── docs/                            Project Documentation
├── gallery/                         Application(a documented folder)
│   ├── controllers/                 Contains the business logic
│   │   ├── gallery_controller.py 
│   │   ├── picture_controller.py 
│   │   └── user_controller.py 
│   ├── ext/                         Init external Apps
│   │   ├── auth.py 
│   │   ├── database.py 
│   │   ├── s3.py 
│   │   └── serializer.py 
│   ├── resources/                   Api Views and Serializers
│   │   ├── serializers/             In and Outbouds Schemas 
│   │   └── views.py                 Endpoints
│   ├── tests/                       Tests Files
│   ├── app.py                       Creat Flask App
│   ├── config.py                    Environment variables
│   ├── documents.py                 MongoDB Documents
│   └── exceptions.py                Friend Gallery exceptions 
├── requirements/                    Requirements to run the project
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── mkdocs.yml                       Mkdocs init  
├── Procfile                         Heroku 
├── README.md (The main readme)
├── requirements.txt                 Used by Heroku to install requirements
└── wsgi                             Used by Heroku to run application
```

## Tasks
- [x] Create a User.
- [x] Authenticate a User.
- [x] Create a gallery.
- [x] Send photo from a gallery.
- [X] He and his wife should be the only ones able to approve new photos.
- [x] Approve Photos.
- [X] Friends will be able to upload their photos.
- [x] List photos only approved.
- [ ] Add a comment in photo.
- [x] Like a photo.
- [x] Paginate photos.
- [x] Send photo from AWS.
- [x] Send to production.
- [x] Mkdocs for document the Api.
- [ ] Docker.
- [x] Split domain.
- [x] Estruturar o Readme.
- [ ] Add MakeFile.
- [ ] Improve Coverage.


# Links
- (Code Documentation of the Future — MkDocs-Material Tutorial)[https://ahmed-nafies.medium.com/code-documentation-of-the-future-mkdocs-material-tutorial-35e5176d974f]
- (Desmistificando JWT e Refresh token)[https://medium.com/qualyteam-engineering/jwt-refresh-token-b79440a239]


    @staticmethod
    def approve_picture(gallery_id, user_id, picture_id, status=True):
        can_approve = GalleryModel.objects(
            _id=gallery_id, can_approve__in=[user_id]
        )

        if not can_approve:
            return False

        picture = can_approve.get().pictures.filter(id=picture_id)
        picture.get().approved = status
        picture.save()

        return True
    

    @staticmethod
    def like_picture_by_id(gallery_id, picture_id):
        try:
            picture = (
                GalleryModel.objects(_id=gallery_id)
                .get()
                .pictures.filter(id=picture_id)
            )
            picture.get().likes += 1
            picture.save()
            return True
        except (DoesNotExist, ValidationError):
            return False