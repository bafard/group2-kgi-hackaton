from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import List
from pydantic import BaseModel
import hashlib
import os
from pathlib import Path
import shutil
import io
from datetime import datetime
from ..utils.metadata import add_upload_metadata, remove_upload_metadata, get_all_uploads_metadata, update_objects_metadata

# Try to import optional dependencies for SQL Server functionality
try:
    import pandas as pd
    from ..utils.sql_server_connection import sql_server
    from ..utils.inspection_data_mapper import map_excel_to_database_columns, get_all_inspection_data_columns, filter_excel_columns_for_database
    from ..utils.machine_tracking_mapper import map_excel_to_machine_tracking_columns, get_all_machine_tracking_columns, filter_excel_columns_for_machine_tracking
    from ..utils.uc_lifetime_mapper import map_excel_to_uc_lifetime_columns, get_all_uc_lifetime_columns, filter_excel_columns_for_uc_lifetime
    SQL_SERVER_AVAILABLE = True
    print(f"✅ SQL Server dependencies loaded successfully - SQL_SERVER_AVAILABLE: {SQL_SERVER_AVAILABLE}")
except ImportError as e:
    SQL_SERVER_AVAILABLE = False
    print(f"❌ SQL Server dependencies failed to load - SQL_SERVER_AVAILABLE: {SQL_SERVER_AVAILABLE}, Error: {e}")

router = APIRouter()

def get_target_table(system_type: str) -> str:
    """Get target database table based on system type"""
    if system_type == "KOMTRAX":
        return "Machine_Tracking"
    elif system_type == "Expected Lifetime":
        return "UC_Life_Time"
    else:  # UMS
        return "InspectionData"

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class DeleteFilesRequest(BaseModel):
    filenames: List[str]

class UpdateObjectsRequest(BaseModel):
    stored_filename: str
    objects: List[dict]

def calculate_md5(content: bytes) -> str:
    """Calculate MD5 hash of file content."""
    return hashlib.md5(content).hexdigest()

def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return Path(filename).suffix.lower()

async def save_file(file: UploadFile, content: bytes) -> dict:
    """
    Save file with MD5 hash as filename and return file info.
    
    Args:
        file: The uploaded file object
        content: File content bytes
    
    Returns:
        dict: File information including saved path and hash
    """
    # Calculate MD5 hash
    file_hash = calculate_md5(content)
    
    # Get file extension
    file_extension = get_file_extension(file.filename)
    
    # Create filename with MD5 hash + extension
    hashed_filename = f"{file_hash}{file_extension}"
    file_path = UPLOAD_DIR / hashed_filename
    
    # Check if file already exists (deduplication)
    file_exists = file_path.exists()
    
    # Save file (will overwrite if exists)
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Add metadata for the uploaded file
    add_upload_metadata(
        original_filename=file.filename,
        stored_filename=hashed_filename,
        file_size=len(content)
    )
    
    return {
        "original_filename": file.filename,
        "saved_filename": hashed_filename,
        "file_path": str(file_path),
        "file_hash": file_hash,
        "size": len(content),
        "content_type": file.content_type,
        "was_duplicate": file_exists
    }

@router.post("/upload")
async def upload_file(files: List[UploadFile] = File(...)):
    """
    File upload endpoint that accepts single or multiple files, saves them with MD5 hash filenames,
    and returns file information. Supports both single file and files[] format from multipart/form-data.
    
    Files are saved in the 'uploads' directory with MD5 hash as filename to prevent duplicates.
    If a file with the same content already exists, it will be overwritten.
    
    Args:
        files: The uploaded file(s) (multipart/form-data)
    
    Returns:
        dict: A dictionary containing file information including saved paths and hashes
    
    Raises:
        HTTPException: If no files are provided or there's an error processing them
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    uploaded_files = []
    total_size = 0
    duplicates_count = 0

    try:
        for file in files:
            if not file.filename:
                continue  # Skip files without filenames
            
            # Read the file content
            content = await file.read()
            file_size = len(content)
            total_size += file_size
            
            # Save file with MD5 hash filename
            file_info = await save_file(file, content)
            uploaded_files.append(file_info)
            
            if file_info["was_duplicate"]:
                duplicates_count += 1
            
            # Reset file pointer if needed for further processing
            await file.seek(0)
        
        if not uploaded_files:
            raise HTTPException(status_code=400, detail="No valid files were uploaded")
        
        return {
            "files": uploaded_files,
            "total_files": len(uploaded_files),
            "total_size": total_size,
            "duplicates_count": duplicates_count,
            "upload_directory": str(UPLOAD_DIR),
            "message": f"Successfully uploaded {len(uploaded_files)} file{'s' if len(uploaded_files) > 1 else ''}" +
                      (f" ({duplicates_count} duplicate{'s' if duplicates_count > 1 else ''} overwritten)" if duplicates_count > 0 else "")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

@router.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """
    Multiple file upload endpoint that accepts multiple files and saves them with MD5 hash filenames.
    
    This endpoint provides the same functionality as /upload but with a different route name.
    Files are saved with MD5 hash to prevent duplicates and enable deduplication.
    
    Args:
        files: List of uploaded files (multipart/form-data)
    
    Returns:
        dict: A dictionary containing information about all uploaded files
    
    Raises:
        HTTPException: If no files are provided or there's an error processing them
    """
    # Reuse the main upload function logic
    return await upload_file(files)

@router.get("/uploads")
async def list_uploaded_files():
    """
    List all uploaded files in the uploads directory.
    
    Returns:
        dict: List of uploaded files with their information
    """
    try:
        if not UPLOAD_DIR.exists():
            return {
                "files": [],
                "total_files": 0,
                "upload_directory": str(UPLOAD_DIR),
                "message": "No uploads directory found"
            }
        
        files = []
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "path": str(file_path),
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime
                })
        
        return {
            "files": files,
            "total_files": len(files),
            "upload_directory": str(UPLOAD_DIR),
            "message": f"Found {len(files)} uploaded file{'s' if len(files) != 1 else ''}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@router.get("/uploads/metadata")
async def get_uploads_metadata():
    """
    Get metadata for all uploaded files from the uploads-metadata.json file.
    
    Returns:
        dict: List of uploaded files with their metadata including original filename,
              stored filename, upload time, and file size
    """
    try:
        metadata_records = get_all_uploads_metadata()
        
        return {
            "uploads": metadata_records,
            "total_uploads": len(metadata_records),
            "message": f"Found metadata for {len(metadata_records)} uploaded file{'s' if len(metadata_records) != 1 else ''}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving metadata: {str(e)}")

@router.put("/uploads/metadata/objects")
async def update_upload_objects_metadata(request: UpdateObjectsRequest):
    """
    Update the objects detection information for a specific uploaded file.
    
    Args:
        request: Request body containing stored filename and objects list
        
    Returns:
        dict: Success or error message
    """
    try:
        success = update_objects_metadata(request.stored_filename, request.objects)
        
        if success:
            return {
                "success": True,
                "message": f"Successfully updated objects metadata for {request.stored_filename}"
            }
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"File not found in metadata: {request.stored_filename}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating objects metadata: {str(e)}")

@router.delete("/uploads")
async def delete_files(request: DeleteFilesRequest):
    """
    Delete multiple uploaded files from the uploads directory.
    
    Args:
        request: Request body containing list of filenames to delete
    
    Returns:
        dict: Result of deletion operation
    
    Raises:
        HTTPException: If files are not found or there's an error deleting them
    """
    try:
        if not UPLOAD_DIR.exists():
            raise HTTPException(status_code=404, detail="Uploads directory not found")
        
        deleted_files = []
        not_found_files = []
        errors = []
        
        for filename in request.filenames:
            file_path = UPLOAD_DIR / filename
            
            if not file_path.exists():
                not_found_files.append(filename)
                continue
            
            if not file_path.is_file():
                errors.append(f"{filename} is not a file")
                continue
            
            try:
                os.remove(file_path)
                deleted_files.append(filename)
                # Remove metadata for the deleted file
                remove_upload_metadata(filename)
            except Exception as e:
                errors.append(f"Error deleting {filename}: {str(e)}")
        
        # Build response message
        messages = []
        if deleted_files:
            messages.append(f"Successfully deleted {len(deleted_files)} file{'s' if len(deleted_files) != 1 else ''}")
        if not_found_files:
            messages.append(f"{len(not_found_files)} file{'s' if len(not_found_files) != 1 else ''} not found")
        if errors:
            messages.append(f"{len(errors)} error{'s' if len(errors) != 1 else ''} occurred")
        
        # If there were errors but some files were deleted, return 207 (Multi-Status)
        status_code = 200
        if errors and deleted_files:
            status_code = 207  # Multi-Status
        elif errors and not deleted_files:
            status_code = 400  # Bad Request if nothing was deleted
        elif not_found_files and not deleted_files:
            status_code = 404  # Not Found if no files were found
        
        response = {
            "deleted_files": deleted_files,
            "not_found_files": not_found_files,
            "errors": errors,
            "total_requested": len(request.filenames),
            "total_deleted": len(deleted_files),
            "message": "; ".join(messages) if messages else "No files to delete"
        }
        
        if status_code != 200:
            raise HTTPException(status_code=status_code, detail=response)
        
        return response
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting files: {str(e)}")

# Create documents directory if it doesn't exist
DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)

def is_pdf_file(filename: str) -> bool:
    """Check if the file is a PDF based on file extension."""
    return get_file_extension(filename) == ".pdf"

def validate_pdf_content(content: bytes) -> bool:
    """Validate PDF content by checking PDF signature."""
    # PDF files start with %PDF- signature
    return content.startswith(b'%PDF-')

async def save_pdf_file(file: UploadFile, content: bytes) -> dict:
    """
    Save PDF file with MD5 hash as filename and return file info.
    
    Args:
        file: The uploaded file object
        content: File content bytes
    
    Returns:
        dict: File information including saved path and hash
    
    Raises:
        HTTPException: If file is not a valid PDF
    """
    # Validate file extension
    if not is_pdf_file(file.filename):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF file")
    
    # Validate PDF content
    if not validate_pdf_content(content):
        raise HTTPException(status_code=400, detail=f"File {file.filename} does not contain valid PDF content")
    
    # Calculate MD5 hash
    file_hash = calculate_md5(content)
    
    # Create filename with MD5 hash + .pdf extension
    hashed_filename = f"{file_hash}.pdf"
    file_path = DOCUMENTS_DIR / hashed_filename
    
    # Check if file already exists (duplicate detection)
    file_exists = file_path.exists()
    
    if file_exists:
        # File with same hash already exists, reject the upload
        raise HTTPException(
            status_code=409, 
            detail=f"A PDF file with the same content already exists (hash: {file_hash})"
        )
    
    # Save file to documents directory
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    return {
        "original_filename": file.filename,
        "saved_filename": hashed_filename,
        "file_path": str(file_path),
        "file_hash": file_hash,
        "size": len(content),
        "content_type": file.content_type,
        "storage_location": "documents"
    }

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    PDF file upload endpoint that accepts a single PDF file.
    
    Before accepting the file, computes MD5 hash and checks if a file with 
    the same hash already exists. If a duplicate is detected, rejects the upload 
    and notifies the user. Uploaded files are saved in the 'documents' folder.
    
    Args:
        file: The uploaded PDF file (multipart/form-data)
    
    Returns:
        dict: File information including saved path and hash
    
    Raises:
        HTTPException: 
            - 400: If no file provided, file is not PDF, or invalid PDF content
            - 409: If duplicate file detected (same hash exists)
            - 500: If error processing file
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No PDF file provided")
    
    try:
        # Read the file content
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Save PDF file with duplicate detection
        file_info = await save_pdf_file(file, content)
        
        # Add metadata for the uploaded PDF
        add_upload_metadata(
            original_filename=file.filename,
            stored_filename=file_info["saved_filename"],
            file_size=len(content),
            storage_location="documents"
        )
        
        return {
            "file": file_info,
            "message": f"PDF file '{file.filename}' uploaded successfully",
            "upload_directory": str(DOCUMENTS_DIR)
        }
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF file: {str(e)}")

@router.post("/upload-pdfs")
async def upload_multiple_pdfs(files: List[UploadFile] = File(...)):
    """
    Multiple PDF file upload endpoint that accepts multiple PDF files.
    
    Each file is validated and checked for duplicates before being saved.
    If any file is a duplicate, the entire upload is rejected.
    
    Args:
        files: List of uploaded PDF files (multipart/form-data)
    
    Returns:
        dict: Information about all uploaded PDF files
    
    Raises:
        HTTPException: If any file validation fails or duplicates detected
    """
    if not files:
        raise HTTPException(status_code=400, detail="No PDF files provided")
    
    uploaded_files = []
    total_size = 0
    
    try:
        # First pass: validate all files and check for duplicates
        file_contents = []
        for file in files:
            if not file.filename:
                continue
            
            # Read content
            content = await file.read()
            file_contents.append((file, content))
            
            # Validate file extension
            if not is_pdf_file(file.filename):
                raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF file")
            
            # Validate PDF content
            if not validate_pdf_content(content):
                raise HTTPException(status_code=400, detail=f"File {file.filename} does not contain valid PDF content")
            
            # Check for duplicate
            file_hash = calculate_md5(content)
            hashed_filename = f"{file_hash}.pdf"
            file_path = DOCUMENTS_DIR / hashed_filename
            
            if file_path.exists():
                raise HTTPException(
                    status_code=409,
                    detail=f"PDF file '{file.filename}' already exists (hash: {file_hash})"
                )
        
        # Second pass: save all files (only if all validations passed)
        for file, content in file_contents:
            file_info = await save_pdf_file(file, content)
            uploaded_files.append(file_info)
            total_size += len(content)
            
            # Add metadata
            add_upload_metadata(
                original_filename=file.filename,
                stored_filename=file_info["saved_filename"],
                file_size=len(content),
                storage_location="documents"
            )
        
        if not uploaded_files:
            raise HTTPException(status_code=400, detail="No valid PDF files were uploaded")
        
        return {
            "files": uploaded_files,
            "total_files": len(uploaded_files),
            "total_size": total_size,
            "upload_directory": str(DOCUMENTS_DIR),
            "message": f"Successfully uploaded {len(uploaded_files)} PDF file{'s' if len(uploaded_files) > 1 else ''}"
        }
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF files: {str(e)}")

@router.get("/documents")
async def get_documents():
    """
    Get a list of all uploaded PDF documents.
    
    Returns:
        dict: List of PDF documents with their metadata
    """
    try:
        all_uploads = get_all_uploads_metadata()
        
        # Filter only documents (PDFs stored in documents folder)
        documents = [
            upload for upload in all_uploads 
            if upload.get("storage_location") == "documents"
        ]
        
        return {
            "documents": documents,
            "total_documents": len(documents),
            "storage_directory": str(DOCUMENTS_DIR)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")

@router.delete("/documents")
async def delete_documents(filenames: List[str]):
    """
    Delete multiple PDF documents.
    
    Args:
        filenames: List of stored filenames to delete
        
    Returns:
        dict: Result of the deletion operation
    """
    try:
        deleted_files = []
        not_found_files = []
        error_files = []
        
        for filename in filenames:
            try:
                # Remove from documents directory
                file_path = DOCUMENTS_DIR / filename
                if file_path.exists():
                    file_path.unlink()
                    deleted_files.append(filename)
                    
                    # Remove from metadata
                    remove_upload_metadata(filename)
                else:
                    not_found_files.append(filename)
                    
            except Exception as e:
                error_files.append({"filename": filename, "error": str(e)})
        
        return {
            "message": f"Deletion completed. {len(deleted_files)} files deleted.",
            "deleted_files": deleted_files,
            "not_found_files": not_found_files,
            "error_files": error_files,
            "total_requested": len(filenames),
            "total_deleted": len(deleted_files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting documents: {str(e)}")

@router.post("/upload-knowledge")
async def upload_knowledge(
    file: UploadFile = File(..., max_size=500*1024*1024),  # Max 500MB file size
    system_type: str = Form(...)
):
    """
    Upload Excel/CSV knowledge file for UMS system and save to SQL Server InspectionData table.
    
    Args:
        file: The uploaded Excel/CSV file
        system_type: The system type (UMS or KOMTRAX)
    
    Returns:
        dict: Upload result with records processed count
    
    Raises:
        HTTPException: If file validation fails or database error occurs
    """
    
    # Check if SQL Server dependencies are available
    if not SQL_SERVER_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="SQL Server functionality not available. Missing required dependencies (pandas, pyodbc, sqlalchemy)."
        )
    
    # Debug: Print received system type
    print(f"🔍 UPLOAD DEBUG: Received system_type = '{system_type}' (type: {type(system_type)})")
    
    # Validate system type
    if system_type not in ['UMS', 'KOMTRAX', 'Expected Lifetime']:
        raise HTTPException(
            status_code=400, 
            detail="Invalid system type. Must be 'UMS', 'KOMTRAX', or 'Expected Lifetime'"
        )
    
    # Validate file type
    allowed_types = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        'application/vnd.ms-excel',  # .xls
        'text/csv'  # .csv
    ]
    
    allowed_extensions = ['.xlsx', '.xls', '.csv']
    file_extension = Path(file.filename).suffix.lower()
    
    if file.content_type not in allowed_types and file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only Excel (.xlsx, .xls) and CSV files are allowed."
        )
    
    # Validate file size (50MB limit)
    max_file_size = 50 * 1024 * 1024  # 50MB
    
    try:
        # Read file content
        contents = await file.read()
        
        if len(contents) > max_file_size:
            raise HTTPException(
                status_code=400, 
                detail="File size too large. Maximum file size is 50MB."
            )
        
        # Parse Excel/CSV file
        try:
            if file_extension == '.csv':
                df = pd.read_csv(io.BytesIO(contents))
            else:
                df = pd.read_excel(io.BytesIO(contents))
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Error reading file: {str(e)}. Please ensure the file is a valid Excel or CSV file."
            )
        
        if df.empty:
            raise HTTPException(
                status_code=400, 
                detail="The uploaded file is empty or contains no data."
            )
        
        # Test database connection with fallback to simulation
        try:
            print(f"🔍 Testing SQL Server connection to {sql_server.server}...")
            connection_available = sql_server.test_connection()
            print(f"✅ Connection test result: {connection_available}")
        except Exception as e:
            print(f"⚠️  SQL Server connection test failed with exception: {str(e)}")
            connection_available = False
        
        # If database connection fails, return simulation response
        if not connection_available:
            target_table = get_target_table(system_type)
            print(f"📊 Database not available - returning simulation response for {len(df)} records")
            return {
                "success": True,
                "message": f"Knowledge file processed successfully (simulation mode). Table '{target_table}' would be truncated and {len(df)} records inserted.",
                "records_processed": len(df),
                "system_type": system_type,
                "filename": file.filename,
                "database_table": target_table,
                "mode": "simulation",
                "table_truncated": False,
                "note": f"Database connection not available. Table '{target_table}' would be truncated and {len(df)} records inserted to RAGPrototipe.{target_table} when SQL Server is accessible.",
                "columns_detected": list(df.columns),
                "upload_timestamp": datetime.now().isoformat()
            }
        
        # Process based on system type
        print(f"🎯 PROCESSING: system_type = '{system_type}'")
        if system_type == "KOMTRAX":
            print("✅ KOMTRAX branch selected - using Machine_Tracking table")
            # KOMTRAX system - use Machine_Tracking table
            df_filtered = filter_excel_columns_for_machine_tracking(df)
            column_mapping = map_excel_to_machine_tracking_columns(df_filtered)
            df_mapped = df_filtered.rename(columns=column_mapping)
            all_db_columns = get_all_machine_tracking_columns()
            target_table = "Machine_Tracking"
            
            # Add missing columns with NULL values
            for col in all_db_columns:
                if col not in df_mapped.columns:
                    df_mapped[col] = None
            
            # Ensure only existing database columns are included
            final_columns = [col for col in all_db_columns if col in df_mapped.columns]
            df_final = df_mapped[final_columns]
            
        elif system_type == "Expected Lifetime":
            print("✅ Expected Lifetime branch selected - using UC_Life_Time table")
            # Expected Lifetime system - use UC_Life_Time table
            df_filtered = filter_excel_columns_for_uc_lifetime(df)
            column_mapping = map_excel_to_uc_lifetime_columns(df_filtered)
            df_mapped = df_filtered.rename(columns=column_mapping)
            all_db_columns = get_all_uc_lifetime_columns()
            target_table = "UC_Life_Time"
            
            # Add missing columns with NULL values
            for col in all_db_columns:
                if col not in df_mapped.columns:
                    df_mapped[col] = None
            
            # Clean and convert data types for UC_Life_Time
            numeric_columns = ['General_Sand', 'Soil', 'Marsh', 'Coal', 'Hard_Rock', 'Brittle_Rock', 'Pure_Sand_Middle_East']
            
            for col in numeric_columns:
                if col in df_mapped.columns:
                    # Convert to numeric, handle non-numeric values
                    df_mapped[col] = pd.to_numeric(df_mapped[col], errors='coerce')
                    print(f"🔢 Converted {col} to numeric")
            
            # Model and Component should be string
            string_columns = ['Model', 'Component']
            for col in string_columns:
                if col in df_mapped.columns:
                    df_mapped[col] = df_mapped[col].astype(str).replace('nan', '')
                    print(f"📝 Converted {col} to string")
            
            # Ensure only existing database columns are included
            final_columns = [col for col in all_db_columns if col in df_mapped.columns]
            df_final = df_mapped[final_columns]
            
            print(f"📊 Final DataFrame shape: {df_final.shape}")
            print(f"📊 Final columns: {list(df_final.columns)}")
            
        else:
            print("✅ UMS branch selected - using InspectionData table")
            # UMS system - use InspectionData table
            df_filtered = filter_excel_columns_for_database(df)
            column_mapping = map_excel_to_database_columns(df_filtered)
            df_mapped = df_filtered.rename(columns=column_mapping)
            
            # Handle duplicate columns after mapping (e.g., 'Equipment Number' and 'Machine ID' both map to 'Equipment_Number')
            duplicate_cols = df_mapped.columns[df_mapped.columns.duplicated()].tolist()
            if duplicate_cols:
                print(f"⚠️  Found duplicate columns after mapping: {duplicate_cols}")
                # Keep only the first occurrence of each column and drop duplicates
                df_mapped = df_mapped.loc[:, ~df_mapped.columns.duplicated()]
                print(f"✅ Removed duplicate columns. Final columns: {len(df_mapped.columns)}")
            
            all_db_columns = get_all_inspection_data_columns()
            target_table = "InspectionData"
            
            # Add filename and upload info only if columns exist in database
            if 'Comments' in all_db_columns and df_mapped['Comments'].isna().all():
                df_mapped['Comments'] = f'Uploaded from {file.filename} via UMS system'
            if 'Attachments' in all_db_columns and df_mapped['Attachments'].isna().all():
                df_mapped['Attachments'] = file.filename
            
            # Only keep columns that actually exist in the database, in database order
            # Use database column order to ensure consistent SQL parameter binding
            # Exclude ID column since it's auto-increment
            available_columns = set(df_mapped.columns)
            final_columns = [col for col in all_db_columns if col in available_columns and col != 'ID']
            df_final = df_mapped[final_columns]
            
            print(f"📊 Filtered to {len(final_columns)} existing database columns")
            print(f"📊 Final columns: {list(df_final.columns)[:10]}{'...' if len(df_final.columns) > 10 else ''}")
            
            # Convert data types to match database schema
            print("🔄 Converting data types to match database schema...")
            
            # Integer columns
            int_columns = ['ID', 'Inspection_ID', 'SMR', 
                          'LinkPitch_History_SMR_LHS', 'LinkPitch_History_SMR_RHS',
                          'Bushings_History_SMR_LHS', 'Bushings_History_SMR_RHS',
                          'LinkHeight_History_SMR_LHS', 'LinkHeight_History_SMR_RHS',
                          'TrackShoe_History_SMR_LHS', 'TrackShoe_History_SMR_RHS',
                          'Idlers_History_SMR_LHS1', 'Idlers_History_SMR_RHS1',
                          'Sprocket_History_SMR_LHS', 'Sprocket_History_SMR_RHS']
                          
            # Date columns  
            date_columns = ['Delivery_Date', 'Inspection_Date',
                           'LinkPitch_History_Date_LHS', 'LinkPitch_History_Date_RHS',
                           'LinkPitch_ReplaceDate_LHS', 'LinkPitch_ReplaceDate_RHS',
                           'Bushings_History_Date_LHS', 'Bushings_History_Date_RHS',
                           'Bushings_ReplaceDate_LHS', 'Bushings_ReplaceDate_RHS',
                           'LinkHeight_History_Date_LHS', 'LinkHeight_History_Date_RHS',
                           'LinkHeight_ReplaceDate_LHS', 'LinkHeight_ReplaceDate_RHS',
                           'TrackShoe_History_Date_LHS', 'TrackShoe_History_Date_RHS',
                           'TrackShoe_ReplaceDate_LHS', 'TrackShoe_ReplaceDate_RHS',
                           'Idlers_History_Date_LHS1', 'Idlers_History_Date_RHS1',
                           'Idlers_ReplaceDate_LHS1', 'Idlers_ReplaceDate_RHS1',
                           'Sprocket_History_Date_LHS', 'Sprocket_History_Date_RHS',
                           'Sprocket_ReplaceDate_LHS', 'Sprocket_ReplaceDate_RHS']
                           
            # Decimal columns (for percentages, hours, measurements)
            decimal_columns = ['WorkingHourPerDay', 'TrackShoe_Width',
                              'LinkPitch_History_Hours_LHS', 'LinkPitch_History_Hours_RHS',
                              'LinkPitch_PercentWorn_LHS', 'LinkPitch_PercentWorn_RHS',
                              'Bushings_History_Hours_LHS', 'Bushings_History_Hours_RHS', 
                              'Bushings_PercentWorn_LHS', 'Bushings_PercentWorn_RHS',
                              'LinkHeight_History_Hours_LHS', 'LinkHeight_History_Hours_RHS',
                              'LinkHeight_PercentWorn_LHS', 'LinkHeight_PercentWorn_RHS',
                              'TrackShoe_History_Hours_LHS', 'TrackShoe_History_Hours_RHS',
                              'TrackShoe_PercentWorn_LHS', 'TrackShoe_PercentWorn_RHS',
                              'Idlers_History_Hours_LHS1', 'Idlers_History_Hours_RHS1',
                              'Idlers_PercentWorn_LHS1', 'Idlers_PercentWorn_RHS1',
                              'Sprocket_History_Hours_LHS', 'Sprocket_History_Hours_RHS',
                              'Sprocket_PercentWorn_LHS', 'Sprocket_PercentWorn_RHS']
            
            # Convert integer columns
            for col in int_columns:
                if col in df_final.columns:
                    df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('Int64')
                    print(f"  ✅ Converted {col} to integer")
            
            # Convert date columns
            for col in date_columns:
                if col in df_final.columns:
                    df_final[col] = pd.to_datetime(df_final[col], errors='coerce')
                    print(f"  ✅ Converted {col} to datetime")
            
            # Convert decimal columns  
            for col in decimal_columns:
                if col in df_final.columns:
                    df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
                    print(f"  ✅ Converted {col} to decimal")
            
            # ID column is already excluded during column filtering above
            
        # Clean NULL values for pyodbc compatibility
        print("🧹 Cleaning NULL values for pyodbc compatibility...")
        
        # Replace pandas NaT and numpy NaN with Python None
        for col in df_final.columns:
            # Handle datetime columns - replace NaT with None
            if df_final[col].dtype == 'datetime64[ns]':
                df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
                
            # Handle nullable integer columns - replace <NA> with None  
            elif str(df_final[col].dtype).startswith('Int'):
                df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
                
            # Handle float columns - replace NaN with None
            elif df_final[col].dtype in ['float64', 'float32']:
                df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
                
            # Handle object columns - replace NaN with None
            elif df_final[col].dtype == 'object':
                df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
        
        # Convert numpy types to native Python types to avoid pyodbc issues
        print("🔧 Converting numpy types to native Python types...")
        
        for col in df_final.columns:
            dtype_str = str(df_final[col].dtype)
            
            if dtype_str.startswith('Int') or dtype_str in ['int64', 'int32', 'int16', 'int8']:
                # Convert all integer types (including numpy.int64) to Python int or None
                def convert_int(x):
                    if pd.isna(x) or x is None:
                        return None
                    try:
                        return int(x)  # This converts numpy.int64 to Python int
                    except (ValueError, TypeError):
                        return None
                        
                df_final[col] = df_final[col].apply(convert_int)
                print(f"  ✅ Converted {col} from {dtype_str} to Python int")
                
            elif dtype_str in ['float64', 'float32', 'float16']:
                # Convert all float types to Python float or None
                def convert_float(x):
                    if pd.isna(x) or x is None:
                        return None
                    try:
                        return float(x)
                    except (ValueError, TypeError):
                        return None
                        
                df_final[col] = df_final[col].apply(convert_float)
                print(f"  ✅ Converted {col} from {dtype_str} to Python float")
        
        print(f"✅ NULL value handling and type conversion completed")
        
        # Truncate table before inserting new data
        try:
            print(f"🗑️  Truncating table '{target_table}' before upload...")
            sql_server.truncate_table(target_table)
            print(f"✅ Table '{target_table}' truncated successfully")
        except Exception as truncate_error:
            print(f"⚠️  Warning: Failed to truncate table '{target_table}': {str(truncate_error)}")
            # Continue with insert even if truncate fails
        
        # Insert data to SQL Server
        try:
            records_processed = sql_server.insert_dataframe_to_table(
                df_final, 
                target_table, 
                if_exists='append'
            )
            
            return {
                "success": True,
                "message": f"Knowledge file uploaded successfully. Table '{target_table}' was truncated and {records_processed} records were inserted.",
                "records_processed": records_processed,
                "system_type": system_type,
                "filename": file.filename,
                "total_columns_mapped": len(column_mapping),
                "database_table": target_table,
                "table_truncated": True,
                "upload_timestamp": datetime.now().isoformat()
            }
            
        except Exception as db_error:
            raise HTTPException(
                status_code=500, 
                detail=f"Database insertion failed: {str(db_error)}"
            )
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing file: {str(e)}"
        )

@router.get("/test-database-connection")
async def test_database_connection(system_type: str = "UMS"):
    """
    Test SQL Server database connection for knowledge upload.
    
    Args:
        system_type: The system type (UMS or KOMTRAX) to determine target table
    
    Returns:
        dict: Connection test result with database info
    """
    
    # Check if SQL Server dependencies are available
    if not SQL_SERVER_AVAILABLE:
        return {
            "success": False,
            "message": "SQL Server functionality not available. Missing required dependencies (pandas, pyodbc, sqlalchemy).",
            "database": "Not configured",
            "server": "Not configured",
            "mode": "simulation_only"
        }
    
    try:
        print(f"🔍 Testing database connection to {sql_server.server}:{sql_server.port}")
        is_connected = sql_server.test_connection()
        print(f"📊 Connection test result: {is_connected}")
        
        # Determine target table based on system type
        target_table = get_target_table(system_type)
        
        if is_connected:
            response_data = {
                "success": True,
                "message": "Database connection successful",
                "database": sql_server.database,
                "server": f"{sql_server.server}:{sql_server.port}",
                "target_table": target_table,
                "system_type": system_type,
                "mode": "database_available"
            }
            return response_data
        else:
            return {
                "success": False,
                "message": "Database connection failed - using simulation mode",
                "database": sql_server.database,
                "server": f"{sql_server.server}:{sql_server.port}",
                "mode": "simulation_fallback",
                "note": "Check if SQL Server is running and accessible"
            }
    except Exception as e:
        print(f"⚠️ Database connection test error: {str(e)}")
        return {
            "success": False,
            "message": f"Database connection error: {str(e)}",
            "database": sql_server.database,
            "server": f"{sql_server.server}:{sql_server.port}",
            "mode": "simulation_fallback",
            "error": str(e)
        }

@router.get("/test-db-new")
async def test_database_connection_new(system_type: str = "UMS"):
    """New test endpoint to verify system_type functionality"""
    
    if not SQL_SERVER_AVAILABLE:
        return {
            "success": False,
            "message": "SQL Server functionality not available.",
            "system_type": system_type,
            "target_table": get_target_table(system_type)
        }
    
    try:
        is_connected = sql_server.test_connection()
        target_table = get_target_table(system_type)
        
        return {
            "success": is_connected,
            "message": "Database connection successful" if is_connected else "Connection failed",
            "database": sql_server.database,
            "server": f"{sql_server.server}:{sql_server.port}",
            "target_table": target_table,
            "system_type": system_type,
            "mode": "database_available" if is_connected else "simulation_fallback"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "system_type": system_type,
            "target_table": get_target_table(system_type)
        }