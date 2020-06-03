# List of all changes

## What's new in service-bdms 1.0.1-RC1

### New features

 - **Attachments**: 
   
   You can now upload files attachments for each borehole on a AWS S3 Bucket.

 - **New configuration options**:
   
   To configure the file repository some options have been added to configure
   the AWS S3 Bucket (file_repo, aws_bucket, aws_credentials)

 - **New REST API**:

   */api/v1/borehole*

   - ACTION=LISTFILES list all files with less metadata linked to a given borehole

   */api/v1/borehole/edit*

   - ACTION=LISTFILES list all files metadata linked to a given borehole 
   
   */api/v1/borehole/edit/files*

   - ACTION=ATTACHFILE (multipart/form-data) and attach files to existing boreholes
   - ACTION=DETACHFILE unlink an uploaded file from a borehole
   - ACTION=PATCH update metadata of a file


 - **Database changes**:
   
   To handle the new attachments feature, two new tables were added to the
   schema bdms: **files** and **borehole_files**


### Backwards incompatible changes

 - **REST API Changes**:
   
   CSV importer API path has been changed from '/api/v1/borehole/upload' to
   '/api/v1/borehole/edit/import' and the POST-ed action param changed from
   'UPLOAD' to 'IMPORTCSV'