"""
This is where the routes are defined. 
It may be split into a package of its own (yourapp/views/) with related views grouped together into modules.
"""

from flask import render_template, Blueprint, redirect, url_for, request, current_app, session, jsonify
from flask_mail import Message
from flask_login import current_user
from ..forms.auth import LoginForm
from ..forms.contact import ContactForm
from ..forms.photos import PhotoForm

from werkzeug.utils import secure_filename
from app import mail

import json
import os


AHB = Blueprint('AHB', __name__)

@AHB.route('/')
@AHB.route('/home')
def index():
    with open('json/slideshow.json') as f:
        data = json.load(f)
    slides = data.get('slides', [])

    with open('json/instagram.json') as f:
        data = json.load(f)
    instagram_posts = data.get('instagram', [])

    form = ContactForm()

    if current_user.is_authenticated:
        print("logged in")
    else:
        print("logged out")


    return render_template('1_HOME/index.html', slides=slides, instagram_posts=instagram_posts, form=form)


@AHB.route('/')
@AHB.route('/services')
def services():
    with open('json/services.json') as f:
        data = json.load(f)
    services = data.get('services', [])

    with open('json/reviews.json') as f:
        data = json.load(f)
    reviews = data.get('reviews', [])

    with open('json/instagram.json') as f:
        data = json.load(f)
    instagram_posts = data.get('instagram', [])

    form = ContactForm()

    return render_template('2_SERVICES/services.html', services=services, reviews=reviews, instagram_posts=instagram_posts, form=form)


@AHB.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    with open('json/portfolio.json') as f:
        data = json.load(f)
    portfolio = data.get('portfolio', {})

    with open('json/instagram.json') as f:
        data = json.load(f)
    instagram_posts = data.get('instagram', [])

    form = PhotoForm()
    if form.validate_on_submit():
        files = request.files.getlist('photos')  # Get list of files
        residence_name = request.form.get('name').title()

        # Determine the project directory
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Create the upload path with the folder name
        portfolio_upload_path = os.path.join(app_dir, 'static', 'images', 'portfolio', residence_name)

        # Ensure the directory exists, create if it doesn't
        if not os.path.exists(portfolio_upload_path):
            os.makedirs(portfolio_upload_path)
            print(f"Directory created: {portfolio_upload_path}")
        else:
            print(f"Directory already exists: {portfolio_upload_path}")

        # Check if the residence_name already exists in the portfolio
        if residence_name in portfolio:
            # If it exists, get the current photos list
            photos = portfolio[residence_name]['photos']
        else:
            # If it doesn't exist, create a new entry
            photos = []
            portfolio[residence_name] = {
                "photos": photos
            }

        # Add files to folder and update the JSON data with filenames
        for idx, file in enumerate(files, start=(0 if not photos else int(photos[-1][0]))+1):
            if file:
                filename = f"{idx}_{secure_filename(file.filename)}"
                file_path = os.path.join(portfolio_upload_path, filename)
                file.save(file_path)
                photos.append(filename)  # Add filename to the photos list

        # Update the portfolio JSON file with the modified data
        with open('json/portfolio.json', 'w') as f:
            json.dump({"portfolio": portfolio}, f, indent=4)

        return redirect(url_for('AHB.portfolio'))  # Redirect after upload

    return render_template('3_PORTFOLIO/portfolio.html', portfolio=portfolio, instagram_posts=instagram_posts, form=form)



@AHB.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for('AHB.send_email'))
    
    return render_template('4_CONTACT/contact.html', form=form)



@AHB.route('/send-email', methods=['POST'])
def send_email():
    # Get customer details from the form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    message = request.form.get('message')

    customer_name = f"{first_name} {last_name}"


    # Create email message
    msg = Message(
        subject=f"I need to add a subject",  # Include customer's name in the subject
        recipients=["ahb_carpentry@gmail.com"],
        sender=email,
        body=f"Message from {customer_name}:\n\n{message}"  # Include customer's name in the body
    )

    # Send email
    mail.send(msg)

    return redirect(url_for('AHB.success', message="Your email has been sent"))


@AHB.route('/success')
def success():
    message = request.args.get('message', '')  
    session.pop('_flashes', None) 
    return render_template('CODES/success.html', message=message)


@AHB.route('/404')
def failure():
    message = request.args.get('message', '404 Error!')  
    session.pop('_flashes', None) 
    return render_template('CODES/404.html', message=message)





@AHB.route('/delete-image', methods=['POST'])
def delete_image():
    data = request.json
    image_name = data.get('image_name')
    residency_name = data.get('residency_name')

    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    residency_path = os.path.join(app_dir, 'static', 'images', 'portfolio', residency_name)
    image_path = os.path.join(residency_path, image_name)

    # Check if the file exists and remove it
    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        return jsonify({'status': 'error', 'message': 'Image not found on server'}), 404

    # Load the current portfolio data
    with open('json/portfolio.json') as f:
        data = json.load(f)
    
    portfolio = data.get('portfolio', {})

    if residency_name in portfolio:
        photos = portfolio[residency_name]['photos']

        if image_name in photos:
            photos.remove(image_name)

 

            # If there are no photos left, remove the residency
            if not photos:
                del portfolio[residency_name]
                os.rmdir(residency_path)
                
            
            # Save the updated JSON data back to the file
            with open('json/portfolio.json', 'w') as f:
                json.dump(data, f, indent=4)
                
                
            
            if not photos:
                return jsonify({'status': 'success', 
                                'message': 'remove_project_container', 
                                'refresh' : True})
            else:
                return jsonify({'status': 'success', 
                                'message': 'remove_photo_container',
                                'refresh' : True})
        else:
            return jsonify({'status': 'error', 'message': 'Image not found in JSON'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'Residency not found in JSON'}), 404



def remove_photo_from_json(residence_name, index):
    # Read the existing JSON data
    with open('json/portfolio.json', 'r') as file:
        data = json.load(file)

    # Find the residence by name
    for residence in data['portfolio']:
        if residence['residence_name'] == residence_name:
            # Check if index is within range
            if 0 <= index < len(residence['photos']):
                # Remove the photo at the specified index
                residence['photos'].pop(index)
                # Write the updated data back to the JSON file
                with open('json/portfolio.json', 'w') as file:
                    json.dump(data, file, indent=4)
                return True
            else:
                return False  # Index out of range
    return False  # Residence name not found