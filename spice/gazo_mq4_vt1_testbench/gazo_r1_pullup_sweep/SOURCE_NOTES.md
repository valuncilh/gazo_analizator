# Источники и допущения

1. Joy-IT SEN-MQ4-V2 datasheet, 2026-01-15: питание 5 V, AOUT 0–5 V, DOUT 0/5 V, встроенный компаратор с регулируемым порогом. Документ не публикует схему DOUT, active-high/active-low, тип выходного транзистора и допустимый ток вывода.
   https://joy-it.net/en/products/SEN-MQ4-V2
2. Texas Instruments NE555 datasheet Rev. K, section 5.5: RESET voltage level min 0.3 V, typ 0.7 V, max 1.0 V при VCC=5…15 V, TA=25 °C (табличные условия).
   https://www.ti.com/document-viewer/NE555/datasheet
3. MQSensorsLib — программная библиотека обработки аналогового MQ-сигнала. Она рассчитывает Rs из AOUT и RL, далее использует калибровочный R0 и пользовательские коэффициенты регрессии. Она не предоставляет схемотехническую модель платы Joy-IT SEN-MQ4-V2.
   https://github.com/miguel5612/MQSensorsLib

Модель DOUT open-collector и условное сопротивление sink 10 Ом используются только как проверяемая гипотеза. Значения R1 — sweep для оценки чувствительности, не рекомендации для переделки.
