from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load the video
video = VideoFileClip("your_video.mp4")

# Create glowing text
glow_text = TextClip(
    "Powered By TrendRiders",
    fontsize=50,
    color="gold",
    font="Arial",
    stroke_color="yellow",
    stroke_width=5,
).set_position("center").set_duration(video.duration)

# Composite the video
composite_video = CompositeVideoClip([video, glow_text])

# Export the video
composite_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")
