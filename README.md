# DIY ChatGPT-like app 🚀
###  **Install necessary libraries**
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

### Running Locally ? 📍
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