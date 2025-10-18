# import os
# import json
# import pdfplumber
# import camelot
# import pandas as pd
# import re
# from pathlib import Path
# from datetime import datetime
# import hashlib
# import numpy as np
# from difflib import SequenceMatcher

# # --------------------------
# # 📁 CONFIGURATION
# # --------------------------
# FORMAT_REGISTRY_PATH = "auto_formats13.json"
# OUTPUT_BASE_DIR = "strctured_work3"

# # --------------------------
# # 🧠 ENHANCED CLEAN FORMAT MANAGER
# # --------------------------
# class CleanFormatManager:
#     def __init__(self):
#         self.formats = self.load_formats()
#         self.setup_directories()
    
#     def load_formats(self):
#         if os.path.exists(FORMAT_REGISTRY_PATH):
#             with open(FORMAT_REGISTRY_PATH, 'r') as f:
#                 return json.load(f)
#         return {}
    
#     def save_formats(self):
#         with open(FORMAT_REGISTRY_PATH, 'w') as f:
#             json.dump(self.formats, f, indent=2)
    
#     def setup_directories(self):
#         os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    
#     def create_format_signature(self, df):
#         """Create precise signature from ACTUAL column names with content validation"""
#         if df.empty or len(df.columns) < 2:
#             return None
        
#         # Use ONLY actual column names with enhanced cleaning
#         original_columns = [str(col).strip() for col in df.columns]
        
#         # Filter out completely empty column names
#         non_empty_columns = [col for col in original_columns if col and col.strip()]
        
#         if len(non_empty_columns) < 2:
#             return None
            
#         # Enhanced column cleaning with semantic preservation
#         cleaned_columns = []
#         for col in non_empty_columns:
#             cleaned = self.enhanced_column_cleaning(col)
#             if cleaned:
#                 cleaned_columns.append(cleaned)
        
#         if len(cleaned_columns) < 2:
#             return None
            
#         # Create signature with column order preservation for better accuracy
#         signature_string = "|".join(cleaned_columns)
#         return hashlib.md5(signature_string.encode()).hexdigest()
    
#     def enhanced_column_cleaning(self, column_text):
#         """Enhanced column cleaning while preserving semantic meaning"""
#         if not isinstance(column_text, str):
#             column_text = str(column_text)
        
#         # Remove extra whitespace, newlines, tabs
#         cleaned = re.sub(r'[\n\r\t]', ' ', column_text)
#         cleaned = ' '.join(cleaned.split())
        
#         # Preserve special characters that might be meaningful in headers
#         # Remove only excessive special characters
#         cleaned = re.sub(r'[^\w\s\.\-\_\@\#\$\%\&\*\(\)]', '', cleaned)
        
#         return cleaned.lower().strip()
    
#     def find_matching_format(self, df):
#         """Find matching format with similarity threshold"""
#         if not self.formats:
#             return None
        
#         current_signature = self.create_format_signature(df)
#         if not current_signature:
#             return None
        
#         # Exact signature match
#         for format_name, format_data in self.formats.items():
#             if format_data.get('signature') == current_signature:
#                 return format_name
        
#         # Fallback: Similarity-based matching for 100% accuracy
#         return self.find_similar_format(df)
    
#     def find_similar_format(self, df, similarity_threshold=0.95):
#         """Find similar format using column name similarity"""
#         current_columns = [self.enhanced_column_cleaning(str(col)) for col in df.columns if str(col).strip()]
        
#         best_match = None
#         highest_similarity = 0
        
#         for format_name, format_data in self.formats.items():
#             stored_columns = format_data.get('columns', [])
            
#             if len(current_columns) != len(stored_columns):
#                 continue
                
#             # Calculate column-by-column similarity
#             total_similarity = 0
#             for current_col, stored_col in zip(current_columns, stored_columns):
#                 similarity = SequenceMatcher(None, current_col, stored_col).ratio()
#                 total_similarity += similarity
            
#             avg_similarity = total_similarity / len(current_columns)
            
#             if avg_similarity > highest_similarity and avg_similarity >= similarity_threshold:
#                 highest_similarity = avg_similarity
#                 best_match = format_name
        
#         if best_match:
#             print(f"🔍 Similar format found: {best_match} (similarity: {highest_similarity:.2f})")
        
#         return best_match
    
#     def learn_new_format(self, df, source_pdf):
#         """Learn new format with duplicate prevention"""
#         format_signature = self.create_format_signature(df)
        
#         if not format_signature:
#             return None
        
#         # Check for exact duplicate format
#         for existing_name, existing_data in self.formats.items():
#             if existing_data.get('signature') == format_signature:
#                 print(f"🔄 Format already exists: {existing_name}")
#                 return existing_name
        
#         # Check for similar formats to avoid near-duplicates
#         similar_format = self.find_similar_format(df, similarity_threshold=0.98)
#         if similar_format:
#             print(f"🔄 Very similar format exists: {similar_format}")
#             return similar_format
        
#         format_name = self.generate_simple_format_name(df)
        
#         # Store ONLY the actual column names with enhanced cleaning
#         actual_columns = [self.enhanced_column_cleaning(str(col)) for col in df.columns if str(col).strip()]
        
#         new_format = {
#             'signature': format_signature,
#             'columns': actual_columns,  # ONLY actual column names
#             'column_count': len(actual_columns),
#             'output_folder': os.path.join(OUTPUT_BASE_DIR, format_name),
#             'created_date': datetime.now().isoformat(),
#             'learned_from': os.path.basename(source_pdf),
#             'sample_data_shape': f"{len(df)}x{len(df.columns)}"
#         }
        
#         os.makedirs(new_format['output_folder'], exist_ok=True)
#         self.formats[format_name] = new_format
#         self.save_formats()
        
#         print(f"✅ LEARNED NEW FORMAT: {format_name}")
#         print(f"   Columns: {', '.join(actual_columns)}")
#         print(f"   Shape: {new_format['sample_data_shape']}")
        
#         return format_name
    
#     def generate_simple_format_name(self, df):
#         """Generate unique format name based on actual column content"""
#         base_name = "Format"
#         actual_columns = [self.enhanced_column_cleaning(str(col)) for col in df.columns if str(col).strip()]
#         column_count = len(actual_columns)
        
#         if len(actual_columns) >= 2:
#             # Use first 2 meaningful column names
#             name_parts = []
#             for col in actual_columns[:2]:
#                 # Clean column name for filename
#                 clean_col = re.sub(r'[^\w\s]', '', col)
#                 clean_col = '_'.join(clean_col.split()[:2])  # Use first 2 words max
#                 if clean_col and len(clean_col) > 1:
#                     name_parts.append(clean_col)
            
#             if name_parts:
#                 name_candidate = f"{base_name}_{'_'.join(name_parts)}_{column_count}col"
                
#                 # Ensure uniqueness
#                 counter = 1
#                 final_name = name_candidate
#                 while final_name in self.formats:
#                     final_name = f"{name_candidate}_{counter}"
#                     counter += 1
                
#                 return final_name
        
#         # Fallback naming
#         base_format_name = f"{base_name}_{column_count}col"
#         counter = 1
#         final_name = base_format_name
#         while final_name in self.formats:
#             final_name = f"{base_format_name}_{counter}"
#             counter += 1
        
#         return final_name

# # --------------------------
# # 📄 ENHANCED STRICT COLUMN EXTRACTOR
# # --------------------------
# class StrictColumnExtractor:
#     def __init__(self, format_manager):
#         self.format_manager = format_manager
    
#     def extract_tables_from_pdf(self, pdf_path):
#         """Enhanced table extraction with multiple strategies"""
#         all_tables = []
        
#         print("🔍 Extracting tables with enhanced detection...")
        
#         # Strategy 1: pdfplumber with actual headers
#         tables1 = self.extract_with_actual_headers(pdf_path)
#         if tables1:
#             print(f"📊 Found {len(tables1)} tables with proper headers (Strategy 1)")
#             all_tables.extend(tables1)
        
#         # Strategy 2: Camelot for complex tables
#         tables2 = self.extract_with_camelot(pdf_path)
#         if tables2:
#             print(f"📊 Found {len(tables2)} tables with Camelot (Strategy 2)")
#             all_tables.extend(tables2)
        
#         # Remove duplicate tables
#         unique_tables = self.remove_duplicate_tables(all_tables)
        
#         return unique_tables
    
#     def extract_with_actual_headers(self, pdf_path):
#         """Enhanced table extraction with better header detection"""
#         tables = []
#         try:
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page_num, page in enumerate(pdf.pages):
#                     print(f"📄 Analyzing page {page_num + 1} for structured tables...")
                    
#                     # Try multiple table detection strategies
#                     table_strategies = [
#                         {"vertical_strategy": "lines", "horizontal_strategy": "lines"},
#                         {"vertical_strategy": "text", "horizontal_strategy": "text"},
#                         {"vertical_strategy": "explicit", "horizontal_strategy": "explicit"}
#                     ]
                    
#                     for strategy_num, table_settings in enumerate(table_strategies):
#                         try:
#                             detected_tables = page.find_tables(table_settings)
                            
#                             for table_num, table in enumerate(detected_tables):
#                                 table_data = table.extract()
                                
#                                 if table_data and len(table_data) >= 2:  # At least header + one data row
#                                     df = self.create_enhanced_dataframe(table_data, page_num, table_num, strategy_num)
#                                     if df is not None and not df.empty and self.has_proper_headers(df):
#                                         tables.append(df)
#                                         print(f"   ✅ Strategy {strategy_num+1}: Table {table_num+1} - {len(df)}x{len(df.columns)}")
#                         except Exception as e:
#                             continue  # Try next strategy
        
#         except Exception as e:
#             print(f"❌ PDF extraction failed: {e}")
        
#         return tables
    
#     def extract_with_camelot(self, pdf_path):
#         """Use Camelot as fallback for complex tables"""
#         tables = []
#         try:
#             print("   Trying Camelot extraction...")
#             camelot_tables = camelot.read_pdf(pdf_path, flavor='lattice', pages='all')
            
#             for i, table in enumerate(camelot_tables):
#                 if table.parsing_report and table.parsing_report.get('accuracy', 0) > 80:
#                     df = table.df
                    
#                     # Clean and validate the table
#                     if not df.empty and len(df.columns) >= 2 and len(df) >= 2:
#                         # Try to identify header row
#                         df_with_headers = self.identify_camelot_headers(df)
#                         if df_with_headers is not None and self.has_proper_headers(df_with_headers):
#                             cleaned_df = self.clean_dataframe(df_with_headers)
#                             if not cleaned_df.empty:
#                                 tables.append(cleaned_df)
#                                 print(f"   ✅ Camelot Table {i+1} - {len(cleaned_df)}x{len(cleaned_df.columns)}")
        
#         except Exception as e:
#             print(f"   ⚠️ Camelot extraction failed: {e}")
        
#         return tables
    
#     def identify_camelot_headers(self, df):
#         """Identify header row in Camelot extracted tables"""
#         if df.empty:
#             return None
        
#         # Check if first row contains header-like content
#         first_row = df.iloc[0].values
#         if self.is_header_row(first_row):
#             # Use first row as header
#             new_columns = [self.clean_text(str(cell)) for cell in first_row]
#             new_df = df.iloc[1:].copy()
#             new_df.columns = new_columns
#             new_df = new_df.reset_index(drop=True)
#             return new_df
        
#         # If no clear header, use generic column names but mark as no-header
#         return df
    
#     def create_enhanced_dataframe(self, table_data, page_num, table_num, strategy_num):
#         """Enhanced DataFrame creation with better header validation"""
#         try:
#             if not table_data or len(table_data) < 2:
#                 return None
            
#             # Find the best header row
#             header_row_index = self.find_best_header_row(table_data)
            
#             if header_row_index is None:
#                 print(f"   ⏭️ Table {table_num+1}: No suitable header row found")
#                 return None
            
#             # Use identified header row
#             headers = []
#             for cell in table_data[header_row_index]:
#                 if cell is not None:
#                     clean_header = self.clean_text(str(cell))
#                     if clean_header:
#                         headers.append(clean_header)
#                     else:
#                         headers.append(f"Column_{len(headers)+1}")
#                 else:
#                     headers.append(f"Column_{len(headers)+1}")
            
#             # Extract data rows (skip header row)
#             rows = []
#             for i, row in enumerate(table_data):
#                 if i != header_row_index:  # Skip header row
#                     clean_row = [self.clean_text(str(cell)) if cell is not None else "" for cell in row]
#                     if any(cell.strip() for cell in clean_row):  # Only add non-empty rows
#                         rows.append(clean_row)
            
#             if headers and rows:
#                 # Ensure consistent columns
#                 max_cols = len(headers)
#                 normalized_rows = []
#                 for row in rows:
#                     if len(row) < max_cols:
#                         row.extend([''] * (max_cols - len(row)))
#                     elif len(row) > max_cols:
#                         row = row[:max_cols]
#                     normalized_rows.append(row)
                
#                 df = pd.DataFrame(normalized_rows, columns=headers)
#                 return df
                
#         except Exception as e:
#             print(f"⚠️ Error creating enhanced dataframe: {e}")
        
#         return None
    
#     def find_best_header_row(self, table_data):
#         """Find the best row to use as headers"""
#         if not table_data:
#             return None
        
#         best_row_index = 0
#         best_header_score = 0
        
#         for i, row in enumerate(table_data[:3]):  # Check first 3 rows
#             if not row:
#                 continue
                
#             header_score = self.calculate_header_score(row)
#             if header_score > best_header_score:
#                 best_header_score = header_score
#                 best_row_index = i
        
#         # Only use as header if score is above threshold
#         if best_header_score > 0.7:
#             return best_row_index
        
#         return None
    
#     def calculate_header_score(self, row):
#         """Calculate how likely a row is to be a header row"""
#         if not row:
#             return 0
        
#         header_like_count = 0
#         total_cells = 0
        
#         for cell in row:
#             if cell is None:
#                 continue
                
#             cell_str = str(cell).strip()
#             if not cell_str:
#                 continue
            
#             total_cells += 1
            
#             # Enhanced header detection criteria
#             is_header_like = (
#                 len(cell_str) <= 50 and                    # Not too long
#                 cell_str.count(' ') <= 8 and               # Reasonable word count
#                 not cell_str.replace('.', '').replace(',', '').replace('$', '').isdigit() and # Not just numbers
#                 not re.match(r'^\d+[/-]\d+[/-]\d+$', cell_str) and  # Not dates
#                 not re.match(r'^[+-]?\$?\d+[,\.]?\d*$', cell_str) and  # Not amounts
#                 len(cell_str) >= 2 and                     # Not too short
#                 not cell_str.isupper() or len(cell_str) <= 5  # All caps ok for short text
#             )
            
#             if is_header_like:
#                 header_like_count += 1
        
#         if total_cells == 0:
#             return 0
        
#         return header_like_count / total_cells
    
#     def is_header_row(self, row):
#         """Check if a row contains actual column headers"""
#         return self.calculate_header_score(row) > 0.6
    
#     def has_proper_headers(self, df):
#         """Enhanced header validation"""
#         if df.empty:
#             return False
        
#         # Count non-empty, meaningful column names
#         meaningful_headers = 0
#         for col in df.columns:
#             col_str = str(col).strip()
#             if (col_str and 
#                 len(col_str) >= 1 and  # Reduced minimum length
#                 len(col_str) <= 100 and # Increased maximum length
#                 col_str != "Unnamed: 0" and
#                 not re.match(r'^Column_\d+$', col_str)):
#                 meaningful_headers += 1
        
#         # Need at least 2 meaningful column headers
#         return meaningful_headers >= 2
    
#     def clean_text(self, text):
#         """Clean text - remove extra whitespace but preserve content exactly"""
#         if not isinstance(text, str):
#             text = str(text)
        
#         # Replace newlines and tabs with spaces
#         cleaned = re.sub(r'[\n\r\t]', ' ', text)
#         # Normalize whitespace but preserve original content
#         cleaned = ' '.join(cleaned.split())
#         return cleaned.strip()
    
#     def remove_duplicate_tables(self, tables):
#         """Remove duplicate tables based on content and structure"""
#         unique_tables = []
#         table_signatures = set()
        
#         for table in tables:
#             if table.empty:
#                 continue
                
#             # Create signature based on column names and first few rows
#             col_signature = "|".join([str(col) for col in table.columns])
#             data_signature = "|".join([str(table.iloc[i].values) for i in range(min(2, len(table)))])
#             signature = hashlib.md5((col_signature + data_signature).encode()).hexdigest()
            
#             if signature not in table_signatures:
#                 table_signatures.add(signature)
#                 unique_tables.append(table)
#             else:
#                 print("   🔄 Removing duplicate table")
        
#         return unique_tables
    
#     def clean_dataframe(self, df):
#         """Clean dataframe - preserve original structure exactly"""
#         if df.empty:
#             return df
        
#         df_cleaned = df.copy()
        
#         # Clean column names but preserve original content
#         df_cleaned.columns = [self.clean_column_name(col) for col in df_cleaned.columns]
        
#         # Clean cell data without merging or modifying structure
#         for col in df_cleaned.columns:
#             df_cleaned[col] = df_cleaned[col].apply(
#                 lambda x: self.clean_text(x) if pd.notna(x) and str(x).strip() else ""
#             )
        
#         # Remove completely empty rows (all cells empty)
#         df_cleaned = df_cleaned[df_cleaned.astype(str).apply(
#             lambda x: ''.join(x).strip() != '', axis=1
#         )]
        
#         # Reset index but preserve original order
#         df_cleaned = df_cleaned.reset_index(drop=True)
        
#         return df_cleaned
    
#     def clean_column_name(self, col_name):
#         """Clean column name - preserve original meaning"""
#         cleaned = self.clean_text(col_name)
#         return cleaned if cleaned else f"Column_{hash(col_name) % 10000}"

# # --------------------------
# # 🚀 ENHANCED CLEAN PROCESSOR
# # --------------------------
# class CleanPDFProcessor:
#     def __init__(self):
#         self.format_manager = CleanFormatManager()
#         self.extractor = StrictColumnExtractor(self.format_manager)
    
#     def process_pdf(self, pdf_path):
#         """Enhanced PDF processing with better accuracy"""
#         if not os.path.exists(pdf_path):
#             print(f"❌ File not found: {pdf_path}")
#             return
        
#         print(f"\n🎯 PROCESSING: {os.path.basename(pdf_path)}")
#         print("=" * 60)
        
#         # Extract tables with enhanced detection
#         tables = self.extractor.extract_tables_from_pdf(pdf_path)
        
#         if not tables:
#             print("❌ No valid tables found in PDF")
#             return
        
#         print(f"📊 Found {len(tables)} unique tables with proper headers")
        
#         format_tables = {}
#         processed_count = 0
        
#         for i, table in enumerate(tables):
#             # Clean the table (preserves original structure)
#             cleaned_table = self.extractor.clean_dataframe(table)
            
#             if cleaned_table.empty or len(cleaned_table.columns) < 2:
#                 print(f"⚠️ Table {i+1} is empty or has too few columns, skipping")
#                 continue
            
#             print(f"\n📋 Table {i+1}:")
#             print(f"   Rows: {len(cleaned_table)}")
#             print(f"   Columns: {len(cleaned_table.columns)}")
#             print(f"   Headers: {list(cleaned_table.columns)}")
            
#             # Find matching format or learn new one
#             format_name = self.format_manager.find_matching_format(cleaned_table)
            
#             if format_name:
#                 print(f"   ✅ Matched existing format: {format_name}")
#             else:
#                 format_name = self.format_manager.learn_new_format(cleaned_table, pdf_path)
#                 if format_name:
#                     print(f"   🆕 Learned new format: {format_name}")
            
#             if format_name:
#                 if format_name not in format_tables:
#                     format_tables[format_name] = []
#                 format_tables[format_name].append(cleaned_table)
#                 processed_count += 1
        
#         # Save consolidated tables
#         for format_name, tables_list in format_tables.items():
#             if tables_list:
#                 self.save_consolidated_tables(tables_list, format_name, pdf_path)
        
#         print(f"\n✅ COMPLETED: {os.path.basename(pdf_path)}")
#         print(f"📈 Successfully processed {processed_count}/{len(tables)} tables")
    
#     def save_consolidated_tables(self, tables, format_name, source_pdf):
#         """Save tables to Excel with enhanced formatting"""
#         format_data = self.format_manager.formats[format_name]
#         output_folder = format_data['output_folder']
        
#         source_name = Path(source_pdf).stem
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"{format_name}_{source_name}_{timestamp}.xlsx"
#         output_path = os.path.join(output_folder, filename)
        
#         try:
#             with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#                 for i, table in enumerate(tables):
#                     sheet_name = f"Table_{i+1}"
#                     if len(sheet_name) > 31:
#                         sheet_name = f"T_{i+1}"
                    
#                     # Save exactly as is, no modifications
#                     table.to_excel(writer, sheet_name=sheet_name, index=False)
                    
#                     # Auto-adjust column widths
#                     worksheet = writer.sheets[sheet_name]
#                     for idx, col in enumerate(table.columns):
#                         max_len = max(
#                             table[col].astype(str).str.len().max(),
#                             len(str(col))
#                         )
#                         worksheet.column_dimensions[chr(65 + idx)].width = min(max_len + 2, 50)
            
#             print(f"💾 SAVED: {output_path}")
#             print(f"   📊 Tables: {len(tables)}")
#             print(f"   📁 Format: {format_name}")
            
#         except Exception as e:
#             print(f"❌ Error saving file: {e}")
    
#     def process_folder(self, folder_path):
#         """Process folder of PDFs"""
#         folder_path = Path(folder_path)
        
#         if not folder_path.exists():
#             print(f"❌ Folder not found: {folder_path}")
#             return
        
#         pdf_files = list(folder_path.glob("*.pdf"))
        
#         if not pdf_files:
#             print(f"❌ No PDF files found in: {folder_path}")
#             return
        
#         print(f"📁 Processing {len(pdf_files)} PDFs from: {folder_path}")
#         print("=" * 60)
        
#         successful_files = 0
#         for pdf_file in pdf_files:
#             try:
#                 self.process_pdf(str(pdf_file))
#                 successful_files += 1
#             except Exception as e:
#                 print(f"❌ Failed to process {pdf_file}: {e}")
        
#         print(f"\n🎉 OVERALL SUMMARY:")
#         print(f"   ✅ Successfully processed: {successful_files}/{len(pdf_files)} files")
#         self.list_learned_formats()
    
#     def list_learned_formats(self):
#         """Show learned formats with enhanced details"""
#         formats = self.format_manager.formats
        
#         if not formats:
#             print("📋 No formats learned yet")
#             return
        
#         print(f"\n📋 LEARNED FORMATS ({len(formats)}):")
#         print("=" * 60)
        
#         for i, (format_name, format_data) in enumerate(formats.items(), 1):
#             print(f"{i}. {format_name}")
#             print(f"   🔑 Signature: {format_data['signature'][:16]}...")
#             print(f"   📊 Columns: {', '.join(format_data['columns'])}")
#             print(f"   📐 Shape: {format_data['sample_data_shape']}")
#             print(f"   📁 Folder: {format_data['output_folder']}")
#             print(f"   📅 Created: {format_data['created_date'][:10]}")
#             print()

# # --------------------------
# # ▶️ USAGE
# # --------------------------
# if __name__ == "__main__":
#     processor = CleanPDFProcessor()
    
#     # Process folder
#     processor.process_folder(r"C:\Users\abcom\Desktop\statemetns\pdf3")
    
#     # Show final summary
#     print("\n" + "=" * 60)
#     print("🏁 EXTRACTION COMPLETED")
#     print("=" * 60)















import os
import json
import pdfplumber
import camelot
import pandas as pd
import re
from pathlib import Path
from datetime import datetime
import hashlib
import numpy as np
from difflib import SequenceMatcher

# --------------------------
# 📁 CONFIGURATION
# --------------------------
FORMAT_REGISTRY_PATH = "auto_formats13.json"
OUTPUT_BASE_DIR = "strctured_work3"

# --------------------------
# 🧠 TABLE-ONLY FORMAT MANAGER
# --------------------------
class TableOnlyFormatManager:
    def __init__(self):
        self.formats = self.load_formats()
        self.setup_directories()
    
    def load_formats(self):
        if os.path.exists(FORMAT_REGISTRY_PATH):
            with open(FORMAT_REGISTRY_PATH, 'r') as f:
                return json.load(f)
        return {}
    
    def save_formats(self):
        with open(FORMAT_REGISTRY_PATH, 'w') as f:
            json.dump(self.formats, f, indent=2)
    
    def setup_directories(self):
        os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    
    def create_format_signature(self, df):
        """Create signature ONLY from actual table column structure"""
        if df.empty or len(df.columns) < 2:
            return None
        
        # Use ONLY actual column names found in table structure
        original_columns = [str(col).strip() for col in df.columns]
        
        # Filter out empty and generated column names
        valid_columns = []
        for col in original_columns:
            clean_col = self.clean_column_name(col)
            # Only include columns that are actual table headers, not generated names
            if (clean_col and 
                not clean_col.startswith('column_') and 
                not clean_col.startswith('col_') and
                not clean_col.startswith('unnamed') and
                len(clean_col) > 1):
                valid_columns.append(clean_col)
        
        if len(valid_columns) < 2:
            return None
            
        # Create signature from valid table columns only
        signature_string = "|".join(sorted(valid_columns))
        return hashlib.md5(signature_string.encode()).hexdigest()
    
    def clean_column_name(self, column_text):
        """Clean column name - preserve actual table headers only"""
        if not isinstance(column_text, str):
            column_text = str(column_text)
        
        # Remove extra whitespace but preserve actual content
        cleaned = re.sub(r'[\n\r\t]', ' ', column_text)
        cleaned = ' '.join(cleaned.split())
        return cleaned.strip().lower()
    
    def find_matching_format(self, df):
        """Find matching format for table data only"""
        if not self.formats:
            return None
        
        current_signature = self.create_format_signature(df)
        if not current_signature:
            return None
        
        # Exact signature match for table structures
        for format_name, format_data in self.formats.items():
            if format_data.get('signature') == current_signature:
                return format_name
        
        return None
    
    def learn_new_format(self, df, source_pdf):
        """Learn new format ONLY for proper table structures"""
        format_signature = self.create_format_signature(df)
        
        if not format_signature:
            return None
        
        # Check for exact duplicates
        for existing_name, existing_data in self.formats.items():
            if existing_data.get('signature') == format_signature:
                return existing_name
        
        format_name = self.generate_table_format_name(df)
        
        # Store ONLY valid table columns
        actual_columns = []
        for col in df.columns:
            clean_col = self.clean_column_name(str(col))
            if (clean_col and 
                not clean_col.startswith('column_') and 
                not clean_col.startswith('col_') and
                not clean_col.startswith('unnamed') and
                len(clean_col) > 1):
                actual_columns.append(clean_col)
        
        if len(actual_columns) < 2:
            return None
        
        new_format = {
            'signature': format_signature,
            'columns': actual_columns,
            'column_count': len(actual_columns),
            'output_folder': os.path.join(OUTPUT_BASE_DIR, format_name),
            'created_date': datetime.now().isoformat(),
            'learned_from': os.path.basename(source_pdf),
            'sample_data_shape': f"{len(df)}x{len(df.columns)}"
        }
        
        os.makedirs(new_format['output_folder'], exist_ok=True)
        self.formats[format_name] = new_format
        self.save_formats()
        
        print(f"✅ LEARNED TABLE FORMAT: {format_name}")
        print(f"   Table Columns: {', '.join(actual_columns)}")
        
        return format_name
    
    def generate_table_format_name(self, df):
        """Generate format name based on actual table columns"""
        base_name = "TableFormat"
        
        # Get actual table columns (not generated ones)
        actual_columns = []
        for col in df.columns:
            clean_col = self.clean_column_name(str(col))
            if (clean_col and 
                not clean_col.startswith('column_') and 
                not clean_col.startswith('col_') and
                not clean_col.startswith('unnamed')):
                actual_columns.append(clean_col)
        
        column_count = len(actual_columns)
        
        if len(actual_columns) >= 2:
            # Use first 2 actual column names
            name_parts = []
            for col in actual_columns[:2]:
                # Clean for filename
                clean_col = re.sub(r'[^\w]', '_', col)
                clean_col = '_'.join(clean_col.split('_')[:2])  # Use first 2 parts
                if clean_col and len(clean_col) > 1:
                    name_parts.append(clean_col)
            
            if name_parts:
                name_candidate = f"{base_name}_{'_'.join(name_parts)}_{column_count}cols"
                return self.ensure_unique_name(name_candidate)
        
        return self.ensure_unique_name(f"{base_name}_{column_count}cols")
    
    def ensure_unique_name(self, name_candidate):
        """Ensure format name is unique"""
        counter = 1
        final_name = name_candidate
        while final_name in self.formats:
            final_name = f"{name_candidate}_{counter}"
            counter += 1
        return final_name

# --------------------------
# 📄 STRICT TABLE-ONLY EXTRACTOR
# --------------------------
class StrictTableOnlyExtractor:
    def __init__(self, format_manager):
        self.format_manager = format_manager
    
    def extract_tables_from_pdf(self, pdf_path):
        """Extract ONLY proper tables with column-wise data"""
        print("🔍 Extracting structured tables only (no headers/footers)...")
        
        # Primary extraction with strict table detection
        tables = self.extract_structured_tables_only(pdf_path)
        
        if not tables:
            print("❌ No proper structured tables found")
            return []
        
        # Filter only valid table structures
        valid_tables = [tbl for tbl in tables if self.is_proper_table_structure(tbl)]
        
        print(f"📊 Found {len(valid_tables)} proper structured tables")
        return valid_tables
    
    def extract_structured_tables_only(self, pdf_path):
        """Extract only properly structured tables"""
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Skip pages that are mostly text (headers/footers/descriptions)
                    if self.is_text_page(page):
                        print(f"📄 Page {page_num+1}: Skipping text-heavy page (likely header/footer)")
                        continue
                    
                    print(f"📄 Page {page_num+1}: Analyzing for structured tables...")
                    
                    # Extract tables with visual boundaries (most reliable for real tables)
                    visual_tables = self.extract_visual_tables(page, page_num)
                    tables.extend(visual_tables)
                    
        except Exception as e:
            print(f"❌ PDF extraction error: {e}")
        
        return tables
    
    def is_text_page(self, page):
        """Check if page is mostly text (header/footer/description) rather than table"""
        try:
            text = page.extract_text()
            if not text:
                return False
            
            # Count lines and words
            lines = text.split('\n')
            words = text.split()
            
            # Text-heavy pages have many lines but may not have table structure
            if len(lines) > 50 and len(words) > 200:
                return True
            
            # Check for common header/footer patterns
            header_footer_indicators = [
                'confidential', 'page', 'date:', 'copyright', 'all rights reserved',
                'proprietary', 'internal use', 'statement', 'report', 'summary'
            ]
            
            text_lower = text.lower()
            indicator_count = sum(1 for indicator in header_footer_indicators if indicator in text_lower)
            
            return indicator_count > 3
            
        except Exception:
            return False
    
    def extract_visual_tables(self, page, page_num):
        """Extract tables with visual boundaries only"""
        tables = []
        try:
            # Use line detection for structured tables only
            table_settings = {
                "vertical_strategy": "lines", 
                "horizontal_strategy": "lines",
                "snap_tolerance": 3,
                "join_tolerance": 3,
                "edge_min_length": 20,  # Require proper table lines
                "min_words_vertical": 2,  # Require multiple words for vertical
                "min_words_horizontal": 2,  # Require multiple words for horizontal
            }
            
            detected_tables = page.find_tables(table_settings)
            
            for table_num, table in enumerate(detected_tables):
                table_data = table.extract()
                
                if table_data and len(table_data) >= 3:  # Require at least header + 2 data rows
                    df = self.create_table_dataframe(table_data, page_num, table_num)
                    if df is not None and self.is_proper_table_structure(df):
                        tables.append(df)
                        print(f"   ✅ Table {table_num+1}: {len(df)}x{len(df.columns)} - Proper structure")
                        
        except Exception as e:
            print(f"   ⚠️ Table extraction error: {e}")
        
        return tables
    
    def create_table_dataframe(self, table_data, page_num, table_num):
        """Create dataframe ONLY for proper table structures"""
        try:
            if not table_data or len(table_data) < 3:
                return None
            
            # Find the actual header row (not first row if it's data)
            header_idx = self.find_actual_header_row(table_data)
            if header_idx is None:
                return None
            
            # Extract headers - only use if they are actual column headers
            headers = []
            valid_header_count = 0
            
            for cell in table_data[header_idx]:
                header_text = self.clean_table_text(str(cell)) if cell is not None else ""
                
                # Validate if this looks like an actual column header
                if self.is_actual_column_header(header_text):
                    headers.append(header_text)
                    valid_header_count += 1
                else:
                    # If not a valid header, we can't use this table structure
                    return None
            
            # Need at least 2 valid column headers
            if valid_header_count < 2:
                return None
            
            # Extract data rows
            data_rows = []
            for i in range(len(table_data)):
                if i != header_idx:  # Skip header row
                    row_data = []
                    for cell in table_data[i]:
                        cell_text = self.clean_table_text(str(cell)) if cell is not None else ""
                        row_data.append(cell_text)
                    
                    # Only add rows with actual data
                    if any(cell.strip() for cell in row_data if cell):
                        data_rows.append(row_data)
            
            if len(data_rows) < 2:  # Need at least 2 data rows
                return None
            
            # Ensure proper column alignment
            max_cols = len(headers)
            aligned_rows = []
            
            for row in data_rows:
                aligned_row = row[:max_cols]  # Take first max_cols elements
                if len(aligned_row) < max_cols:
                    aligned_row.extend([''] * (max_cols - len(aligned_row)))
                aligned_rows.append(aligned_row)
            
            # Create dataframe with actual headers
            df = pd.DataFrame(aligned_rows, columns=headers)
            
            # Remove completely empty columns
            non_empty_columns = []
            for col in df.columns:
                if df[col].astype(str).str.strip().ne('').any():
                    non_empty_columns.append(col)
            
            if len(non_empty_columns) >= 2:
                df = df[non_empty_columns]
                return df
            
        except Exception as e:
            print(f"⚠️ Error creating table dataframe: {e}")
        
        return None
    
    def find_actual_header_row(self, table_data):
        """Find the row that contains actual column headers"""
        if not table_data:
            return None
        
        best_score = 0
        best_idx = 0
        
        # Check first 3 rows for header characteristics
        for idx in range(min(3, len(table_data))):
            row = table_data[idx]
            score = self.calculate_header_confidence(row)
            if score > best_score:
                best_score = score
                best_idx = idx
        
        # Only return if we have high confidence it's a header
        return best_idx if best_score >= 0.7 else None
    
    def calculate_header_confidence(self, row):
        """Calculate confidence that a row contains column headers"""
        if not row:
            return 0
        
        header_like_cells = 0
        total_cells = 0
        
        for cell in row:
            if cell is None:
                continue
                
            cell_str = str(cell).strip()
            if not cell_str:
                continue
                
            total_cells += 1
            
            # Characteristics of actual column headers vs data
            is_header_like = (
                len(cell_str) <= 30 and                    # Not too long
                len(cell_str) >= 2 and                     # Not too short
                cell_str.count(' ') <= 4 and               # Reasonable word count
                not cell_str.replace('.', '').replace(',', '').replace('$', '').isdigit() and # Not numeric
                not re.match(r'^\d+[/-]\d+[/-]\d+$', cell_str) and  # Not date
                not re.match(r'^[+-]?\$?[\d,]+\.?\d*$', cell_str) and  # Not amount
                not cell_str.isupper() or len(cell_str) <= 4  # All caps ok for short text
            )
            
            if is_header_like:
                header_like_cells += 1
        
        return header_like_cells / total_cells if total_cells > 0 else 0
    
    def is_actual_column_header(self, text):
        """Check if text is an actual column header (not data)"""
        if not text or len(text.strip()) < 2:
            return False
        
        text = text.strip()
        
        # Definitely NOT headers
        if (text.isdigit() or
            re.match(r'^\d+[/-]\d+[/-]\d+$', text) or
            re.match(r'^[+-]?\$?[\d,]+\.?\d*$', text) or
            len(text) > 50):
            return False
        
        # Likely headers
        if (2 <= len(text) <= 30 and
            text.count(' ') <= 5 and
            not text.replace('.', '').replace(',', '').replace('$', '').isdigit()):
            return True
        
        return False
    
    def is_proper_table_structure(self, df):
        """Validate that this is a proper table structure"""
        if df.empty or len(df.columns) < 2 or len(df) < 2:
            return False
        
        # Check for actual column headers (not generated names)
        actual_headers = 0
        for col in df.columns:
            col_str = str(col).strip()
            if (col_str and 
                len(col_str) >= 2 and 
                not col_str.startswith('column_') and
                not col_str.startswith('col_') and
                not col_str.startswith('unnamed') and
                self.is_actual_column_header(col_str)):
                actual_headers += 1
        
        # Need at least 2 actual column headers
        if actual_headers < 2:
            return False
        
        # Check for data content (not just headers)
        data_cells = 0
        total_cells = df.size
        
        for col in df.columns:
            non_empty = df[col].astype(str).str.strip().ne('').sum()
            data_cells += non_empty
        
        # Should have reasonable data content
        return data_cells >= len(df.columns) * 2  # At least 2 cells per column
    
    def clean_table_text(self, text):
        """Clean text for table cells only"""
        if not isinstance(text, str):
            text = str(text)
        
        # Basic cleaning - preserve actual content
        cleaned = re.sub(r'[\n\r\t]', ' ', text)
        cleaned = ' '.join(cleaned.split())
        return cleaned.strip()

# --------------------------
# 🚀 TABLE-ONLY PDF PROCESSOR
# --------------------------
class TableOnlyPDFProcessor:
    def __init__(self):
        self.format_manager = TableOnlyFormatManager()
        self.extractor = StrictTableOnlyExtractor(self.format_manager)
    
    def process_pdf(self, pdf_path):
        """Process PDF to extract ONLY proper tables"""
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return
        
        print(f"\n🎯 PROCESSING: {os.path.basename(pdf_path)}")
        print("=" * 60)
        
        # Extract ONLY proper tables
        tables = self.extractor.extract_tables_from_pdf(pdf_path)
        
        if not tables:
            print("❌ No proper table structures found")
            return
        
        format_tables = {}
        success_count = 0
        
        for i, table in enumerate(tables):
            print(f"\n📋 Table {i+1}:")
            print(f"   Size: {len(table)} rows x {len(table.columns)} columns")
            print(f"   Headers: {list(table.columns)}")
            
            # Find or learn format
            format_name = self.format_manager.find_matching_format(table)
            
            if format_name:
                print(f"   ✅ Matched table format: {format_name}")
            else:
                format_name = self.format_manager.learn_new_format(table, pdf_path)
                if format_name:
                    print(f"   🆕 Learned new table format: {format_name}")
            
            if format_name:
                if format_name not in format_tables:
                    format_tables[format_name] = []
                format_tables[format_name].append(table)
                success_count += 1
        
        # Save results
        for format_name, tables_list in format_tables.items():
            self.save_table_data(tables_list, format_name, pdf_path)
        
        print(f"\n✅ COMPLETED: {success_count} proper tables processed")
    
    def save_table_data(self, tables, format_name, source_pdf):
        """Save table data with original structure"""
        format_data = self.format_manager.formats[format_name]
        output_folder = format_data['output_folder']
        
        source_name = Path(source_pdf).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{format_name}_{source_name}_{timestamp}.xlsx"
        output_path = os.path.join(output_folder, filename)
        
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for i, table in enumerate(tables):
                    sheet_name = f"Table_{i+1}"[:31]
                    
                    # Save exact table structure
                    table.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"💾 SAVED: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
    
    def process_folder(self, folder_path):
        """Process folder of PDFs"""
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print(f"❌ Folder not found: {folder_path}")
            return
        
        pdf_files = list(folder_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"❌ No PDF files found in: {folder_path}")
            return
        
        print(f"📁 Processing {len(pdf_files)} PDFs for table extraction...")
        success_count = 0
        
        for pdf_file in pdf_files:
            try:
                self.process_pdf(str(pdf_file))
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to process {pdf_file.name}: {e}")
        
        print(f"\n🎉 OVERALL: {success_count}/{len(pdf_files)} files processed")
        self.list_table_formats()
    
    def list_table_formats(self):
        """List all learned table formats"""
        formats = self.format_manager.formats
        
        if not formats:
            print("📋 No table formats learned yet")
            return
        
        print(f"\n📋 LEARNED TABLE FORMATS ({len(formats)}):")
        print("=" * 50)
        
        for name, data in formats.items():
            print(f"• {name}")
            print(f"  Columns: {data['column_count']}")
            print(f"  Structure: {data['sample_data_shape']}")
            print(f"  Source: {data['learned_from']}")
            print()

# --------------------------
# ▶️ USAGE
# --------------------------
if __name__ == "__main__":
    processor = TableOnlyPDFProcessor()
    processor.process_folder(r"C:\Users\abcom\Desktop\statemetns\pdf3")