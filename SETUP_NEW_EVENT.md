# Setting Up for a New Event

## Resetting the Database

To start fresh for a new event, you can reset the SQLite database:

```bash
python reset_database.py
```

This will:
- Delete all existing RSVP entries
- Recreate the database with a fresh schema
- Confirm before deleting to prevent accidental data loss

**Note:** Make sure to export any data you want to keep before resetting!

## Connecting to a New Google Sheet

To connect to a different Google Sheet for a new event:

1. **Create a new Google Sheet** (or use an existing one)
2. **Share the sheet with your service account email** (found in your Google credentials JSON)
3. **Set the environment variable** `GOOGLE_SHEET_NAME` to the name of your new sheet:
   ```bash
   export GOOGLE_SHEET_NAME="Your-New-Sheet-Name"
   ```
   
   Or add it to your `.env` file:
   ```
   GOOGLE_SHEET_NAME=Your-New-Sheet-Name
   ```

4. **Restart your server** for the changes to take effect

If `GOOGLE_SHEET_NAME` is not set, it will default to `"Yavneh-Arts-RSVP"`.

