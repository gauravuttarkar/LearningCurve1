import requests

url='https://maps.googleapis.com/maps/api/distancematrix/json'

payload={
	'origins':'Boston,MA',
	'destinations':'Lexington,MA',
	'key':'AIzaSyCSvYPh9cC2oAzADo7taRjSziWqo8gj258',
	'departure_time':'now'
}
r = requests.get(url, params=payload)
results = r.json()
print(results)
print(results['rows'][0]['elements'][0]['distance']['text'])
print(results['rows'][0]['elements'][0]['duration']['text'])