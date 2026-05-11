uvicorn src.main:app --reload
cd docs && hugo server
python -m pytest tests/