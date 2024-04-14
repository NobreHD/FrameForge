## Frame Forge: Frame-by-Frame GIF Editing

**Frame Forge** is a user-friendly tool that empowers you to edit animated GIFs on a frame-by-frame basis. 

**Key Features:**

* **Extract Frames:** Easily extract all frames from an animated GIF/video and save them as individual PNG images.
* **Visually Compare Frames:** Quickly compare adjacent frames to identify duplicates or subtle changes.
* **Identify Unique Frames:**  With user guidance, Frame Forge helps you distinguish unique frames from repetitive sequences.
* **Selective Removal:** Remove unwanted or redundant frames to optimize your GIF.
* **Optional Reconstruction:** Rebuild a new GIF using only the unique frames, creating a leaner animation.

**Getting Started**

1. **Installation:**
   - Frame Forge requires Python 3 and the following libraries: Pillow,  os, and shutil. You can install them using `pip install Pillow`.

2. **Usage:**
   - Clone the repository: `git clone https://github.com/NobreHD/FrameForge.git`
   - Navigate to the project directory: `cd FrameForge`
   - Run the script: `python app.py`

3. **Follow the Prompts:**
   - The program will guide you through the process of selecting a GIF, extracting frames, and identifying unique sequences.

**Example Workflow:**

1. Open Frame Forge and select your target GIF.
2. The program will extract all frames and display them in a folder.
3. Frame Forge will create temporary GIFs comparing adjacent frames to aid your decision-making.
4. Indicate whether frames are duplicates or unique. 
5. Frame Forge will compile a list of unique frames based on your input.
6. You can choose to copy the unique image files and optionally reconstruct a new, optimized GIF.

**Further Considerations:**

* Refer to the `Frame_Forge.py` script for detailed function definitions. 
* Frame identification requires user input. Review the comparisons carefully for optimal results.

**Contributing:**

We welcome contributions to improve Frame Forge! Feel free to submit pull requests with bug fixes, enhancements, or new features.
