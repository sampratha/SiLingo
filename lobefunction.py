import base64
import requests

# Save string of image file path below

def predictcnn(img_filepath):
    # Create base64 encoded string
    with open(img_filepath, "rb") as f:
        image_string = base64.b64encode(f.read()).decode("utf-8")

    # Get response from POST request
    response = requests.post(
        url="http://localhost:38101/v1/predict/683669f0-25a9-470b-bbde-d98ade7097c9",
        json={"image": image_string},
    )
    data = response.json()
    print(data)
    top_prediction = data["predictions"][0]

    # Print the top predicted label and its confidence
    print("predicted label:\t{}\nconfidence:\t\t{}"
          .format(top_prediction["label"], top_prediction["confidence"]))
    return top_prediction["label"]

