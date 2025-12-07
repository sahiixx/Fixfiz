#!/bin/bash
# ================================================================================================
# NOWHERE.AI Platform - Database Restore Script
# ================================================================================================
# Restore MongoDB database from backup

set -e  # Exit on error

# Configuration
BACKUP_DIR="/app/backups"
DATABASE_NAME="nowhereai"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================================================================================${NC}"
echo -e "${GREEN}NOWHERE.AI Database Restore${NC}"
echo -e "${GREEN}================================================================================================${NC}"

# Check if backup file is provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}Available backups:${NC}"
    ls -lh "$BACKUP_DIR"/nowhereai_backup_*.tar.gz 2>/dev/null || echo "No backups found"
    echo ""
    echo -e "${RED}Usage: $0 <backup_file>${NC}"
    echo "Example: $0 $BACKUP_DIR/nowhereai_backup_20241207_120000.tar.gz"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}ERROR: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo -e "${RED}ERROR: MongoDB is not running${NC}"
    exit 1
fi

echo -e "${YELLOW}⚠️  WARNING: This will replace the current database!${NC}"
echo "Database: $DATABASE_NAME"
echo "Backup file: $BACKUP_FILE"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Restore cancelled${NC}"
    exit 0
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo -e "${YELLOW}Extracting backup...${NC}"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# Find the backup directory
BACKUP_FOLDER=$(find "$TEMP_DIR" -type d -name "nowhereai_backup_*" | head -n 1)

if [ -z "$BACKUP_FOLDER" ]; then
    echo -e "${RED}ERROR: Could not find backup data in archive${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${YELLOW}Restoring database...${NC}"

# Drop existing database
echo -e "${YELLOW}Dropping existing database...${NC}"
mongosh "$DATABASE_NAME" --eval "db.dropDatabase()" --quiet

# Restore from backup
mongorestore \
    --db "$DATABASE_NAME" \
    "$BACKUP_FOLDER/$DATABASE_NAME" \
    --quiet

# Check if restore was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database restored successfully${NC}"
    
    # Cleanup
    rm -rf "$TEMP_DIR"
    
    # Verify restoration
    COLLECTION_COUNT=$(mongosh "$DATABASE_NAME" --eval "db.getCollectionNames().length" --quiet)
    echo -e "${GREEN}Collections restored: $COLLECTION_COUNT${NC}"
    
    echo ""
    echo -e "${GREEN}================================================================================================${NC}"
    echo -e "${GREEN}Restore completed successfully at $(date)${NC}"
    echo -e "${GREEN}================================================================================================${NC}"
else
    echo -e "${RED}❌ Restore failed${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi
