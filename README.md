# discography-dl

This project downloads an entire album of songs from YouTube using yt-dlp, while obtaining track metadata from the MusicBrainz API. No API keys are required.

## Prerequisites

- **Python 3.10+**
- **FFmpeg** must be installed and available in your system's PATH.
- A working internet connection.

## Setup Instructions

1. **Clone the Repository**

   Open a terminal and run:

   ```bash
   git clone https://github.com/stano45/discography-dl.git
   cd discography-dl
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   Create the environment:

   ```bash
   python3 -m venv .venv
   ```

   Activate it:

   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux/MacOS:**
     ```bash
     source .venv/bin/activate
     ```

3. **Install Dependencies**

   Install the required packages with:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

To start the album downloader, run:

```bash
python main.py
```

Follow the on-screen instructions to:

- Choose a path for downloads.
- Choose whether to run in interactive mode.
- Enter the artist name.
- Select the artist from the list of search results.
- Choose an album to download.
- Choose the correct version (release) of the album.
- Confirm track selections before downloading (if using interactive mode).

## Additional Information

- The tool uses MusicBrainz to gather metadata like album title and track list.
- yt-dlp downloads the audio in the best available quality and converts it to MP3 (192 kbps).
- No API keys are needed for accessing the MusicBrainz API.

## Contributing

Contributions, improvements, and bug fixes are welcome. Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
