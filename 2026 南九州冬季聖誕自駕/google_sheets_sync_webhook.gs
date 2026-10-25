/**
 * 2026 南九州旅行手帳 - Google 試算表自動記帳 Webhook (全自動直接寫入版)
 * 試算表：https://docs.google.com/spreadsheets/d/1P4niaKfXpHnrlVkiexFmxa2Q0U7kwOvj6yUINn--WNo
 * 
 * 【功能說明】：
 * - 支援儀表板網頁或手機「一鍵儲存 ➔ 直接寫入試算表」，全程 0 手動複製貼上！
 * - 自動鎖定【費用】工作表中的空白列 (從第 24 列開始自動填入)。
 * - 自動寫入日期、項目、類別、代墊人、雙幣金額與 4 人勾選分攤。
 * - 自動連動試算表公式與上方結算看板！
 */

function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("費用") || ss.getActiveSheet();
    
    var data = JSON.parse(e.postData.contents);
    
    var date = data.date || Utilities.formatDate(new Date(), "GMT+9", "yyyy-MM-dd");
    var item = data.item || "";
    var category = data.category || "其他雜支";
    var payer = data.payer || "阿純";
    var currency = data.currency || "JPY";
    var amountOriginal = Number(data.amount_original || 0);
    
    // 分攤成員布林值
    var achun = (data.achun !== undefined) ? !!data.achun : true;
    var alu = (data.alu !== undefined) ? !!data.alu : true;
    var aunt = (data.aunt !== undefined) ? !!data.aunt : true;
    var uncle = (data.uncle !== undefined) ? !!data.uncle : true;
    var note = data.note || "";

    // 尋找第 18 列以後第一個「消費項目 (Column C, 第3欄)」為空的列
    var targetRow = -1;
    for (var r = 18; r <= 41; r++) {
      var val = sheet.getRange(r, 3).getValue();
      if (!val || val.toString().trim() === "") {
        targetRow = r;
        break;
      }
    }
    
    // 若 18~41 列已滿，則在合計列 (原第 42 列) 上方插入新列
    if (targetRow === -1) {
      targetRow = 42;
      sheet.insertRowBefore(42);
    }

    // 寫入欄位至對應欄位 (Column B 至 O)
    // B: 日期, C: 項目, D: 類別, E: 付款人, F: 幣別, G: 原幣金額
    sheet.getRange(targetRow, 2).setValue(date);
    sheet.getRange(targetRow, 3).setValue(item);
    sheet.getRange(targetRow, 4).setValue(category);
    sheet.getRange(targetRow, 5).setValue(payer);
    sheet.getRange(targetRow, 6).setValue(currency);
    sheet.getRange(targetRow, 7).setValue(amountOriginal);
    
    // H: 折合台幣公式
    sheet.getRange(targetRow, 8).setFormula('=IF(F' + targetRow + '="JPY", ROUND(G' + targetRow + '*$K$2, 0), IF(F' + targetRow + '="TWD", G' + targetRow + ', 0))');
    
    // I, J, K, L: 4人分攤 (TRUE / FALSE)
    sheet.getRange(targetRow, 9).setValue(achun);
    sheet.getRange(targetRow, 10).setValue(alu);
    sheet.getRange(targetRow, 11).setValue(aunt);
    sheet.getRange(targetRow, 12).setValue(uncle);
    
    // M: 分攤人數公式, N: 每人應付公式, O: 備註
    sheet.getRange(targetRow, 13).setFormula('=COUNTIF(I' + targetRow + ':L' + targetRow + ', TRUE)');
    sheet.getRange(targetRow, 14).setFormula('=IF(M' + targetRow + '>0, H' + targetRow + '/M' + targetRow + ', 0)');
    sheet.getRange(targetRow, 15).setValue(note);

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: "成功直接寫入 Google 試算表第 " + targetRow + " 列！",
      targetRow: targetRow,
      item: item,
      payer: payer
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("2026 南九州旅行記帳 Webhook 直寫連線正常！❄️").setMimeType(ContentService.MimeType.TEXT);
}
