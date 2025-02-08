package com.selenium.utilities;

import java.io.FileInputStream;
import org.apache.poi.ss.usermodel.*;

public class ReadDataUtil {
    public static String getCellData(String filePath, int sheetIndex, int row, int col) {
        try {
            FileInputStream fis = new FileInputStream(filePath);
            Workbook workbook = WorkbookFactory.create(fis);
            Sheet sheet = workbook.getSheetAt(sheetIndex);
            String data = sheet.getRow(row).getCell(col).getStringCellValue();
            workbook.close();
            return data;
        } catch (Exception e) {
            e.printStackTrace();
            return "";
        }
    }
}
