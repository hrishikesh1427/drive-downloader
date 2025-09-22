Below is a **clear, beginner-friendly README.md** you can place in the project root.
It explains the Google Cloud setup, environment creation, installation, and running steps so anyone can follow.

---

```markdown
# Google Drive File/Folder Downloader (Python)

A Python utility to **download entire Google Drive folders or individual files**  
using the Google Drive API.

This tool supports:
- ✅ File or folder share links
- ✅ Raw file/folder IDs
- ✅ Automatic handling of duplicate file names
- ✅ Download progress bar with `tqdm`

---

## ⚡ 1. Prerequisites

| Requirement | Version (recommended) |
|-------------|------------------------|
| Python      | 3.8 or higher |
| Google account | Any Gmail / Workspace account |
| Internet connection | Needed for Google OAuth |

---

## 📂 2. Google Cloud Setup

Follow these steps **once** to enable Google Drive API and obtain credentials.

1. **Create a Google Cloud project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Click **Select a project** → **New Project** → give it a name → **Create**.

2. **Enable Google Drive API**
   - Inside the project, go to  
     **APIs & Services → Library**.
   - Search for **Google Drive API** → **Enable**.

3. **Configure OAuth consent screen**
   - Navigate to **APIs & Services → OAuth consent screen**.
   - Choose **External** → **Create**.
   - Fill in:
     - **App name** (anything you like)
     - **User support email**
     - **Developer contact info**
   - Scopes: click **Add or Remove Scopes**, search and add  
     `.../auth/drive.readonly`.
   - Save and continue until you can **Publish** or keep in **Testing** mode.
     > ⚠️ If you keep it in Testing, add your Google account under **Test Users**.

4. **Create OAuth Client ID**
   - Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
   - Application type: **Desktop App**.
   - Name: e.g. `Drive Downloader`.
   - Click **Create** → **Download JSON**.
   - Rename the file to `credentials.json` and place it in the project root.

Your project folder should now contain:
```

files\_download.py
credentials.json

````

---

## 🐍 3. Local Environment Setup

It’s best to use a virtual environment.

```bash
# Create and activate a virtual environment (Windows PowerShell)
python -m venv myenv
.\myenv\Scripts\activate

# Install required packages
pip install --upgrade pip
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib tqdm
````

---

## ▶️ 4. Running the Downloader

1. Make sure you have:

   * `files_download.py`
   * `credentials.json`
   * Your virtual environment activated.

2. Run:

```bash
python files_download.py
```

3. The first time you run it:

   * A browser window opens asking you to log in and grant access.
   * After approval, a `token.pickle` file is saved so you won’t need to log in again.

4. When prompted:

   ```
   Enter Google Drive file/folder link or ID:
   ```

   * You can paste **any** of these:

     * Full file link (e.g. `https://drive.google.com/file/d/<ID>/view?usp=sharing`)
     * Full folder link (e.g. `https://drive.google.com/drive/folders/<ID>`)
     * Raw ID (`<ID>`)

5. The content is downloaded to the `downloads` folder
   (created automatically in the project directory).

---

## 💡 Tips

* If you get `access_denied` during OAuth:

  * Make sure your Gmail is added as a **Test User** or the app is **Published**.
* If you need to start fresh, delete `token.pickle` and run again.
* To change the download directory, edit:

  ```python
  downloader = GoogleDriveDownloader(download_dir='my_downloads')
  ```

---

## 📜 License

This project is provided **as is**, for personal use.

```

---

### How to Use
1. Save the above text into a file named **`README.md`** in your project folder.  
2. Commit/push if using Git, or just keep it locally.  
3. Anyone can open the file in GitHub or a text editor and follow the steps.
```
