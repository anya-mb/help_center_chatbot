# Help center chatbot

## Setup

Create virtual environment:

```
python -m venv venv
```

Activate the virtual environment:
* On Windows:
```
venv\Scripts\activate
```
* On macOS and Linux:

```
source venv/bin/activate
```

Add `OPENAI_API_KEY=` to `.env` file. See example in `.env_example` file.


## Run

To run streamlit frontend chatbot:
```
streamlit run app.py
```