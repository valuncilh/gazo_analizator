#!/usr/bin/env python3
"""Generate explicitly preliminary ESKD-style drawing previews from project CAD.

The SVG pages are review aids, not released drawings. The stamp and document
codes remain provisional pending confirmation of the actual MAI assignment.
"""
from __future__ import annotations
import html
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PCB = ROOT / "cad/kicad/gazo_analizator_preliminary.kicad_pcb"
OUT = ROOT / "cad/drawings/exports"
OUT.mkdir(parents=True, exist_ok=True)
PAGE_W, PAGE_H = 420.0, 297.0
FRAME = (20.0, 5.0, 415.0, 287.0)
STAMP = (230.0, 232.0, 185.0, 55.0)
PREVIEW = "ПРЕДВАРИТЕЛЬНЫЙ МАКЕТ — НЕ ДЛЯ ИЗГОТОВЛЕНИЯ"


def esc(value):
    return html.escape(str(value), quote=True)


def ln(x1, y1, x2, y2, width=0.25, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" '
            f'stroke="#111" stroke-width="{width:.3f}"{d}/>')


def rect(x, y, w, h, width=0.25, fill="none", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" '
            f'fill="{fill}" stroke="#111" stroke-width="{width:.3f}"{d}/>')


def circ(x, y, r, width=0.25, fill="none"):
    return (f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" '
            f'stroke="#111" stroke-width="{width:.3f}"/>')


def txt(x, y, content, size=2.8, anchor="start", weight="normal", fill="#111", rotate=None):
    transform = f' transform="rotate({rotate} {x:.3f} {y:.3f})"' if rotate is not None else ""
    return (f'<text x="{x:.3f}" y="{y:.3f}" font-family="Arial, sans-serif" '
            f'font-size="{size:.3f}" text-anchor="{anchor}" font-weight="{weight}" '
            f'fill="{fill}"{transform}>{esc(content)}</text>')


def poly(points, width=0.25, fill="none", dash=None):
    coords = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{coords}" fill="{fill}" stroke="#111" stroke-width="{width:.3f}"{d}/>'


def dim_h(x1, x2, y, ext_y1, ext_y2, label):
    out = [
        ln(x1, ext_y1, x1, y+2, 0.15),
        ln(x2, ext_y2, x2, y+2, 0.15),
        ln(x1, y, x2, y, 0.18),
        ln(x1, y, x1+2.2, y-1, 0.18),
        ln(x1, y, x1+2.2, y+1, 0.18),
        ln(x2, y, x2-2.2, y-1, 0.18),
        ln(x2, y, x2-2.2, y+1, 0.18),
        txt((x1+x2)/2, y-1.5, label, 2.4, "middle"),
    ]
    return "".join(out)


def dim_v(x, y1, y2, ext_x1, ext_x2, label):
    out = [
        ln(ext_x1, y1, x-2, y1, 0.15),
        ln(ext_x2, y2, x-2, y2, 0.15),
        ln(x, y1, x, y2, 0.18),
        ln(x, y1, x-1, y1+2.2, 0.18),
        ln(x, y1, x+1, y1+2.2, 0.18),
        ln(x, y2, x-1, y2-2.2, 0.18),
        ln(x, y2, x+1, y2-2.2, 0.18),
        txt(x-2, (y1+y2)/2, label, 2.4, "middle", rotate=-90),
    ]
    return "".join(out)


def sheet_open(title, code, scale):
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297">',
        '<rect x="0" y="0" width="420" height="297" fill="white"/>',
        rect(FRAME[0], FRAME[1], FRAME[2]-FRAME[0], FRAME[3]-FRAME[1], 0.35),
        txt(25, 13, title, 4.3, weight="bold"),
        txt(25, 18, PREVIEW, 2.6, weight="bold", fill="#922"),
        txt(415, 13, f"Формат A3 • Масштаб эскиза {scale}", 2.5, "end"),
    ]
    out.append(stamp(code, title, scale))
    return out


def stamp(code, title, scale):
    x, y, w, h = STAMP
    # Deliberately labelled as a provisional layout. This table is not a claim
    # of exact geometrical compliance with a released MAI stamp template.
    out = [rect(x, y, w, h, 0.30)]
    out += [
        ln(x, y+8, x+w, y+8, 0.20),
        ln(x, y+29, x+w, y+29, 0.20),
        ln(x, y+44, x+w, y+44, 0.20),
        ln(x+25, y, x+25, y+8, 0.15),
        ln(x+45, y, x+45, y+8, 0.15),
        ln(x+82, y, x+82, y+8, 0.15),
        ln(x+112, y, x+112, y+8, 0.15),
        ln(x+142, y, x+142, y+8, 0.15),
        ln(x+125, y+8, x+125, y+29, 0.15),
        ln(x+155, y+8, x+155, y+29, 0.15),
        ln(x+118, y+29, x+118, y+44, 0.15),
        ln(x+145, y+29, x+145, y+44, 0.15),
        ln(x+165, y+29, x+165, y+44, 0.15),
    ]
    labels = [
        (x+2, y+3.5, "Изм."),
        (x+27, y+3.5, "Лист"),
        (x+47, y+3.5, "№ докум."),
        (x+84, y+3.5, "Подп."),
        (x+114, y+3.5, "Дата"),
        (x+144, y+3.5, "Лист/листов"),
        (x+2, y+12, "Изделие"),
        (x+2, y+16, "Бытовой сигнализатор утечки газа"),
        (x+2, y+21, "Документ"),
        (x+2, y+26, title[:60]),
        (x+127, y+12, "Литера: не назначена"),
        (x+127, y+17, "Масса: не определена"),
        (x+127, y+22, f"Масштаб: {scale}"),
        (x+2, y+33, "Разработал: __________________"),
        (x+2, y+38, "Проверил: ____________________"),
        (x+2, y+42, "Н.контр.: ____________________"),
        (x+120, y+33, "Дата: __.__.____"),
        (x+147, y+33, "Лист: 1"),
        (x+167, y+33, "Всего: 1"),
        (x+2, y+48, "Обозначение: СОГЛАСОВАТЬ"),
        (x+2, y+52, f"{code} — ВРЕМЕННОЕ"),
    ]
    out.extend(txt(a,b,c,1.9 if "Бытовой" not in c and "Документ" not in c else 2.2,
                   weight="bold" if c in ("Изделие","Документ") else "normal",
                   fill="#922" if ("СОГЛАСОВАТЬ" in c or "ВРЕМЕННОЕ" in c) else "#111")
               for a,b,c in labels)
    return "".join(out)


def extract_expr(text, start):
    depth, quoted, escaped = 0, False, False
    for idx in range(start, len(text)):
        ch = text[idx]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        else:
            if ch == '"':
                quoted = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[start:idx+1]
    raise ValueError("Unbalanced KiCad footprint S-expression")


def read_footprints():
    if not PCB.is_file():
        raise SystemExit(f"Missing preliminary KiCad board: {PCB}")
    board = PCB.read_text(encoding="utf-8")
    result = []
    cursor = 0
    pattern = re.compile(r'\(footprint "([^"]+)"')
    while True:
        match = pattern.search(board, cursor)
        if not match:
            break
        block = extract_expr(board, match.start())
        cursor = match.start() + len(block)
        # KiCad may serialize the footprint position on a later line after pcbnew.SaveBoard().
        # Search the balanced footprint block rather than only the first line.
        pos = re.search(r'\(at\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\)', block)
        ref = re.search(r'\(property "Reference" "([^"]+)"', block)
        value = re.search(r'\(property "Value" "([^"]+)"', block)
        if not pos or not ref:
            continue
        result.append({
            "lib": match.group(1),
            "ref": ref.group(1),
            "value": value.group(1) if value else "",
            "x": float(pos.group(1)),
            "y": float(pos.group(2)),
            "rotation": float(pos.group(3)),
        })
    return result


def copper_item_counts():
    """Count routed copper records from the current KiCad board file."""
    board_text = PCB.read_text(encoding="utf-8")
    segments = len(re.findall(r"\(segment\b", board_text))
    vias = len(re.findall(r"\(via\b", board_text))
    return segments, vias

def pcb_sheet(parts):
    out = sheet_open("Чертёж печатной платы — предварительная компоновка", "ПП?", "2:1")
    scale, ox, oy = 1.8, 42.0, 45.0
    board_x, board_y, board_w, board_h = 100.0, 100.0, 72.0, 50.0
    segments, vias = copper_item_counts()
    if segments + vias:
        route_label = f"Автотрассировка: {segments} сегм., {vias} via."
        route_detail = "Проверить DRC, связность и маршрут вручную."
    else:
        route_label = "Плата не трассирована."
        route_detail = "Проверить nets по завершённой схеме Э3."
    X = lambda x: ox+(x-board_x)*scale
    Y = lambda y: oy+(y-board_y)*scale
    out.append(rect(X(100),Y(100),board_w*scale,board_h*scale,0.35))
    # Drill points are read from the actual KiCad board positions.
    for p in parts:
        x,y,lib = p["x"],p["y"],p["lib"]
        sx,sy=X(x),Y(y)
        if "MountingHole" in lib:
            out.append(circ(sx,sy,1.6*scale,0.22))
            out.append(circ(sx,sy,0.35*scale,0.18))
            continue
        if "Buzzer" in lib:
            out.append(circ(sx,sy,6*scale,0.25))
            out.append(circ(sx,sy,4*scale,0.18))
        elif "LED_" in lib:
            out.append(circ(sx,sy,2.5*scale,0.22))
        elif "R_0805" in lib or "C_0805" in lib:
            out.append(rect(sx-scale,sy-0.62*scale,2*scale,1.24*scale,0.18))
        elif "KT26" in lib:
            out.append(rect(sx-3.1*scale,sy-2*scale,6.2*scale,4*scale,0.18))
        elif "KR1006" in lib:
            out.append(rect(sx-5*scale,sy-3.75*scale,10*scale,7.5*scale,0.22))
        elif "SOT23" in lib:
            out.append(rect(sx-1.5*scale,sy-scale,3*scale,2*scale,0.22))
        elif "PinHeader" in lib:
            out.append(rect(sx-1.4*scale,sy-3*scale,2.8*scale,6*scale,0.18))
        elif "Capacitor_THT" in lib:
            radius = 3.4 if p["ref"]=="C3" else (3.0 if p["ref"]=="C1" else 2.0)
            out.append(circ(sx,sy,radius*scale,0.20))
        elif "PowerIn" in lib or "SA1" in lib:
            out.append(rect(sx-3*scale,sy-4*scale,6*scale,8*scale,0.18))
        else:
            out.append(rect(sx-2*scale,sy-1.5*scale,4*scale,3*scale,0.18))
        label = p["ref"]
        if label in {"J1","J2","J3","U2","VT1","VT2","DA1","HA1","HL1","HL2","R4","R5","R9","H1","H2","H3","H4","VD1","P1","J4"}:
            out.append(txt(sx+2.2,sy-2.0,label,1.8,weight="bold"))
    out.append(dim_h(X(100),X(172),oy+board_h*scale+9,oy+board_h*scale,oy+board_h*scale,"72"))
    out.append(dim_v(ox+board_w*scale+10,Y(100),Y(150),ox+board_w*scale,ox+board_w*scale,"50"))
    out.extend([
        txt(220,42,"Параметры платы",3.1,weight="bold"),
        txt(220,49,"Контур платы: 72 × 50 мм",2.6),
        txt(220,55,"Толщина FR-4: 1,6 мм, предварительное допущение",2.3),
        txt(220,65,"Четыре отверстия: Ø3,2 мм, монтаж M3 — TBC",2.3),
        txt(220,75,route_label,2.3),
        txt(220,80,route_detail,2.3),
        txt(220,90,"Не выпускать Gerber для производства.",2.3,weight="bold",fill="#922"),
        txt(220,104,"Критичные открытые вопросы",3.1,weight="bold"),
        txt(220,111,"• распиновка конкретного КТ3102ГМ для VT1/VT2",2.3),
        txt(220,117,"• физический потенциометр P1, переключатель SA1",2.3),
        txt(220,123,"• разъём XS1 и его ввод в корпус",2.3),
        txt(220,129,"• корпуса и мощность пассивных компонентов",2.3),
        txt(220,135,"• схема-to-PCB netlist, ERC и полный DRC",2.3),
        txt(36,179,"Эскиз показывает расположение по preliminary KiCad PCB.",2.4),
        txt(36,184,"Точные посадочные размеры и зазоры не подтверждены.",2.4),
    ])
    out.append("</svg>")
    return "".join(out)


def overall_view_sheet():
    out = sheet_open("Чертёж общего вида — концепт корпуса", "ВО?", "1:1")
    ox, oy, s = 43.0, 38.0, 1.0
    out.extend([
        txt(ox, 29, "Вид сверху", 2.8, weight="bold"),
        rect(ox,oy,120*s,78*s,0.35),
    ])
    # MQ-4 ventilation field, based on the current concept only.
    cx, cy = ox+20.7*s, oy+39*s
    for row in range(5):
        for col in range(5):
            out.append(circ(cx+(col-2)*5*s,cy+(row-2)*5*s,1.25*s,0.18))
    # Sound aperture and indicators.
    out.append(circ(ox+102.6*s,oy+53*s,4.25*s,0.25))
    out.append(circ(ox+85.4*s,oy+54.5*s,2.75*s,0.18))
    out.append(circ(ox+93.4*s,oy+54.5*s,2.75*s,0.18))
    for x,y in [(6,6),(114,6),(6,72),(114,72)]:
        out.append(circ(ox+x*s,oy+y*s,1.6*s,0.22))
    out.append(dim_h(ox,ox+120*s,oy+88,oy+78,oy+78,"120"))
    out.append(dim_v(ox+130,oy,oy+78*s,ox+120,ox+120,"78"))
    out.extend([
        txt(40,142,"Вид спереди",2.8,weight="bold"),
        rect(43,148,120,42,0.35),
        ln(43,150,163,150,0.2),
        txt(44,157,"Основание",2.2),
        txt(44,146,"Крышка, 2 мм — предварительно",2.1),
        dim_h(43,163,196,190,190,"120"),
        dim_v(174,148,190,163,163,"42"),
        txt(222,142,"Вид сбоку",2.8,weight="bold"),
        rect(222,148,78,42,0.35),
        ln(222,150,300,150,0.2),
        dim_h(222,300,196,190,190,"78"),
        dim_v(310,148,190,300,300,"42"),
        txt(40,207,"Наружные габариты 120 × 78 × 42 мм — допущение для компоновки.",2.4),
        txt(40,213,"Поле вентиляции MQ-4, акустический порт, световоды и крепления требуют проверки.",2.4),
        txt(40,219,"Материал, допуски, IP-защита и механические испытания пока не заданы.",2.4),
    ])
    out.append("</svg>")
    return "".join(out)


def assembly_sheet(parts):
    out = sheet_open("Сборочная компоновка — взрыв-схема", "СБ?", "эскиз")
    # Simplified exploded top views, not yet a fully dimensioned assembly drawing.
    x, y, s = 54.0, 33.0, 0.55
    # Lid
    out.append(txt(38,30,"1 — крышка корпуса",3.0,weight="bold"))
    out.append(rect(x,y,120*s,78*s,0.32))
    for row in range(5):
        for col in range(5):
            out.append(circ(x+(20.7+(col-2)*5)*s,y+(39+(row-2)*5)*s,1.25*s,0.15))
    out.append(circ(x+102.6*s,y+53*s,4.25*s,0.20))
    out.append(circ(x+85.4*s,y+54.5*s,2.75*s,0.15))
    out.append(circ(x+93.4*s,y+54.5*s,2.75*s,0.15))
    # Guide lines indicate separation, not actual fasteners.
    out.extend([ln(95, y+78*s+3, 95, 92, 0.25, "4 2"),
                ln(112, y+78*s+3, 112, 92, 0.25, "4 2")])
    out.append(txt(38,84,"2 — плата управления и индикаторы",3.0,weight="bold"))
    pcbx, pcby, ps = 66.0, 91.0, 0.55
    out.append(rect(pcbx,pcby,72*ps,50*ps,0.30))
    out.append(rect(pcbx+(8/72)*72*ps,pcby+(12/50)*50*ps,25.4*ps,25.4*ps,0.20,dash="2 1"))
    out.append(txt(pcbx+6,pcby+15,"A1",2.5,weight="bold"))
    out.append(circ(pcbx+63*ps,pcby+39*ps,6*ps,0.20))
    out.append(txt(pcbx+63*ps+3.6,pcby+39*ps,"HA1",2.0,weight="bold"))
    for h in [(3.5,3.5),(68.5,3.5),(3.5,46.5),(69.5,47.0)]:
        out.append(circ(pcbx+h[0]*ps,pcby+h[1]*ps,1.6*ps,0.18))
    out.append(ln(95,pcby+50*ps+4,95,141,0.25,"4 2"))
    out.append(ln(112,pcby+50*ps+4,112,141,0.25,"4 2"))
    out.append(txt(38,137,"3 — основание корпуса с опорами",3.0,weight="bold"))
    basex, basey, bs=54.0,145.0,0.55
    out.append(rect(basex,basey,120*bs,78*bs,0.35))
    out.append(rect(basex+2.5*bs,basey+2.5*bs,115*bs,73*bs,0.18,dash="2 1"))
    for hx,hy in [(6,6),(114,6),(6,72),(114,72)]:
        out.append(circ(basex+hx*bs,basey+hy*bs,3.4*bs,0.18))
    out.extend([
        txt(225,40,"Позиции",3.1,weight="bold"),
        txt(225,48,"1. Крышка с вентиляционным полем MQ-4",2.4),
        txt(225,55,"2. Плата управления, ориентир 72 × 50 мм",2.4),
        txt(225,62,"3. Модуль Amperka AMP-B052, 25,4 × 25,4 мм",2.4),
        txt(225,69,"4. Основание и стойки корпуса",2.4),
        txt(225,76,"5. HCM1205X, Ø12 × 9,5 мм",2.4),
        txt(225,87,"Схема установки предварительная.",2.6,weight="bold",fill="#922"),
        txt(225,94,"Крепление A1, профиль MQ-4, проводка,",2.3),
        txt(225,100,"акустический канал и зазоры TBC.",2.3),
        txt(225,115,"Эта взрыв-схема не заменяет утверждённый",2.3),
        txt(225,121,"сборочный чертёж и спецификацию.",2.3),
        txt(38,204,"Размеры и позиции основаны на CAD-концепте. Проверить столкновения и порядок сборки перед выпуском.",2.35),
    ])
    out.append("</svg>")
    return "".join(out)


def electrical_topology_sheet():
    out=sheet_open("Электрическая топология к подготовке Э3", "Э3?", "эскиз")
    # Functional topology overview based on the current vendor SPICE netlist.
    boxes=[
        (35,48,58,28,"A1","MQ-4"),
        (114,48,50,28,"U2","TLV7041-Q1"),
        (188,48,45,28,"VT1","KT3102ГМ"),
        (254,48,52,28,"DA1","КР1006ВИ1"),
        (330,48,60,28,"HL1","R6 + LED"),
        (254,118,52,28,"R9 + SA1","Звук"),
        (330,118,60,28,"VT2 / HA1","HCM1205X"),
    ]
    for x,y,w,h,a,b in boxes:
        out.append(rect(x,y,w,h,0.30))
        out.append(txt(x+w/2,y+10,a,3.0,"middle","bold"))
        out.append(txt(x+w/2,y+17,b,2.5,"middle"))
    # Orthogonal signal paths.
    out.extend([
        ln(93,62,114,62,0.40), txt(103,59,"S",2.5,"middle"),
        ln(164,62,188,62,0.40), txt(176,59,"DOUT′",2.5,"middle"),
        ln(233,62,254,62,0.40), txt(243,59,"RESET",2.3,"middle"),
        ln(306,62,330,62,0.40), txt(318,59,"OUT",2.5,"middle"),
        ln(312,62,312,102,0.40), ln(312,102,280,102,0.40),
        ln(280,102,280,118,0.40), circ(312,62,0.9,0.25,fill="#111"),
        ln(306,132,330,132,0.40), txt(318,129,"VT2 base",2.2,"middle"),
        txt(40,91,"S → U2 / порог и гистерезис → VT1 → RESET → таймер → сигнализация",2.8),
        txt(40,101,"R1/R8 — подтяжка выхода. P1 формирует UREF. RHYS задаёт внешний гистерезис.",2.5),
        txt(40,159,"Схема является функциональным эскизом по текущей расчётной модели, а не официальной Э3.",2.7,weight="bold",fill="#922"),
        txt(40,166,"Перед выпуском требуется проверить pin mapping, полярности, сетевые соединения и состав ПЭ3.",2.4),
        txt(40,173,"Ток/модель A1, выводы DA1 и pinout VT1/VT2 должны соответствовать реальным исполнениям.",2.4),
    ])
    out.append("</svg>")
    return "".join(out)


def main():
    parts = read_footprints()
    if len(parts) < 20:
        raise SystemExit(f"Expected at least 20 PCB footprints, found {len(parts)}")
    outputs={
        "PP_preliminary.svg":pcb_sheet(parts),
        "VO_preliminary.svg":overall_view_sheet(),
        "SB_preliminary_exploded.svg":assembly_sheet(parts),
        "electrical_topology_preliminary.svg":electrical_topology_sheet(),
    }
    for name, content in outputs.items():
        path=OUT/name
        path.write_text(content,encoding="utf-8")
    manifest={
        "status":"PRELIMINARY / NOT FOR FABRICATION",
        "source_pcb":"cad/kicad/gazo_analizator_preliminary.kicad_pcb",
        "footprints_read":len(parts),
        "sheets":list(outputs),
        "stamp":"provisional. Check actual MAI template and code before release.",
        "limitations":[
            "No official KiCad schematic E3 or ERC/netlist parity exists yet.",
            "Board is unrouted and has TBC footprints.",
            "Enclosure dimensions and MQ-4 envelope are assumptions.",
            "Drawing stamp is a preview and is not a normative released title block.",
        ],
    }
    (OUT/"drawing_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Generated {len(outputs)} preliminary SVG sheets from {len(parts)} KiCad footprints.")
    print("Outputs: "+", ".join(outputs))
    print("All sheets are marked PRELIMINARY / NOT FOR FABRICATION.")

if __name__=="__main__":
    main()
