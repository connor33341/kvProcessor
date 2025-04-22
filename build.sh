echo "Building"
#rm dist
python -m pip install build twine
#cd kvprocessor
python -m build
python -m pip install dist/kvprocessor-0.1.5-py3-none-any.whl