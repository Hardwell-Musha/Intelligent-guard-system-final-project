import cloudinary
from cloudinary.uploader import upload

# Configure Cloudinary
cloudinary.config( 
    cloud_name = "diykglllj", 
    api_key = "239345618852227", 
    api_secret = "JE2QGH1j-g9aqwL5unkSXVEiTDg" 
)

# Provide the file path for the video
video_path = "C:\\Users\\ARX56\\OneDrive\\Desktop\\InteligentGuardReact\\client\\public\\processed_videos\\processed_video.mp4"

# Upload video to Cloudinary with the resource_type set to "video"
response = upload(video_path, resource_type="video")

# Print the Cloudinary response
print(response)
