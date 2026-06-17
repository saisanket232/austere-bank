#!/bin/bash
echo "Building Django project on Vercel..."
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
echo "Build complete!"
