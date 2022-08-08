# Deployed Live Hotel Advisor

Deployed app link: [AWS EC2 link](http://ec2-34-226-190-87.compute-1.amazonaws.com/)

## Motivation
I built this non-Commercial web app for my Duke project. What it  does is that it listens to you and provides top 10 travel listing based on your criterias. The app itsels has been designed in a way that users can easily navigate around. It is a simple app but really brings the most suitable hotels (flights and other travelling parameters will be added later) to your convenience just by listening. 

## Backend

I used a pre-trained deep learning model, [Facebook's Wav2Vec2](https://huggingface.co/facebook/wav2vec2-base-960h) for turning the speech into transcripts. For the most logic, I used Python Flask to implement the functionality.

## Frontend 

HTML, CSS, JavaScript for managing the buttons

## Deployment

I pushed docker image to AWS ECR  and from there I used ECS to deploy my app into EC2 instance. 

## Collaboration

Feel free to contribute if you're interested. Commands to run to start:

```
make all
```
```
python3 app.py
```

### Future work

I'm still working on this app to make it more comprehensive and bug free. I'll continue adding the details.

(I'll add some detailed pictures for the whole process here later)
