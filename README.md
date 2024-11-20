### **YouTube Channel Video and Comments Data Fetcher**  
This Python script fetches data from a YouTube channel URL (with a handle) and generates an Excel file containing:  
1. **Video Data** (e.g., title, views, likes, etc.) in Sheet 1.  
2. **Comments Data** (e.g., comments, replies, author details, etc.) in Sheet 2.

---

### **Prerequisites**  
Ensure you have the following installed before running the script:  
1. **Python 3.7+**  
2. **Google YouTube Data API v3** enabled in your Google Cloud Console.  

---

### **Setup Instructions**

#### **Step 1: Clone or Download the Repository**
```bash
git clone https://github.com/Shaheen1906/youtube-data-fetcher.git
cd youtube-data-fetcher
```
#### **Step 2: Create Virtual Enviornment **
1. Use `venv` to create virutal environment:  
```bash
python -m venv venv_name(venv)
```
2. Activate:
```bash
.\venv\Scripts\activate
```

#### **Step 3: Install Dependencies**
### **Dependencies**
The script uses the following Python libraries:
1. **`google-api-python-client`**: For interacting with the YouTube Data API.  
2. **`pandas`**: For data manipulation and exporting to Excel.  
3. **`openpyxl`**: For working with Excel files.  
4. **`logging`**: For debugging and error handling. 
5. **`isodate`**: Convert ISO 8601 duration to HH:MM:SS format.

Use `pip` to install the required libraries:  
```bash
pip install -r requirements.txt
```

#### **Step 4: Enable the YouTube Data API**
1. Visit the [Google Cloud Console](https://console.cloud.google.com/).  
2. Create a new project or select an existing project.  
3. Enable the **YouTube Data API v3** for your project.  
4. Create credentials:
   - Go to **Credentials** > **Create Credentials** > **API Key**.
   - Copy the API key for use in the script.

#### **Step 5: Configure the Script**
Open the `config.py` file (if provided) or locate the `API_KEY` placeholder in the script and replace it with your API key:
```python
API_KEY = "YOUR_API_KEY_HERE"
```

### **Usage Instructions**

#### **Run the Script**
1. Open a terminal in the project directory.
2. Run the script and provide the channel URL:
```bash
python youtube_fetcher.py
```

#### **Input Example**
When prompted, enter a valid YouTube channel URL with a handle (e.g., `https://www.youtube.com/@ConcreteThinking`).

#### **Output**
- The script generates an Excel file named `youtube_data.xlsx` in the working directory.
- **Sheet 1: Video Data**:
  - Contains video details such as Video ID, Title, Description, Published Date, View Count, Like Count, Comment Count, Duration, and Thumbnail URL.
- **Sheet 2: Comments Data**:
  - Contains comments and replies for the latest videos, including Video ID, Comment ID, Text, Author Name, Published Date, Like Count, and "Reply to" information.

---
 
### **Error Handling**
- If an invalid URL is provided, the script will terminate gracefully with an error message.  
- Ensure that the YouTube channel URL includes a valid handle (starts with `@`).  
- API quota exceeded:
  - You might hit YouTube's daily API quota limits. Consider optimizing API usage or requesting a higher quota.  


### ** Output Files**
For reference, I have included the output files `youtube_data.xlsx` and `youtube_data1.xlsx`