/**
 * ==============================================================================
 * REAL-TIME GOOGLE SHEETS LIVE INVENTORY CONNECTOR FOR 3D ARCHITECTURAL MODEL
 * ==============================================================================
 * 
 * INSTRUCTIONS FOR DEPLOYING THIS SCRIPT:
 * ------------------------------------------------------------------------------
 * 1. Open your Google Sheet in your web browser.
 * 2. In the top menu, click: Extensions > Apps Script
 * 3. Delete any code in the editor, and PASTE THIS ENTIRE SCRIPT.
 * 4. Click the "Save project" icon (floppy disk).
 * 5. Click the blue "Deploy" button (top right) > "New deployment".
 * 6. Under "Select type" (gear icon), choose "Web app".
 * 7. Configuration settings:
 *    - Description: "Live 3D Inventory API"
 *    - Execute as: "Me (your_email@gmail.com)"   <-- CRITICAL!
 *    - Who has access: "Anyone"                  <-- CRITICAL!
 * 8. Click "Deploy".
 * 9. Copy the "Web app URL" (it ends with /exec).
 * 
 * ------------------------------------------------------------------------------
 * IMPORTANT: WHEN YOU EDIT THIS CODE IN THE FUTURE:
 * To make changes live, click:
 *   Deploy > Manage deployments > Click Edit (pencil icon) > 
 *   Version: Select "New version" > Click Deploy.
 * ------------------------------------------------------------------------------
 */

function doGet(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // 1. Try finding an explicit sheet named 'Inventory', 'Flats', 'Units', or use the active sheet
    var sheet = ss.getSheetByName('Inventory') || 
                ss.getSheetByName('Flats') || 
                ss.getSheetByName('Inventory Status') || 
                ss.getActiveSheet();
                
    var range = sheet.getDataRange();
    var values = range.getValues();

    if (!values || values.length < 2) {
      return jsonResponse({
        error: "Spreadsheet is empty or has no data rows.",
        count: 0,
        data: []
      });
    }

    var inventory = [];

    // Check if the sheet is in LIST FORMAT (Floor | Position | Status)
    // or GRID FORMAT (Floors as rows 1-14, Positions 1-26 as columns)
    var headerRow = values[0];
    var isGridFormat = false;

    // Check header row for numbers 1..26 or 'Flat 1'..'Flat 26'
    var numericColCount = 0;
    for (var c = 1; c < headerRow.length; c++) {
      var headerVal = String(headerRow[c]).trim();
      if (!isNaN(parseInt(headerVal, 10)) || headerVal.toLowerCase().indexOf('flat') !== -1 || headerVal.toLowerCase().indexOf('pos') !== -1) {
        numericColCount++;
      }
    }
    if (numericColCount >= 10) {
      isGridFormat = true;
    }

    if (isGridFormat) {
      // -------------------------------------------------------------
      // FORMAT A: GRID MATRIX (Row = Floor, Column = Apartment Pos)
      // -------------------------------------------------------------
      for (var r = 1; r < values.length; r++) {
        var row = values[r];
        var floorNum = parseInt(row[0], 10);
        if (isNaN(floorNum) || floorNum < 1 || floorNum > 14) continue;

        for (var col = 1; col < row.length; col++) {
          var colHeader = String(headerRow[col]).trim();
          var match = colHeader.match(/\d+/);
          var posNum = match ? parseInt(match[0], 10) : col;
          if (posNum < 1 || posNum > 26) continue;

          var cellStatus = String(row[col] || '').trim();
          inventory.push({
            floor: floorNum,
            position: posNum,
            status: cellStatus || 'Available'
          });
        }
      }
    } else {
      // -------------------------------------------------------------
      // FORMAT B: LIST FORMAT (Each row is one apartment)
      // Headers: Floor | Position (or Flat) | Status
      // -------------------------------------------------------------
      var colFloor = -1;
      var colPos = -1;
      var colStatus = -1;

      for (var h = 0; h < headerRow.length; h++) {
        var name = String(headerRow[h]).trim().toLowerCase();
        if (name.indexOf('floor') !== -1 && colFloor === -1) colFloor = h;
        else if ((name.indexOf('position') !== -1 || name.indexOf('pos') !== -1 || name.indexOf('flat') !== -1 || name.indexOf('unit') !== -1) && colPos === -1) colPos = h;
        else if ((name.indexOf('status') !== -1 || name.indexOf('state') !== -1 || name.indexOf('book') !== -1) && colStatus === -1) colStatus = h;
      }

      // Sensible column fallbacks: Col A = Floor, Col B = Position, Col C = Status
      if (colFloor === -1) colFloor = 0;
      if (colPos === -1) colPos = 1;
      if (colStatus === -1) colStatus = 2;

      for (var r = 1; r < values.length; r++) {
        var row = values[r];
        var floorVal = parseInt(row[colFloor], 10);
        var posVal = parseInt(row[colPos], 10);
        var statusVal = String(row[colStatus] || '').trim();

        if (!isNaN(floorVal) && !isNaN(posVal) && floorVal >= 1 && floorVal <= 14 && posVal >= 1 && posVal <= 26) {
          inventory.push({
            floor: floorVal,
            position: posVal,
            status: statusVal || 'Available'
          });
        }
      }
    }

    // Return the inventory array directly for 100% compatibility
    return jsonResponse(inventory);

  } catch (error) {
    return jsonResponse({
      error: error.toString(),
      data: []
    });
  }
}

function jsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
