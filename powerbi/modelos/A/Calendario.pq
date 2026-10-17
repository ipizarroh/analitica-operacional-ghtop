let
    Libro = Excel.Workbook(File.Contents(RutaExcel), null, true),
    Hoja = Libro{[Item="CalendarioOperacion",Kind="Sheet"]}[Data],
    Cabeceras = Table.PromoteHeaders(Hoja, [PromoteAllScalars=true]),
    Contrato = Table.SelectColumns(Cabeceras, {"Fecha", "Abierto", "Horas disponibles por cancha", "Motivo"}, MissingField.Error),
    Tipos = Table.TransformColumnTypes(Contrato, {{"Fecha", type date}, {"Abierto", type logical}, {"Horas disponibles por cancha", type number}, {"Motivo", type text}}, "es-CL"),
    Mes = Table.AddColumn(Tipos, "Mes", each Date.ToText([Fecha], "yyyy-MM"), type text),
    Dia = Table.AddColumn(Mes, "Día", each Date.DayOfWeekName([Fecha], "es-CL"), type text),
    Orden = Table.AddColumn(Dia, "Orden Día", each Date.DayOfWeek([Fecha], Day.Monday)+1, Int64.Type)
in
    Orden
