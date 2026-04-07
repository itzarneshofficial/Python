from PIL import Image, ImageDraw

# Create a blank image with white background
width, height = 800, 800
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Draw Doraemon's face
face_center = (400, 400)
face_radius = 300
draw.ellipse((face_center[0] - face_radius, face_center[1] - face_radius, 
              face_center[0] + face_radius, face_center[1] + face_radius), 
             fill="blue", outline="black", width=5)

# Draw Doraemon's face white inner circle
inner_face_radius = 250
draw.ellipse((face_center[0] - inner_face_radius, face_center[1] - inner_face_radius, 
              face_center[0] + inner_face_radius, face_center[1] + inner_face_radius), 
             fill="white", outline="black", width=5)

# Draw Doraemon's eyes
eye_radius = 50
left_eye_center = (face_center[0] - 70, face_center[1] - 100)
right_eye_center = (face_center[0] + 70, face_center[1] - 100)
draw.ellipse((left_eye_center[0] - eye_radius, left_eye_center[1] - eye_radius, 
              left_eye_center[0] + eye_radius, left_eye_center[1] + eye_radius), 
             fill="white", outline="black", width=5)
draw.ellipse((right_eye_center[0] - eye_radius, right_eye_center[1] - eye_radius, 
              right_eye_center[0] + eye_radius, right_eye_center[1] + eye_radius), 
             fill="white", outline="black", width=5)

# Draw Doraemon'sEye Balls
pupil_radius = 20
draw.ellipse((left_eye_center[0] - pupil_radius, left_eye_center[1] - pupil_radius, 
              left_eye_center[0] + pupil_radius, left_eye_center[1] + pupil_radius), 
             fill="black")
draw.ellipse((right_eye_center[0] - pupil_radius, right_eye_center[1] - pupil_radius, 
              right_eye_center[0] + pupil_radius, right_eye_center[1] + pupil_radius), 
             fill="black")

# Draw Doraemon's nose
nose_center = (face_center[0], face_center[1] - 50)
nose_radius = 30
draw.ellipse((nose_center[0] - nose_radius, nose_center[1] - nose_radius, 
              nose_center[0] + nose_radius, nose_center[1] + nose_radius), 
             fill="red", outline="black", width=5)

# Draw Doraemon's mouth
mouth_start = (face_center[0] - 100, face_center[1] + 50)
mouth_end = (face_center[0] + 100, face_center[1] + 50)
draw.line((mouth_start, mouth_end), fill="black", width=5)

# Save the image
image.save("doraemon.png")

print("Doraemon image created and saved as doraemon.png")
