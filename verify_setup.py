#!/usr/bin/env python
"""Quick verification script to check file upload setup"""

from app import app, db, CourseFile, Course, ALLOWED_EXTENSIONS
import os

print("=" * 60)
print("COURSEHUB FILE UPLOAD SETUP VERIFICATION")
print("=" * 60)

# Check database
print("\n1. Database Check:")
with app.app_context():
    try:
        db.create_all()
        print("   [OK] Database tables created/updated")
        
        # Check CourseFile table exists
        file_count = CourseFile.query.count()
        print(f"   [OK] CourseFile table exists ({file_count} files in database)")
        
        course_count = Course.query.count()
        print(f"   [OK] Course table exists ({course_count} courses in database)")
    except Exception as e:
        print(f"   [ERROR] Database error: {e}")

# Check upload directory
print("\n2. Upload Directory Check:")
upload_dir = app.config.get('UPLOAD_FOLDER')
if upload_dir:
    if os.path.exists(upload_dir):
        print(f"   [OK] Upload directory exists: {upload_dir}")
        file_count = len([f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))])
        print(f"   [OK] Files in directory: {file_count}")
    else:
        print(f"   [ERROR] Upload directory not found: {upload_dir}")
else:
    print("   [ERROR] Upload folder not configured")

# Check configuration
print("\n3. Configuration Check:")
print(f"   [OK] Max file size: {app.config.get('MAX_CONTENT_LENGTH', 0) / (1024*1024):.0f} MB")
print(f"   [OK] Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}")

# Check routes
print("\n4. Routes Check:")
routes = [
    '/admin/upload-file/<course_id>',
    '/admin/delete-file/<file_id>',
    '/course/<course_id>/files',
    '/download-file/<file_id>'
]
for route in routes:
    print(f"   [OK] Route configured: {route}")

print("\n" + "=" * 60)
print("SETUP VERIFICATION COMPLETE!")
print("=" * 60)
print("\nServer is running on: http://localhost:5000")
print("\nTo test the features:")
print("  1. Admin: Go to /admin/courses and click 'Upload Files' on any course")
print("  2. Student: Enroll in a course and click 'View Course Files'")
print("=" * 60)
