# Architecture

- [Architecture](#architecture)
  - [Intro](#intro)
  - [Application architecture](#application-architecture)
  - [app.py file](#apppy-file)
  - [vmanify_picture class](#vmanify_picture-class)
    - [Properties](#properties)
    - [Methods](#methods)
      - [__process_picture() method](#__process_picture-method)
      - [process_uploaded_picture() method](#process_uploaded_picture-method)
      - [process_url() method](#process_url-method)
      - [cleanup_pictures() method](#cleanup_pictures-method)

## Intro

The VMagnify application is a server software designed to communicate with the user browser via HTTP.

[!Global Architecture](Global_Architecture.png)

## Application architecture

The application is composed of 4 source files :

[!Application Architecture](Application_Architecture.png)

1. app.py is the main application file.
2. vmanify.py is an abstract class to share code between picture and video processings.
3. vmanify_picture.py is the class for picture processing.
4. vmanify_picture.py is the class for video processing.

## app.py file

app.py is the main file of the application, it contains all the route of the application.

The form of the picture processing contains 4 routes :

1. Load URL button route
2. Load Disk button route
3. Zoom slider route, by default, this road shall be disabled and enabled when the processing of the image is finished.
4. Close of the connection route

## vmanify_picture class

The vmanify_picture is the class for picture processing.

### Properties

The class has 4 properties, all are of the type Mat :

1. original_picture : original picture of the user
2. x2_zoom_picture : picture processed with a X2 zoom
3. x3_zoom_picture : picture processed with a X3 zoom
4. x4_zoom_picture : picture processed with a X4 zoom

They have as goal to contain the result of the processing to permit to switch between pictures fastly.

### Methods

The class has 9 methods, in Python methods which start with __ are private :

1. __delete_picture(file : string)
2. __download_url_content(url:string) : string,bool
3. __process_picture(file : string)
4. __upload_picture() : string,bool
5. __validate_picture(file : string) : bool
6. __validate_url(url:string) : bool
7. cleanup_pictures()
8. process_uploaded_picture() : bool
9. process_url(url:string) : bool

#### __process_picture() method

__process_picture() method is responsible of the read of the input picture and the process of the 3 zoomed pictures.
The input of the method is the file path of the picture.

[!__process_picture()](__process_picture().png)

#### process_uploaded_picture() method

process_uploaded_picture() method is responsible of the upload of the user picture and the process of it.

[!process_uploaded_picture()](process_uploaded_picture().png)

The functions called by the method are :

1. __upload_picture() : string,bool : this function is responsible of the upload of the picture of the user on the server. It returns the file path and the status of the upload, True in case of success.
2. __validate_picture (file : string) : bool : this function is responsible of the test of the validity of the picture, more informations in [Specifications](../Specifications/Specifications.md). It returns True in case of success.
3. __process_picture(file : string) : see the chapiter of __process_picture() method above.
4. __delete_picture() : this function deletes the user file in case of failure during the upload or the validation of the picture.

#### process_url() method

process_url() method is responsible of the download of the url of the user and the process of it.

[!process_url()](process_url().png)

The functions called by the method are :

1. __validate_url(url:string) : bool : this function is responsible of the test of the validity of the URL of the upload, more informations in [Specifications](../Specifications/Specifications.md). It returns True in case of success.
2. __download_url_content() : string,bool : this function is responsible of the download of the picture in the URL on the server. It returns the file path and the status of the upload, True in case of success.
3. __validate_picture (file : string) : bool : this function is responsible of the test of the validity of the picture, more informations in [Specifications](../Specifications/Specifications.md). It returns True in case of success.
4. __process_picture(file : string) : see the chapiter of __process_picture() method above.
5. __delete_picture() : this function deletes the user file in case of failure during the upload or the validation of the picture.

#### cleanup_pictures() method

The cleanup_pictures() method is responsible of the free of the memory used by the pictures when the user disconnects from the server.
