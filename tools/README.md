# Video Management Tools

Utility scripts for managing video content, timestamps, and course data migration in the AI Academy platform.

## 📖 What it does
Provides essential tools for maintaining video content integrity, fixing timestamp issues, migrating video paths, and auditing course data. These scripts ensure the learning platform runs smoothly with accurate content.

## 🛠️ Built with
- **Python 3.8+**: Core scripting language
- **JSON Processing**: Course data manipulation
- **File System Operations**: Path management and validation
- **Data Analysis**: Pandas for timestamp analysis
- **Automation**: Batch processing capabilities

## 🚀 Status
**In Production** - Actively used for platform maintenance and content updates. All scripts are tested and production-ready.

## 🌐 Demo
- **Run Audit**: `python audit_timestamps.py` - Check all timestamps
- **Fix Issues**: `python fix_timestamps.py` - Automatically repair timestamp problems
- **Migrate Paths**: `python migrate_to_video_paths.py` - Update video file references

## 🔧 Available Tools

### Timestamp Management
- **`audit_timestamps.py`** - Comprehensive timestamp validation across all lessons
- **`audit_timestamps_enhanced.py`** - Advanced timestamp analysis with detailed reporting  
- **`fix_timestamps.py`** - Automated timestamp correction and validation
- **`fix_timestamps_enhanced.py`** - Enhanced timestamp fixing with backup creation
- **`apply_week6_timestamps.py`** - Specific tool for Week 6 timestamp application

### Video Path Management  
- **`fix_video_paths.py`** - Repair broken video file references
- **`migrate_to_video_paths.py`** - Migrate legacy paths to new structure

## 🚀 Quick Start

### Prerequisites
```bash
# Install dependencies
pip install pandas json pathlib
```

### Basic Usage
```bash
# Navigate to tools directory
cd tools

# Audit all timestamps
python audit_timestamps.py

# Fix any issues found
python fix_timestamps.py

# Verify video paths
python fix_video_paths.py
```

### Advanced Operations
```bash
# Enhanced timestamp audit with detailed reporting
python audit_timestamps_enhanced.py

# Apply specific week timestamps
python apply_week6_timestamps.py

# Migrate to new video path structure
python migrate_to_video_paths.py
```

## 📊 Tool Details

### Audit Tools
- **Purpose**: Validate content integrity and identify issues
- **Output**: Detailed reports on timestamp accuracy and video accessibility
- **Frequency**: Run before major deployments or content updates

### Fix Tools  
- **Purpose**: Automatically resolve common content issues
- **Safety**: Creates backups before making changes
- **Validation**: Verifies fixes after application

### Migration Tools
- **Purpose**: Update content structure for platform improvements
- **Compatibility**: Maintains backward compatibility where possible
- **Testing**: Includes dry-run modes for safe testing

## 🔒 Safety Features

- **Backup Creation**: All tools create backups before making changes
- **Validation**: Post-operation verification ensures data integrity
- **Dry Run Mode**: Test operations without making actual changes
- **Error Handling**: Robust error handling with detailed logging

## 📁 Integration

These tools integrate seamlessly with:
- **Main Platform**: AI Academy React application
- **Course Data**: JSON-based course content structure
- **Video Storage**: Supabase storage integration
- **CI/CD**: Can be automated as part of deployment pipeline

## 🤝 Contributing

When adding new tools:
1. Follow the existing naming convention
2. Include comprehensive error handling
3. Add backup/safety mechanisms
4. Document all parameters and outputs
5. Test with sample data before production use

## 📞 Support

- **Issues**: Report via main repository issues
- **Documentation**: Each tool includes inline documentation
- **Testing**: Use provided sample data for testing
