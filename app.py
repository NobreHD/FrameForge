import os, json, cv2
from PIL import Image
from time import sleep
from shutil import copyfile

def extractVideo(inVideo, outFolder):
  if not os.path.exists(outFolder):
    os.makedirs(outFolder)
  
  video = cv2.VideoCapture(inVideo)
  fps = video.get(cv2.CAP_PROP_FPS)
  success, image = video.read()
  count = 0
  while success:
    cv2.imwrite(os.path.join(outFolder, f'frame-{count:06}.png'), image)
    success, image = video.read()
    count += 1
  
  return [1/fps] * count
  

def extractGIF(inGIF, outFolder):
  if not os.path.exists(outFolder):
    os.makedirs(outFolder)
  
  frame = Image.open(inGIF)
  count = 0
  duration = []
  while frame:
    duration.append(frame.info['duration'])
    frame.save(os.path.join(outFolder, f'frame-{count:06}.png'))
    count += 1
    try:
      frame.seek(count)
    except EOFError:
      break
  return duration
    
def evaluateImages(inFolder, inTemp, inDuration, outJSON):
  unique_images = []
  current_streak = []
  current_duration = 0
  count = 0
  
  for filename in os.listdir(inFolder):
    if not filename.endswith('.png'):
      continue
    
    if len(current_streak) == 0:
      current_duration = inDuration[0]
      current_streak.append(filename)
      continue
    
    # Compare the current image with the previous image
    current_image = Image.open(inFolder + filename)
    previous_image = Image.open(inFolder + current_streak[-1])
    
    # Make a repeating gif of the two images and show it to the user
    current_image.save(inTemp, save_all=True, append_images=[previous_image], loop=0)
    
    # Ask the user if the images are the same
    is_same = input('Are the images the same? (y/n): ')
    if is_same == 'y':
      current_streak.append(filename)
      current_duration += inDuration[count]
    else:
      unique_images.append((current_duration, current_streak))
      current_streak = [filename]
      current_duration = inDuration[count]
    
    count += 1
      
  with open(outJSON, 'w') as file:
    json.dump(unique_images, file, indent=4)

def copyUniqueImages(inFolder, inJSON, outFolder):
  if not os.path.exists(outFolder):
    os.makedirs(outFolder)
  
  with open(inJSON, 'r') as file:
    unique_images = json.load(file)
    
  for index, image_group in enumerate(unique_images):
    copyfile(inFolder + image_group[1][0], outFolder + str(index).zfill(6) + ".png")
  
def remakeGIF(inFolder, inJSON, outGIF):
  with open(inJSON, 'r') as file:
    unique_images = json.load(file)
    
  gif_frames = []
  
  for image_group in unique_images:
    duration = image_group[0]
    frame_path = image_group[1][0]
    
    frame = Image.open(inFolder + frame_path)
    gif_frames.append(frame.copy())
    gif_frames[-1].info['duration'] = duration*1000
    
  gif_frames[0].save(outGIF, save_all=True, append_images=gif_frames[1:], loop=0)
  
def clearFolder(inFolder):
  if not os.path.exists(inFolder):
    return
  for filename in os.listdir(inFolder):
    os.remove(inFolder + filename)
  
  
if __name__ == '__main__':
  extract_folder = 'extract/'
  unique_folder = 'unique/'
  json_file = 'images.json'
  temp_file = 'temp.gif'
  out_gif = 'out.gif'
  
  if not os.path.exists(unique_folder):
    os.makedirs(unique_folder)
  
  if os.listdir(unique_folder):
    print('The unique directory is not empty.')
    reply = input('Do you want to reconstruct the GIF? (y/n): ').upper()
    if reply == 'Y':
      remakeGIF(extract_folder, json_file, out_gif)
      print(f'Reconstructed GIF saved to: "{os.path.abspath(out_gif)}"')
    
    reply = input('Do you want to clear the unique directory? (y/n): ').upper()
    if reply == 'Y':
      clearFolder(unique_folder)
      print('Cleared directory: ' + unique_folder)
    
    exit()
  
  choice = 0
  
  while True:
    os.system('cls' if os.name == 'nt' else 'clear')  
    print('1. Extract frames from video')
    print('2. Extract frames from GIF')
    print('3. Exit')
    choice = int(input('Enter choice: '))
    if choice in [1, 2, 3]:
      break
    print('Invalid choice. Please try again.')
    sleep(1.5)
    
  if choice == 3:
    exit()
    
  print()
  clearFolder(extract_folder)
  duration = []
  
  if choice == 1:
    duration = extractVideo(input('Enter video path: '), extract_folder)
  elif choice == 2:
    duration = extractGIF(input('Enter GIF path: '), extract_folder)
  
  while len(duration) != len(os.listdir(extract_folder)):
    print('Extracting frames...')
    sleep(1)
  
  print('Extracted frames saved to: ' + extract_folder)
  evaluateImages(extract_folder, temp_file, duration, json_file)
  copyUniqueImages(extract_folder, json_file, unique_folder)
  print('Unique frames saved to: ' + unique_folder)
  print('Please rerun the program to reconstruct the GIF.')
