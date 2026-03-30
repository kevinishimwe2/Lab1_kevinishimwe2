#!/bin/bash

# =============================================================================
# organizer.sh
# Archives the current grades.csv by timestamping it and moving it to an
# archive/ folder, then creates a fresh empty grades.csv ready for next use.
# Every archival action is recorded in organizer.log.
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------
CSV_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# ---------------------------------------------------------------------------
# 2. Check that grades.csv actually exists before we try to archive it
# ---------------------------------------------------------------------------
if [ ! -f "$CSV_FILE" ]; then
    echo "Error: '$CSV_FILE' not found in the current directory."
    echo "Nothing to archive. Exiting."
    exit 1
fi

# ---------------------------------------------------------------------------
# 3. Archive directory — create it if it does not already exist
# ---------------------------------------------------------------------------
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR/"
else
    echo "Archive directory already exists: $ARCHIVE_DIR/"
fi

# ---------------------------------------------------------------------------
# 4. Generate a timestamp string in the format YYYYMMDD-HHMMSS
# ---------------------------------------------------------------------------
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# ---------------------------------------------------------------------------
# 5. Build the new archived filename, e.g. grades_20251105-170000.csv
# ---------------------------------------------------------------------------
BASENAME="${CSV_FILE%.csv}"                          # strips the .csv extension
ARCHIVED_NAME="${BASENAME}_${TIMESTAMP}.csv"         # e.g. grades_20251105-170000.csv
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"      # full destination path

# ---------------------------------------------------------------------------
# 6. Move (rename + relocate) grades.csv into the archive directory
# ---------------------------------------------------------------------------
mv "$CSV_FILE" "$ARCHIVED_PATH"
echo "Archived: '$CSV_FILE' → '$ARCHIVED_PATH'"

# ---------------------------------------------------------------------------
# 7. Workspace reset — create a new empty grades.csv so the environment is
#    immediately ready for the next batch of grades
# ---------------------------------------------------------------------------
touch "$CSV_FILE"
echo "Reset: New empty '$CSV_FILE' created in current directory."

# ---------------------------------------------------------------------------
# 8. Logging — append one line per run to organizer.log
#    Format: [TIMESTAMP] | original: grades.csv | archived: archive/grades_TIMESTAMP.csv
# ---------------------------------------------------------------------------
LOG_ENTRY="[${TIMESTAMP}] | original: ${CSV_FILE} | archived: ${ARCHIVED_PATH}"
echo "$LOG_ENTRY" >> "$LOG_FILE"
echo "Logged: Entry written to '$LOG_FILE'."

# ---------------------------------------------------------------------------
# 9. Done
# ---------------------------------------------------------------------------
echo ""
echo "✔ Archival complete."
echo "  Timestamp : $TIMESTAMP"
echo "  Archived  : $ARCHIVED_PATH"
echo "  Log file  : $LOG_FILE"