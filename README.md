# Deployed Live Travel Advisor

## Motivation

I built this non-Commercial web app for my Duke project. What it  does is that it listens to you and provides top 10 travel listing based on your criterias. The app itsels has been designed in a way that users can easily navigate around. It is a simple app but really brings the most suitable hotels (flights and other travelling parameters will be added later) to your convenience just by listening. Hence, this app can be quite friendly for people who don't wanna spend too much time on typing and understanding the working mechanism of the currently available travel management websites. This robotic approach in services is most likely going to be the future in most service sectors soon. I'm using API to call the most up-to-date information available on internet. 

## How it works?

The application listens to you and brings top 10 hotels' key details based on your criterias. The currently accepted criterias are the following:

- ascending/descending stars
- popularity 
- distance to the center
- reviews
- price

The users are asked to include the check-in and check-out dates, also the number of persons and the location for booking in their voice recordings.    
The results become available within few seconds after recording is stopped.

## Frontend 

HTML, CSS, JavaScript for managing the buttons and UI

## Backend

I used a pre-trained deep learning model, [Facebook's Wav2Vec2](https://huggingface.co/facebook/wav2vec2-base-960h) for turning the speech into transcripts. For the most logic, I used Python Flask functions to implement the functionality along with the NLP best practices. Here is the quick overview of the workflow:

<p align="center">
  <img src="https://user-images.githubusercontent.com/53462948/184711401-d041fe5b-18cc-4b2a-959a-e8efed3883a8.png" />
</p>


## Deployment

AWS ECR (Amazon Elastic Container Registry) is a professional container registry offering high-performance hosting, where I'm also hosting my Docker image. I also used AWS ECS (Amazon Elastic Container Service) to orchestrate my Docker container and successfully run my application on AWS EC2 (Amazon Elastic Compute Cloud). Broadly speaking, I pushed docker image to AWS ECR  and from there I used ECS to deploy my app into EC2 instance as described in the diagram below:

![Unknown](https://user-images.githubusercontent.com/53462948/184713454-1eec2e95-53ef-4f57-97d1-7596ba704e04.png)

Deployed app link: [AWS EC2 link](http://ec2-34-226-190-87.compute-1.amazonaws.com/)


## Collaboration

I'm still trying to improve this app, and add more functionality. Please, feel free  to contribute if you're interested. Commands to run to start:

- Install the required packages
```
make install
```

- Run the app

```
python3 app.py
```

## Demo for the app

### Home page

<img width="1433" alt="1" src="https://user-images.githubusercontent.com/53462948/184707843-7415b4aa-4378-4db1-9bbc-f5e07693bc7f.png">

### The results

<img width="1432" alt="2" src="https://user-images.githubusercontent.com/53462948/184707877-f35b1021-160b-4ff5-8158-cc0615f7f215.png">

### Access the results

<img src="https://user-images.githubusercontent.com/53462948/184708491-8c0ee600-9058-4c25-9cf4-ae2c88e73346.gif" width="800" height="450"/>


### Error handling

<img src="https://user-images.githubusercontent.com/53462948/184709082-347614ee-d621-4288-8a6c-d5808ab5eda3.gif" width="800" height="450"/>



