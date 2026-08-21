#!/usr/bin/env python3
"""Create a small, valid OOXML workbook for manual test-case acceptance."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def column_name(number: int) -> str:
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def xml_text(value: object) -> str:
    return escape(str(value), quote=False)


def normalize_steps(value: object) -> str:
    if isinstance(value, list):
        return "\n".join(f"{index}. {item}" for index, item in enumerate(value, 1))
    return str(value or "")


def cell(row: int, column: int, value: object, style: int = 0) -> str:
    reference = f"{column_name(column)}{row}"
    return (
        f'<c r="{reference}" s="{style}" t="inlineStr">'
        f'<is><t xml:space="preserve">{xml_text(value)}</t></is></c>'
    )


def worksheet(rows: list[list[object]], widths: list[int], validation_column: str | None) -> str:
    row_xml = []
    for row_number, row in enumerate(rows, 1):
        style = 1 if row_number == 1 else 0
        cells = "".join(cell(row_number, index, value, style) for index, value in enumerate(row, 1))
        row_xml.append(f'<row r="{row_number}">{cells}</row>')

    max_column = column_name(max(len(row) for row in rows))
    max_row = len(rows)
    columns = "".join(
        f'<col min="{index}" max="{index}" width="{width}" customWidth="1"/>'
        for index, width in enumerate(widths, 1)
    )
    validation = ""
    if validation_column:
        validation = (
            f'<dataValidations count="1"><dataValidation type="list" allowBlank="1" '
            f'showErrorMessage="1" sqref="{validation_column}2:{validation_column}{max_row}">'
            '<formula1>"待 QA 執行,通過,失敗,阻塞"</formula1></dataValidation></dataValidations>'
        )

    # SpreadsheetML requires autoFilter before dataValidations.
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="{MAIN_NS}" xmlns:r="{REL_NS}">
  <dimension ref="A1:{max_column}{max_row}"/>
  <sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A2" sqref="A2"/></sheetView></sheetViews>
  <cols>{columns}</cols>
  <sheetData>{''.join(row_xml)}</sheetData>
  <autoFilter ref="A1:{max_column}{max_row}"/>
  {validation}
  <pageMargins left="0.25" right="0.25" top="0.5" bottom="0.5" header="0.2" footer="0.2"/>
</worksheet>'''


def styles() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="{MAIN_NS}">
  <numFmts count="0"/>
  <fonts count="2"><font><sz val="11"/><name val="Calibri"/><family val="2"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font></fonts>
  <fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="0" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf></cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
  <dxfs count="0"/><tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleMedium9"/>
</styleSheet>'''


def package_parts(title: str, sheet_names: list[str]) -> dict[str, str]:
    worksheet_overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, len(sheet_names) + 1)
    )
    sheet_entries = "".join(
        f'<sheet name="{xml_text(name)}" sheetId="{i}" r:id="rId{i}"/>'
        for i, name in enumerate(sheet_names, 1)
    )
    relationship_entries = "".join(
        f'<Relationship Id="rId{i}" Type="{REL_NS}/worksheet" Target="worksheets/sheet{i}.xml"/>'
        for i in range(1, len(sheet_names) + 1)
    )
    content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  {worksheet_overrides}
</Types>'''
    root_relationships = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{PKG_REL_NS}">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    workbook = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="{MAIN_NS}" xmlns:r="{REL_NS}"><bookViews><workbookView xWindow="0" yWindow="0" windowWidth="24000" windowHeight="12000"/></bookViews><sheets>{sheet_entries}</sheets></workbook>'''
    workbook_relationships = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{PKG_REL_NS}">{relationship_entries}<Relationship Id="rId{len(sheet_names) + 1}" Type="{REL_NS}/styles" Target="styles.xml"/></Relationships>'''
    return {
        "[Content_Types].xml": content_types,
        "_rels/.rels": root_relationships,
        "docProps/core.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>{xml_text(title)}</dc:title><dc:creator>Codex</dc:creator></cp:coreProperties>''',
        "docProps/app.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Excel Compatible</Application><AppVersion>16.0000</AppVersion></Properties>''',
        "xl/workbook.xml": workbook,
        "xl/_rels/workbook.xml.rels": workbook_relationships,
        "xl/styles.xml": styles(),
    }


def build(payload: dict, output: Path) -> None:
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("input JSON must contain a non-empty cases array")

    overview = [["案例 ID", "需求單", "案例名稱", "測試角色", "目前狀態", "執行結果", "測試日期", "測試人員", "證據／備註"]]
    detailed = [["案例 ID", "需求單", "案例名稱", "測試目的", "測試角色", "開始前準備", "操作步驟", "預期結果", "通過判定", "執行結果", "測試日期", "測試人員", "證據／備註"]]
    required = ["id", "ticket", "name", "purpose", "roles", "preparation", "steps", "expected", "pass_criteria"]
    for case in cases:
        missing = [key for key in required if not case.get(key)]
        if missing:
            raise ValueError(f"case {case.get('id', '<unknown>')} missing: {', '.join(missing)}")
        result = case.get("result") or "待 QA 執行"
        overview.append([case["id"], case["ticket"], case["name"], case["roles"], "待 QA 執行", result, case.get("test_date", ""), case.get("tester", ""), case.get("evidence", "")])
        detailed.append([case["id"], case["ticket"], case["name"], case["purpose"], case["roles"], case["preparation"], normalize_steps(case["steps"]), case["expected"], case["pass_criteria"], result, case.get("test_date", ""), case.get("tester", ""), case.get("evidence", "")])

    instructions = [["填寫項目", "使用方式"], ["測試前", "確認測試帳號與合成資料已準備完成；未完成請標示待 QA 執行或阻塞。"], ["執行結果", "選擇待 QA 執行、通過、失敗或阻塞。"], ["證據／備註", "填寫畫面截圖位置、遮罩後識別碼及異常說明，不貼敏感資料。"], ["判定原則", "所有步驟與預期結果都符合才判定通過；未執行不可填通過。"]]
    sheet_names = ["測試總覽", "測試案例", "填寫說明"]
    sheets = [
        worksheet(overview, [16, 12, 30, 34, 16, 16, 14, 18, 40], "F"),
        worksheet(detailed, [16, 12, 30, 34, 34, 42, 58, 46, 46, 16, 14, 18, 40], "J"),
        worksheet(instructions, [24, 100], None),
    ]
    parts = package_parts(payload.get("title", "Manual Test Cases"), sheet_names)
    parts.update({f"xl/worksheets/sheet{i}.xml": sheet for i, sheet in enumerate(sheets, 1)})
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name, content in parts.items():
            archive.writestr(name, content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(json.loads(args.input.read_text(encoding="utf-8")), args.output)
    print(f"created {args.output}")


if __name__ == "__main__":
    main()
