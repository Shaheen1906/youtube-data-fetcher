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
git clone https://github.com/<your-repo-name>/youtube-data-fetcher.git
cd youtube-data-fetcher
```

#### **Step 2: Install Dependencies**
Use `pip` to install the required libraries:  
```bash
pip install -r requirements.txt
```

#### **Step 3: Enable the YouTube Data API**
1. Visit the [Google Cloud Console](https://console.cloud.google.com/).  
2. Create a new project or select an existing project.  
3. Enable the **YouTube Data API v3** for your project.  
4. Create credentials:
   - Go to **Credentials** > **Create Credentials** > **API Key**.
   - Copy the API key for use in the script.

#### **Step 4: Configure the Script**
Open the `config.py` file (if provided) or locate the `API_KEY` placeholder in the script and replace it with your API key:
```python
API_KEY = "YOUR_API_KEY_HERE"
```

---

### **Usage Instructions**

#### **Run the Script**
1. Open a terminal in the project directory.
2. Run the script and provide the channel URL:
```bash
python youtube_fetcher.py
```

#### **Input Example**
When prompted, enter a valid YouTube channel URL with a handle (e.g., `https://www.youtube.com/@channelhandle`).

#### **Output**
- The script generates an Excel file named `YouTube_Channel_Data.xlsx` in the working directory.
- **Sheet 1: Video Data**:
  - Contains video details such as Video ID, Title, Description, Published Date, View Count, Like Count, Comment Count, Duration, and Thumbnail URL.
- **Sheet 2: Comments Data**:
  - Contains comments and replies for the latest videos, including Video ID, Comment ID, Text, Author Name, Published Date, Like Count, and "Reply to" information.

---

### **Dependencies**
The script uses the following Python libraries:
1. **`google-api-python-client`**: For interacting with the YouTube Data API.  
2. **`pandas`**: For data manipulation and exporting to Excel.  
3. **`openpyxl`**: For working with Excel files.  
4. **`logging`**: For debugging and error handling.  

Install all dependencies using:  
```bash
pip install -r requirements.txt
```

---

### **Error Handling**
- If an invalid URL is provided, the script will terminate gracefully with an error message.  
- Ensure that the YouTube channel URL includes a valid handle (starts with `@`).  
- API quota exceeded:
  - You might hit YouTube's daily API quota limits. Consider optimizing API usage or requesting a higher quota.  

---

### **Future Enhancements**
- Support for paginated comment fetching to handle more than 100 comments.  
- Better handling of different channel URL formats (e.g., `channel ID`, `username`).  
- Caching and retry logic for API requests.  

---

### **Troubleshooting**
If you encounter issues, ensure:
1. **Correct Python version**: Run `python --version` to verify.  
2. **API key permissions**: Verify your API key is active and has access to the YouTube Data API.  
3. **Dependencies installed**: Reinstall using `pip install -r requirements.txt`.  

For further assistance, open an issue in the repository or contact the maintainer.

---

### **License**
This project is licensed under the MIT License.  

---

Let me know if you need any additions or further customization!