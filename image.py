import requests

prompt="Ronaldo winning the world cup in 2022,along with the portugal fooball team, in a stadium full of fans, with fireworks in the background, cinematic lighting, 8k resolution, ultra realistic, trending on artstation"

url=f"https://image.pollinations.ai/prompt/{prompt}"


print("Generating image from prompt...")
response = requests.get(url)
print(response)
if response.status_code == 200:
    with open("GOAT.png","wb") as file:
        file.write(response.content)
    print("Image generated successfully!")
else:
    print("Failed to generate image. Status code:", response.status_code)
