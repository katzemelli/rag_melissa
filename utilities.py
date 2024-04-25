import re, os, requests, configparser
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
import magic

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = cd.split('filename=')[1]
    if fname.lower().startswith(("utf-8''", "utf-8'")):
        fname = fname.split("'")[-1]
    return unquote(fname)
  
def download_file(url):
    try:
        # Start the request and handle possible request-related errors
        with requests.get(url, stream=True) as r:
            r.raise_for_status()  # Raises an HTTPError for bad responses

            # Get filename from content disposition or construct from URL
            filename = get_filename_from_cd(r.headers.get('content-disposition'))
            if not filename:
                filename = urlparse(url).path.split('/')[-1]  # Extracting file name from path
                if not filename:
                    filename = urlparse(url).netloc.replace('.', '-') + '.bin'  # Fallback filename

            # Save the file in a specified directory
            filename = 'content/' + filename
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive chunks
                        f.write(chunk)
            return filename

    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (like 404, 500, etc.)
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        # Handle errors like DNS failure, refused connection
        print("Error connecting to the server")
    except requests.exceptions.Timeout:
        # Handle requests timeout
        print("Timeout occurred")
    except requests.exceptions.RequestException as e:
        # Handle any other requests-related errors
        print(f"Error downloading file: {e}")
    except Exception as e:
        # General exception handler for unexpected errors
        print(f"An error occurred: {e}")

    return None  # Return None if there was an error
  

      
def readtext(path):
  path = path.rstrip()
  path = path.replace(' \n', '')
  path = path.replace('%0A', '')
  # check if path is a comment or empty (comment is a line starting with #)
  if path.startswith('#') or path == "":
    return ""
  if re.match(r'^https?://', path):
    filename = download_file(path)
  else:
    relative_path = path
    filename = os.path.abspath(relative_path)
  
  if not filename:
    return ""
  
  filetype = magic.from_file(filename, mime=True)
  print(f"\nEmbedding {filename} as {filetype}")
  text = ""
  if filetype == 'application/pdf':
    print('PDF not supported yet')
  if filetype == 'text/plain':
    with open(filename, 'rb') as f:
      text = f.read().decode('utf-8')
  if filetype == 'text/html':
    with open(filename, 'rb') as f:
      soup = BeautifulSoup(f, 'html.parser')
      text = soup.get_text()
  
  if os.path.exists(filename) and filename.find('content/') > -1:
    os.remove(filename) 
    
  return text

def getconfig():
  config = configparser.ConfigParser()
  config.read('config.ini')
  return dict(config.items("main"))