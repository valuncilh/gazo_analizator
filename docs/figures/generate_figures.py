from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon

OUT = Path("docs/figures")
OUT.mkdir(parents=True, exist_ok=True)
INK="#182230"; BLUE="#2166AC"; TEAL="#168A8A"; ORANGE="#D97706"
RED="#B42318"; GREEN="#27864A"; PURPLE="#6941C6"; GREY="#667085"; PALE="#F2F4F7"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10})

def canvas(title, subtitle, size=(14,7.8)):
    fig,ax=plt.subplots(figsize=size,dpi=150)
    ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis("off")
    ax.text(.35,7.62,title,fontsize=18,fontweight="bold",color=INK,va="top")
    ax.text(.36,7.14,subtitle,fontsize=9.5,color=GREY,va="top")
    return fig,ax

def wire(ax,pts,c=INK,lw=1.7,ls="-"):
    x,y=zip(*pts); ax.plot(x,y,color=c,lw=lw,ls=ls,solid_capstyle="round")

def node(ax,x,y,c=INK):
    ax.add_patch(Circle((x,y),.045,facecolor=c,edgecolor=c))

def block(ax,x,y,w,h,title,detail="",edge=BLUE,face="white",dash=False):
    p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.05,rounding_size=.12",
        edgecolor=edge,facecolor=face,linewidth=1.7,linestyle="--" if dash else "-")
    ax.add_patch(p)
    ax.text(x+w/2,y+h*.64,title,ha="center",va="center",fontsize=11,fontweight="bold",color=INK)
    if detail: ax.text(x+w/2,y+h*.29,detail,ha="center",va="center",fontsize=8.5,color=GREY,linespacing=1.25)

def arrow(ax,p1,p2,label="",c=BLUE):
    ax.annotate("",xy=p2,xytext=p1,arrowprops=dict(arrowstyle="-|>",lw=1.8,color=c,mutation_scale=13))
    if label: ax.text((p1[0]+p2[0])/2,(p1[1]+p2[1])/2+.16,label,ha="center",fontsize=9,color=c)

def resistor_v(ax,x,y1,y2,label,c=INK):
    lead=.16
    wire(ax,[(x,y1),(x,y1-lead)],c)
    wire(ax,[(x,y2+lead),(x,y2)],c)
    top=y1-lead; bot=y2+lead
    ys=[top]
    xs=[x]
    n=7
    for i in range(1,n):
        ys.append(top+(bot-top)*i/n); xs.append(x+(.10 if i%2 else -.10))
    ys.append(bot); xs.append(x)
    ax.plot(xs,ys,color=c,lw=1.7)
    ax.text(x+.18,(y1+y2)/2,label,va="center",fontsize=8.5,color=INK)

def resistor_h(ax,x1,x2,y,label,c=INK):
    lead=.16
    wire(ax,[(x1,y),(x1+lead,y)],c); wire(ax,[(x2-lead,y),(x2,y)],c)
    left=x1+lead; right=x2-lead
    xs=[left]; ys=[y]; n=7
    for i in range(1,n):
        xs.append(left+(right-left)*i/n); ys.append(y+(.10 if i%2 else -.10))
    xs.append(right); ys.append(y)
    ax.plot(xs,ys,color=c,lw=1.7)
    ax.text((x1+x2)/2,y+.22,label,ha="center",fontsize=8.5,color=INK)

def ground(ax,x,y):
    wire(ax,[(x,y),(x,y-.12)])
    ax.plot([x-.2,x+.2],[y-.12,y-.12],c=INK,lw=1.5)
    ax.plot([x-.13,x+.13],[y-.2,y-.2],c=INK,lw=1.5)
    ax.plot([x-.06,x+.06],[y-.28,y-.28],c=INK,lw=1.5)

def finish(fig,name):
    fig.tight_layout(pad=.5)
    fig.savefig(OUT/name,dpi=180,bbox_inches="tight",facecolor="white")
    plt.close(fig)

# Figure 1. Architecture diagram.
fig,ax=canvas("Рисунок 1 — функциональная схема сигнализатора",
 "Сводная архитектура. Пунктирная рамка означает аналоговую или поведенческую модель, а не точную принципиальную схему.",(15,8))
wire(ax,[(.7,6.25),(13.2,6.25)],ORANGE,2); ax.text(.7,6.48,"+5 В, стабилизированное питание",color=ORANGE,fontweight="bold")
items=[
(.6,3.9,2.1,1.4,"A1: MQ-4","Аналоговый выход S",TEAL,"#E7F6F2",False),
(3.05,3.9,2.15,1.4,"U2: TLV7041-Q1","Компаратор + гистерезис",BLUE,"#EAF2FF",False),
(5.55,3.9,1.55,1.4,"VT1","Ключ RESET, NPN",PURPLE,"#F3E8FF",True),
(7.5,3.9,1.95,1.4,"DA1: 555","Таймер / генератор",ORANGE,"#FFF4E5",True),
(10.1,4.7,2.2,1.0,"HL1","Красный LED",RED,"#FEF3F2",False),
(10.1,3.0,2.2,1.0,"VT2 + HA1","Звуковой выход",GREEN,"#ECFDF3",True)]
for x,y,w,h,t,d,e,f,ds in items: block(ax,x,y,w,h,t,d,e,f,ds)
for x in [1.65,4.12,6.32,8.48,11.2]: wire(ax,[(x,6.25),(x,5.42 if x<9 else 5.7)],ORANGE,1.0,":")
arrow(ax,(2.7,4.6),(3.05,4.6),"S",TEAL); arrow(ax,(5.2,4.6),(5.55,4.6),"DOUT′",BLUE)
arrow(ax,(7.1,4.6),(7.5,4.6),"RESET",PURPLE)
arrow(ax,(9.45,4.75),(10.1,5.15),"OUT",ORANGE); arrow(ax,(9.45,4.35),(10.1,3.5),"OUT",ORANGE)
for x,t,d,c in [(0.8,"Эквивалент MQ-4","Rs меняется с CH₄",TEAL),(3.9,"Порог и ОС","P1 + RHYS",BLUE),(7.0,"Модель 555","Транзиентный анализ",ORANGE),(10.1,"Нагрузка","LED, NPN, HA1, VD1",GREEN)]:
    block(ax,x,1.15,2.6,1.2,t,d,c,"white",True)
ax.text(.75,.55,"Метки «аналог» и пунктир показывают участки, где модель не тождественна установленному компоненту.",fontsize=9,color=GREY)
finish(fig,"fig01_system_architecture.png")

# Figure 2. MQ-4 divider.
fig,ax=canvas("Рисунок 2 — приближённая электрическая модель MQ-4",
 "Эквивалент Rs + RL. Он не воспроизводит внутреннюю схему платы Amperka и не является калибровкой конкретного экземпляра.",(15,7.8))
ax.text(1.0,6.1,"+5 В",ha="center",fontsize=11,fontweight="bold",color=ORANGE)
wire(ax,[(1,5.9),(1,5.45)],ORANGE,1.7); resistor_v(ax,1,5.45,3.7,"Rs(CH₄)",TEAL)
wire(ax,[(1,3.7),(1,3.15),(2.7,3.15)]); node(ax,1,3.15,TEAL)
ax.text(.67,3.38,"S",fontweight="bold",color=TEAL)
wire(ax,[(2.7,3.15),(2.7,2.6)]); resistor_v(ax,2.7,2.6,1.3,"RL = 20 кОм",BLUE)
wire(ax,[(2.7,1.3),(2.7,1.05)]); ground(ax,2.7,1.05)
ax.text(3.6,3.2,"US = VCC · RL / (Rs + RL)",fontsize=11,fontweight="bold",color=BLUE)
ax.text(6.6,6.1,"Сценарные точки при VCC = 5 В",fontsize=12,fontweight="bold",color=INK)
for x,t in [(6.7,"Состояние"),(9.3,"Rs"),(11.0,"Rs/R0"),(12.4,"US")]:
    ax.text(x,5.55,t,fontsize=9,fontweight="bold",color=GREY)
rows=[("Чистый воздух","88 кОм","4,4","0,926 В",TEAL),("1000 ppm CH₄","20 кОм","1,0","2,500 В",ORANGE),("5000 ppm CH₄","12 кОм","0,6","3,125 В",RED)]
for i,row in enumerate(rows):
    y=4.9-i*.72
    ax.plot([6.6,13.5],[y-.24,y-.24],c="#E4E7EC",lw=1)
    for x,val in zip([6.7,9.3,11.0,12.4],row[:4]):
        ax.text(x,y,val,fontsize=10,color=row[4] if x==6.7 else INK)
block(ax,6.65,1.55,6.75,.95,"Статус параметров","RL=20 кОм из библиотеки TroykaMQ; R0 и отношения Rs/R0 — сценарные.",ORANGE,"#FFF4CC",False)
ax.text(.7,.42,"График нужен для проверки направления изменения S. Уставка 1000 ppm должна калиброваться по известной концентрации.",fontsize=9,color=GREY)
finish(fig,"fig02_mq4_equivalent.png")

# Figure 3. Comparator with feedback.
fig,ax=canvas("Рисунок 3 — приближённая схема компаратора с гистерезисом",
 "Выбранный U2 — TLV7041-Q1. Внешние номиналы показаны как рабочая топология; точная внутренняя схема IC здесь не раскрывается.",(15,8))
wire(ax,[(.8,6.35),(13.0,6.35)],ORANGE,1.8); ax.text(.8,6.57,"+5 В",color=ORANGE,fontweight="bold")
wire(ax,[(1.55,6.35),(1.55,5.85)],ORANGE); resistor_v(ax,1.55,5.85,4.85,"P1 верх",ORANGE)
node(ax,1.55,4.5,TEAL); resistor_v(ax,1.55,4.5,3.3,"P1 низ",BLUE)
wire(ax,[(1.55,4.85),(1.55,4.5)],TEAL); wire(ax,[(1.55,3.3),(1.55,2.9)]); ground(ax,1.55,2.9)
wire(ax,[(1.55,4.5),(3.2,4.5)],TEAL,1.8); ax.text(1.85,4.72,"U_REF",color=TEAL,fontweight="bold")
block(ax,4.55,3.0,2.35,2.4,"U2: TLV7041","IN+ ← U_REF\nIN− ← S\nOUT = DOUT′",BLUE,"#EAF2FF",False)
wire(ax,[(3.2,4.5),(4.55,4.5)],TEAL,1.7); wire(ax,[(3.2,3.55),(4.55,3.55)],RED,1.7)
ax.text(3.25,3.77,"S",color=RED,fontweight="bold")
wire(ax,[(6.9,4.15),(8.55,4.15)],BLUE,1.8); node(ax,8.55,4.15,BLUE); ax.text(7.0,4.4,"DOUT′",color=BLUE,fontweight="bold")
for x,lab in [(9.65,"R1=160 кОм"),(11.55,"R8=2,2 кОм")]:
    wire(ax,[(x,6.35),(x,5.8)],ORANGE); resistor_v(ax,x,5.8,4.25,lab); wire(ax,[(x,4.25),(x,4.15),(8.55,4.15)],BLUE); node(ax,x,4.15,BLUE)
wire(ax,[(8.55,4.15),(8.55,5.65)],TEAL,1.4); resistor_h(ax,6.6,8.55,5.65,"RHYS = 100 кОм",TEAL)
wire(ax,[(6.6,5.65),(3.2,5.65),(3.2,4.5)],TEAL,1.4); node(ax,3.2,4.5,TEAL)
block(ax,9.2,1.45,3.9,1.3,"Логика инверсии","S > U_REF → DOUT′ low\nS < U_REF → DOUT′ high",BLUE,PALE,False)
ax.text(.8,.45,"Порог и ширина гистерезиса зависят от настройки P1, RHYS, уровней выхода и параметров фактического компаратора.",fontsize=9,color=GREY)
finish(fig,"fig03_comparator_hysteresis.png")

# Figure 4. 555 timer functional analogue.
fig,ax=canvas("Рисунок 4 — функциональный аналог астабильного таймера 555",
 "TLC555 — аналог для SPICE-проверки, а не электрически точная замена биполярного КР1006ВИ1.",(15,7.8))
wire(ax,[(.9,6.3),(7.8,6.3)],ORANGE,1.8); ax.text(.9,6.53,"+5 В",color=ORANGE,fontweight="bold")

# Timing network is drawn separately from RESET so the two nets cannot be
# mistaken as electrically connected in this approximate illustration.
wire(ax,[(2.0,6.3),(2.0,5.8)],ORANGE)
resistor_v(ax,2.0,5.8,4.55,"R4=8,2 кОм",ORANGE)
wire(ax,[(2.0,4.55),(2.0,4.1)],INK)
node(ax,2.0,4.1); ax.text(1.03,4.26,"DISCH",fontsize=9,color=INK)
resistor_h(ax,2.2,4.7,4.1,"R5=8,2 кОм",BLUE)
wire(ax,[(4.7,4.1),(4.7,3.55)],BLUE); node(ax,4.7,4.1,BLUE)
ax.text(4.48,4.34,"CT",color=BLUE,fontweight="bold")
ax.plot([4.43,4.97],[3.15,3.15],c=INK,lw=1.9)
ax.plot([4.43,4.97],[2.9,2.9],c=INK,lw=1.9)
wire(ax,[(4.7,3.55),(4.7,3.15)],BLUE)
wire(ax,[(4.7,2.9),(4.7,2.3)],INK)
ground(ax,4.7,2.3)
ax.text(5.0,3.03,"C1=4,7 мкФ",fontsize=9,color=INK)

block(ax,6.45,3.1,2.55,2.25,"DA1: TLC555","THRES/TRIG ← CT\nDISCH ← узел R4/R5\nRESET ← VT1\nOUT → нагрузка",ORANGE,"#FFF4E5",True)
arrow(ax,(4.7,4.1),(6.45,4.45),"CT",BLUE)
arrow(ax,(2.0,4.1),(6.45,3.85),"DISCH",GREY)
block(ax,.95,1.0,2.45,1.15,"VT1","Открыт → RESET low\nЗакрыт → RESET high",PURPLE,"#F3E8FF",True)
arrow(ax,(3.4,1.58),(5.25,1.58),"RESET",PURPLE)
arrow(ax,(5.25,1.58),(6.45,3.35),"",PURPLE)
arrow(ax,(9.0,4.15),(10.25,4.15),"OUT",ORANGE)
block(ax,10.25,3.3,2.8,1.5,"Нагрузки","HL1 через R6\nVT2/HA1 через R9",GREEN,"#ECFDF3",True)
block(ax,9.7,1.0,3.7,1.15,"Номинал не исправлен","4,7 мкФ → около 12,47 Гц",RED,"#FEF3F2",False)
ax.text(.8,.4,"CT и RESET — разные цепи. 47 мкФ здесь не установлен, а рассматривается только как сравнение (~1,25 Гц).",fontsize=9,color=GREY)
finish(fig,"fig04_timer_555_analogue.png")

# Figure 5. Buzzer output approximation.
fig,ax=canvas("Рисунок 5 — приближённая схема звукового выхода",
 "Зуммер заменён резистивным эквивалентом для оценки постоянного тока. Это не модель акустики или внутреннего генератора HA1.",(15,7.8))
wire(ax,[(.9,6.3),(12.8,6.3)],ORANGE,1.8); ax.text(.9,6.52,"+5 В",color=ORANGE,fontweight="bold")
wire(ax,[(7.6,6.3),(7.6,5.75)],ORANGE); block(ax,6.8,4.75,1.6,1.0,"HA1","активный",ORANGE,"#FFF4E5",True)
wire(ax,[(7.6,4.75),(7.6,3.55),(5.8,3.55)],INK,1.8); node(ax,7.6,3.55)
# protection diode branch
wire(ax,[(9.25,6.3),(9.25,5.7)],GREEN,1.4)
ax.add_patch(Polygon([[9.07,5.22],[9.43,5.22],[9.25,5.55]],closed=True,facecolor="white",edgecolor=GREEN,lw=1.4))
ax.plot([9.04,9.46],[5.62,5.62],c=GREEN,lw=1.7)
wire(ax,[(9.25,5.62),(9.25,6.3)],GREEN,1.3); wire(ax,[(9.25,5.22),(9.25,3.55),(7.6,3.55)],GREEN,1.3)
ax.text(9.7,5.4,"VD1, катод к +5 В",fontsize=9,color=GREEN)
block(ax,4.4,2.1,1.8,1.4,"VT2","NPN low-side\nключ, 2N3904*",PURPLE,"#F3E8FF",True)
wire(ax,[(5.8,3.55),(5.8,3.0)],INK,1.7); wire(ax,[(5.25,2.1),(5.25,1.55)]); ground(ax,5.25,1.55)
wire(ax,[(.9,3.0),(1.35,3.0)],BLUE,1.7); resistor_h(ax,1.35,3.2,3.0,"R9=560 Ω",BLUE)
wire(ax,[(3.2,3.0),(3.55,3.0)],BLUE); wire(ax,[(3.55,3.0),(3.55,2.72)],BLUE)
wire(ax,[(3.55,2.72),(3.84,2.92)],BLUE); wire(ax,[(3.92,3.0),(4.4,3.0)],BLUE)
ax.text(.9,3.27,"OUT",fontsize=9.5,color=BLUE,fontweight="bold"); ax.text(3.62,3.25,"SA1",fontsize=9,color=BLUE)
block(ax,.95,4.65,2.65,1.0,"HL1","OUT → R6=220 Ω → LED",RED,"#FEF3F2",False)
block(ax,10.0,2.0,3.05,1.6,"Эквивалент HA1","RBZ ≈ 166,7 Ω\nI ≈ 30 мА при 5 В\nНе настоящий зуммер",ORANGE,"#FFF4CC",True)
ax.text(.8,.42,"* 2N3904 используется вместо КТ3102ГМ как сценарный аналог. Ток базы и насыщение нужно подтвердить отдельно.",fontsize=9,color=GREY)
finish(fig,"fig05_buzzer_driver_analogue.png")

# Figure 8. Timer comparison.
fig,ax=plt.subplots(figsize=(12,6),dpi=150)
fig.suptitle("Рисунок 8 — сравнение расчётного периода таймера",fontsize=17,fontweight="bold",color=INK,y=.97)
labels=["C1 = 4,7 мкФ\nисходный номинал","C1 = 47 мкФ\nсравнительный вариант"]
period=[80.20065,801.6786]
bars=ax.bar(labels,period,color=[BLUE,ORANGE],width=.55)
ax.set_ylabel("Период OUT, мс"); ax.set_ylim(0,900); ax.grid(axis="y",alpha=.25)
for b,v in zip(bars,period):
    ax.text(b.get_x()+b.get_width()/2,v+18,f"{v:.2f} мс\n{1000/v:.2f} Гц",ha="center",va="bottom",fontweight="bold",color=INK)
ax.text(.02,-.18,"ngspice 42, поведенческая модель. 47 мкФ не утверждён как новый номинал схемы.",transform=ax.transAxes,fontsize=9,color=GREY)
fig.tight_layout(rect=[0,.05,1,.92]); fig.savefig(OUT/"fig08_timer_period_comparison.png",dpi=180,bbox_inches="tight",facecolor="white"); plt.close(fig)
# Add numbered Russian captions to the charts produced by ngspice.
from PIL import Image, ImageDraw, ImageFont

def caption_plot(source, destination, title, subtitle):
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(f"Expected ngspice plot is missing: {source}")
    im = Image.open(source).convert("RGB")
    w, h = im.size
    band = 108
    canvas = Image.new("RGB", (w, h + band), "white")
    canvas.paste(im, (0, band))
    draw = ImageDraw.Draw(canvas)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    draw.text((42, 12), title, fill=INK, font=font_title)
    draw.text((44, 62), subtitle, fill=GREY, font=font_sub)
    canvas.save(destination, optimize=True)

# Preserve the published reference schematic as a separately attributed figure.
source_scheme = Path("docs/figures/source_schematic.webp")
if source_scheme.is_file():
    source_im = Image.open(source_scheme).convert("RGB")
    source_width = 1500
    source_height = round(source_im.height * source_width / source_im.width)
    source_im = source_im.resize((source_width, source_height), Image.Resampling.LANCZOS)
    top_band, bottom_band = 112, 44
    source_canvas = Image.new("RGB", (source_width, source_height + top_band + bottom_band), "white")
    source_canvas.paste(source_im, (0, top_band))
    source_draw = ImageDraw.Draw(source_canvas)
    source_draw.text(
        (42, 12),
        "Рисунок 0 — исходная схема из публикации С. Кузнецова",
        fill=INK,
        font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 29),
    )
    source_draw.text(
        (44, 62),
        "Источник: «Радио», 2022, № 11, с. 46–48. В оригинале используется модуль с DOUT.",
        fill=GREY,
        font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17),
    )
    source_draw.text(
        (42, top_band + source_height + 10),
        "Референсный рисунок, не изменённая авторская схема. Адаптация под аналоговый выход S оформлена отдельно.",
        fill=GREY,
        font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15),
    )
    source_canvas.save(OUT / "fig00_source_scheme_from_article.png", optimize=True)

caption_plot(
    "spice/bode_linearized.png",
    OUT / "fig06_bode_linearized_submodels.png",
    "Рисунок 6 — АЧХ и ФЧХ линейных подсистем",
    "MQ-4 — условная аппроксимация. RC-состояния таймера показаны отдельно.",
)
caption_plot(
    "spice/vendor_chain_plots.png",
    OUT / "fig07_transient_vendor_model.png",
    "Рисунок 7 — переходные процессы тестовой цепочки",
    "TI TLV7041/TLC555, аналог 2N3904 вместо КТ3102ГМ, сценарный MQ-4 делитель.",
)

print("Generated annotated schematic PNGs in", OUT)
