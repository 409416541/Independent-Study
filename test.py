import numpy as np

text = ['Please choose action', 
        '1. Sit Ups', '2. Push Up', '3. Squat', '4. Leg Raises', '5. Jumping Jacks', '6. Break', # interface
        'Your choose is ', 
        'Rock. OK', 'Pink. NO',
        'Please choose you want', 
        '1. Sample Video', '2. Go Sport', '3. back to interface',
        'How times you want']

print(text[1].split('. ')[1])