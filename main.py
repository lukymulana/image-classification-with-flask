import os
from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from keras_preprocessing import image

model = load_model('waste_management_model.h5')

UPLOAD_FOLDER = './static/images/upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        splitName = file1.filename
        ext = splitName.split(".")
        nameFile = "asd."+ext[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], nameFile)

        file1.save(path)

        img = image.load_img(path, target_size=(150, 150))
        imgplot = plt.imshow(img)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = model.predict(images)

        print(path)
        print(classes)
        ket = ""
        desc = ""

        if classes[0][0]:
            print("Organic")
            ket = "Organic"
            desc = "Composting is a managed process which utilizes microorganisms naturally present in organic matter and soil to decompose organic material. These microorganisms require basic nutrients, oxygen, and water in order for decomposition to occur at an accelerated pace. The end-product, compost, is a dark brown, humus-like material which can be easily and safely handled, stored, and used as a valuable soil conditioner. The composting process is dependent upon several factors, including: the population of microorganisms, carbon to nitrogen ratio, oxygen level, temperature, moisture, surface area, pH, and time."
        elif classes[0][1]:
            print("Rec")
            ket = "Recyclable"
            desc = "Many pesticide labels will have instructions for proper disposal. If you are not able to use the pesticide according the label because it is too old and/or no longer legal to use, the pesticide is considered hazardous waste.  The Massachusetts Department of Agricultural Resources has held many subsidized collection events in the past.  Also, individual communities throughout Massachusetts have annual household hazardous waste collection events.  If you are not able to participate in these types of events, then you will have to contact a licensed hazardous waste hauler company."
        return render_template('result.html', user_image=path, kind=ket, description=desc)
