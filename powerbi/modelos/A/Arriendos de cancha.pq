let
    Libro = Excel.Workbook(File.Contents(RutaExcel), null, true),
    Hoja = Libro{[Item="Arriendos de cancha",Kind="Sheet"]}[Data],
    Cabeceras = Table.PromoteHeaders(Hoja, [PromoteAllScalars=true]),
    Contrato = Table.SelectColumns(Cabeceras, {"ID arriendocancha", "Fecha", "Día semana", "Hora inicio", "Hora termino", "Uso de cancha", "Cancha", "Donde pagó", "Cliente", "Uso de luz artificial(Si/No)", "Monto a pagar", "¿pagado¡", "Pagado en ", "IVA (19%)", "Comisión mercago pago", "recibido", "Neto Sin IVA"}, MissingField.Error),
    Tipos = Table.TransformColumnTypes(Contrato, {{"ID arriendocancha", type text}, {"Fecha", type date}, {"Día semana", type text}, {"Hora inicio", type time}, {"Hora termino", type time}, {"Uso de cancha", type number}, {"Cancha", type text}, {"Donde pagó", type text}, {"Cliente", type text}, {"Uso de luz artificial(Si/No)", type text}, {"Monto a pagar", Currency.Type}, {"¿pagado¡", type text}, {"Pagado en ", type text}, {"IVA (19%)", Currency.Type}, {"Comisión mercago pago", Currency.Type}, {"recibido", Currency.Type}, {"Neto Sin IVA", Currency.Type}}, "es-CL"),
    Filtrado = Table.SelectRows(Tipos, each [Hora inicio] <> null),
    CanchaClave = Table.DuplicateColumn(Filtrado, "Cancha", "Cancha original"),
    Deporte = Table.TransformColumns(CanchaClave, {{"Cancha", each if Text.StartsWith(_, "Cancha P") then "Pádel" else if Text.StartsWith(_, "Cancha T") then "Tenis" else error "Cancha desconocida", type text}}),
    Horas = Table.AddColumn(Deporte, "Horas de Uso", each Duration.TotalHours([Hora termino]-[Hora inicio]), type number),
    Dia = Table.AddColumn(Horas, "Día correspondiente", each Date.DayOfWeekName([Fecha], "es-CL"), type text),
    Orden = Table.AddColumn(Dia, "Orden Día", each Date.DayOfWeek([Fecha], Day.Monday)+1, Int64.Type)
in
    Orden
