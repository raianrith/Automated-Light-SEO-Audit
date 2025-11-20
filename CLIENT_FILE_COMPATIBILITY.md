# Client File Compatibility Guide

## Overview

The app has been enhanced to handle files from different clients consistently, as long as the column structure matches the expected format. The app now uses **flexible column detection** that automatically identifies required columns regardless of minor naming variations.

## Key Features

### ✅ Automatic Column Detection

The app automatically detects columns using flexible pattern matching:
- **Keyword columns**: Detects "Keyword", "Keywords", "Query", "Queries" (case-insensitive)
- **Position columns**: Detects "Position", "Pos", "Rank", "Ranking" (case-insensitive)
- **Handles variations**: Works with spaces, underscores, hyphens, and different cases

### 📋 Column Preview Feature

When you upload files, the app shows a **Column Detection Preview** that displays:
- All detected columns in the file
- Sample values from each column
- Confirmation of key columns (Keyword, Position) detection

This helps you verify that the app correctly identified the required columns before running the analysis.

### 🔄 Consistent Processing

All files are normalized to a standard format:
- Column names converted to lowercase
- Spaces and hyphens replaced with underscores
- This ensures consistent processing across different client file formats

## Supported File Types

- **Semrush Positions**: CSV or Excel (.xlsx, .xls)
- **Semrush Position Changes**: CSV or Excel
- **Semrush Pages**: CSV or Excel
- **Semrush Competitors**: CSV or Excel
- **Google Search Console Queries**: Excel (with Compare format)
- **Google Search Console Pages**: Excel (with Pages and Countries sheets)

## Column Requirements

### Keyword Visibility Analysis
- **Required**: Keyword/Query column, Position/Rank column
- **Optional**: Any additional columns are preserved but not used

### Keyword Movement Analysis
- **Required**: Keyword column, Position column, Previous Position column
- **Optional**: Movement, Change columns (will be calculated if missing)

### Page Performance Analysis
- **Required**: URL/Page column, Traffic column
- **Optional**: Keywords column, Position column

### Query Analysis (GSC)
- **Required**: Query column, Clicks (current and previous), Impressions (current and previous)
- **Optional**: CTR, Position columns

## Troubleshooting

### If Column Detection Fails

1. **Check the Column Preview**: Expand the "Column Detection Preview" section to see what columns were found
2. **Verify File Format**: Ensure you're using the correct export format from Semrush/GSC
3. **Check Column Names**: The app looks for common variations, but if your columns have unusual names, you may need to rename them

### Common Issues

**Issue**: "Missing required columns" error
- **Solution**: Check the Column Preview to see available columns. The error message will show the first 15 columns found.

**Issue**: "No valid position data found"
- **Solution**: Ensure the Position column contains numeric values (1, 2, 3, etc.) not text like "Top 3" or "Not ranked"

## Best Practices

1. **Use Standard Exports**: Export files directly from Semrush/GSC using their standard export formats
2. **Don't Modify Headers**: Keep the original column headers from the export
3. **Check Preview**: Always review the Column Detection Preview before running analysis
4. **Consistent Dates**: Use the same date ranges for comparison files (e.g., current month vs. same month last year)

## Technical Details

The app uses the following normalization process:
1. Files are read and columns are normalized to lowercase with underscores
2. `find_column()` function searches for column patterns (case-insensitive, handles variations)
3. Analysis functions use detected column names dynamically
4. All processing is consistent regardless of original column name formatting

This ensures that files from different clients with the same structure will work identically.

