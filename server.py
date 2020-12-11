import boto3
import requests
import cloudinary as Cloud
from bs4 import BeautifulSoup
from flask_cors import CORS
from flask import Flask, render_template, request

app = Flask(__name__)
CORS(app)

def recipe(dish):
	url = 'https://recipes.timesofindia.com'
	res = requests.get('{}/recipes/{}'.format(url, dish))

	content = res.content
	soup = BeautifulSoup(content, 'html.parser')
	first_recipe_link = soup.find(class_="caption clearfix").h2.a.get('href')

	dish_url = url + first_recipe_link

	res = requests.get(dish_url)
	data = res.content
	soup = BeautifulSoup(data, 'html.parser')

	steps = []

	for step in soup.find_all(class_='story_right'):
		steps.append(step.p.get_text())

	return steps

def detectDish(dish):
	client=boto3.client('rekognition')

	with open(dish, 'rb') as image:
		response = client.detect_labels(Image={'Bytes': image.read()})

	labels = response['Labels']

	if labels[0]['Name'] != 'Food':
		return "I can't recognize this as a food item. Please try again .."

	dishes = []

	for label in labels:
		dish = label['Name']
		if dish == 'Food': continue
		dishes.append(dish)

	return dishes
	
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/upload-image', methods=["POST", "PUT"])
def uploadFile():
	language = request.form.get('nameImage')
	framework = request.form.get('image')
	return '''The language value is: {}
                  The framework value is: {}'''.format(language, framework)


if __name__ == '__main__':
	app.run()





# dish='flask.jpeg'
# dishes = detectDish(dish)
# steps = recipe(dishes[0])

# for i in range(len(steps)):
# 	print('Step {}:'.format(i))
# 	print(steps[i])
# 	print()
