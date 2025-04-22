bash build.sh
echo "Testing"
python -m pip install -r test/requirements.txt
python test/test.py