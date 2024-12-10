from flask import Flask, request, jsonify
import os
import tempfile
from ImageDetection.script import pipeline as detection_pipeline
from Odometer.odo_script import pipeline as odometer_pipeline
from PriceEstimation.script import piepline as price_pipeline
from DamageDetection.script import pipeline as damage_pipeline


app = Flask(__name__)

@app.route('/image_detection', methods=['POST'])
def image_detection():
    if 'images' not in request.files or len(request.files.getlist('images')) != 6:
        return jsonify({'error': 'Exactly 6 images are required (4 for detection, 1 for odometer, 1 for metadata).'}), 400
    
    # print("Request Files:", request.files)  # Debug: See what Flask receives
    # if 'images' not in request.files:
    #     return jsonify({'error': 'No files uploaded under the key "images".'}), 400
    
    # files = request.files.getlist('images')
    # print(f"Uploaded {len(files)} files.")  # Debug: Check file count

    # if len(files) != 6:
    #     return jsonify({'error': 'Exactly 6 images are required (4 for detection, 1 for odometer, 1 for metadata).'}), 400

    # Save images temporarily
    files = request.files.getlist('images')
    temp_dir = tempfile.mkdtemp()
    image_paths = []
    
    try:
        for i, file in enumerate(files):
            temp_path = os.path.join(temp_dir, f'image_{i}.jpg')
            file.save(temp_path)
            image_paths.append(temp_path)
        
        # Separate images for pipelines
        detection_images = image_paths[:4]  # First 4 images
        odometer_image = image_paths[4]    # Fifth image
        metadata_image = image_paths[5]    # Sixth image (not used, just for aesthetics)

        # Run pipelines
        make, model, variant, year, cc, type, trans, city = detection_pipeline(detection_images)
        damage_count, con = damage_pipeline(detection_images)
        odometer_reading = odometer_pipeline(odometer_image)
        
        con_year = (2024 - int(year)) * 0.005    # Penalizing based on year (0.5% Condition degrade per year)
        condition = min(con, con - con_year) 

        return jsonify({
            'Make': make,
            'Model': model,
            'Variant': variant,
            'Year': int(year),
            'Mileage': int(odometer_reading),
            'Engine Capacity': int(cc), 
            'Engine Type': type,
            'Transmission': trans,
            'Registered City': city,
            'Condition': float(condition * 100)
        })
    finally:
        for path in image_paths:
            if os.path.exists(path):
                os.remove(path)
        os.rmdir(temp_dir)


@app.route('/price_estimation', methods=['POST'])
def price_estimation():
    required_fields = [
        'make', 'model', 'variant', 'year', 
        'mileage', 'engine_cc', 'engine_type', 
        'transmission', 'reg_city', 'condition'
    ]
    
    # Validate request JSON
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request must be in JSON format.'}), 400
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # Extract input features and enforce integer conversion
    try:
        year = int(data['year'])
        mileage = int(data['mileage'])
        engine_cc = int(data['engine_cc'])
    except ValueError as e:
        return jsonify({'error': 'Invalid input: year, mileage, and engine_cc must be integers.'}), 400
    
    # Extract input features
    make = data['make']
    model = data['model']
    variant = data['variant']
    year = data['year']
    mileage = data['mileage']
    engine_cc = data['engine_cc']
    engine_type = data['engine_type']
    transmission = data['transmission']
    reg_city = data['reg_city']
    condition = float(data.get('condition', 100))

    try:
        # Run the price pipeline
        predicted_price = price_pipeline(
            make, model, variant, year, mileage, 
            engine_cc, engine_type, transmission, reg_city
        )
        price = (condition/100)*predicted_price
        return jsonify({'Predicted Price': int(price)})
    
    except Exception as e:
        return jsonify({'error': f'Error occurred during prediction: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    # app.run(debug=True)
