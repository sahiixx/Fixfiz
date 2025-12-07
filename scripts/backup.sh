#!/bin/bash
# ================================================================================================
# NOWHERE.AI Platform - Database Backup Script
# ================================================================================================
# Automated backup of MongoDB database with rotation

set -e  # Exit on error

# Configuration
BACKUP_DIR="/app/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="nowhereai_backup_${DATE}"
RETENTION_DAYS=7  # Keep backups for 7 days
DATABASE_NAME="nowhereai"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================================================================================${NC}"
echo -e "${GREEN}NOWHERE.AI Database Backup${NC}"
echo -e "${GREEN}================================================================================================${NC}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo -e "${RED}ERROR: MongoDB is not running${NC}"
    exit 1
fi

echo -e "${YELLOW}Starting backup...${NC}"
echo "Database: $DATABASE_NAME"
echo "Backup location: $BACKUP_DIR/$BACKUP_NAME"
echo "Timestamp: $(date)"
echo ""

# Perform backup
mongodump \
    --db "$DATABASE_NAME" \
    --out "$BACKUP_DIR/$BACKUP_NAME" \
    --quiet

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backup completed successfully${NC}"
    
    # Compress backup
    echo -e "${YELLOW}Compressing backup...${NC}"
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" -C "$BACKUP_DIR" "$BACKUP_NAME"
    
    # Remove uncompressed backup
    rm -rf "$BACKUP_DIR/$BACKUP_NAME"
    
    # Get backup size
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | cut -f1)
    echo -e "${GREEN}Compressed backup size: $BACKUP_SIZE${NC}"
    
    # Remove old backups
    echo -e "${YELLOW}Cleaning up old backups (older than $RETENTION_DAYS days)...${NC}"
    find "$BACKUP_DIR" -name "nowhereai_backup_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete
    
    # List current backups
    echo ""
    echo -e "${GREEN}Current backups:${NC}"
    ls -lh "$BACKUP_DIR"/nowhereai_backup_*.tar.gz 2>/dev/null || echo "No backups found"
    
    echo ""
    echo -e "${GREEN}================================================================================================${NC}"
    echo -e "${GREEN}Backup completed successfully at $(date)${NC}"
    echo -e "${GREEN}================================================================================================${NC}"
else
    echo -e "${RED}❌ Backup failed${NC}"
    exit 1
fi
