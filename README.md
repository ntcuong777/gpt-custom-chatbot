# DIY ChatGPT-like app 🚀
## Table of Contents
1. [Install necessary libraries](#installlibs)
2. [Running Locally? 📍](#runlocal)
    1. [Setting OpenAI API key](#setting-openai-api-key)
        1. [Windows setup](#windows-setup)
        2. [Linux / MacOS setup](#linux--macos-setup)
    2. [Running back-end and front-end](#running-back-end-and-front-end)

##  **Install necessary libraries** <a name="installlibs"></a>
First, create the `conda` environment:
```
conda create -n chatgpt python=3.10
```

Then, activate the environment:
```
conda activate chatgpt
```

Finally, install the requirements:
```
cd /path/to/app/dir
pip install -r requirements.txt
```

## Running Locally? 📍 <a name="runlocal"></a>
### Setting OpenAI API key
First, you need to set your OpenAI API key into your environment variable:

#### Windows setup
On **Windows**, you can set your `OPENAI_API_KEY` Environment Variable via the cmd prompt. Run the following in the cmd prompt, replacing <yourkey> with your API key:
```
setx OPENAI_API_KEY "<yourkey>"
```

This will apply to future cmd prompt window, so you will need to open a new one to use that variable with curl. You can validate that this variable has been set by opening a new cmd prompt window and typing in 
```
echo %OPENAI_API_KEY%
```

#### Linux / MacOS setup
On **Linux / MacOS**, set your `OPENAI_API_KEY` Environment Variable using *zsh* or *bash*
1. Run the following command in your terminal, replacing yourkey with your API key.
    ```
    echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
    ```
    If you are using *bash*, just replace **.zshrc** with **.bashrc**
2. Update the shell with the new variable:
    ```
    source ~/.zshrc
    ```
    or
    ```
    source ~/.bashrc
    ```
    if you are using *bash*.
3. Confirm that you have set your environment variable using the following command.
    ```
    echo $OPENAI_API_KEY
    ```

### Running back-end and front-end
Backend Run Command (development):
```
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

Or, for production mode:
```
uvicorn backend:app --host 0.0.0.0 --port 8000
```

Front-end Run Command (development):
```
streamlit run frontend.py
```

The app front-end can be accessed at `localhost:8501`